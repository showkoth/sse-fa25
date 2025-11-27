#!/usr/bin/env python3
"""
This analyzer uses symbolic execution to generate inputs and
performs dynamic taint analysis to detect SQL injection vulnerabilities.
"""

import ast
import inspect
import linecache
import re
import sys
import z3
from vuln import vulnerable_function

# Regex to detect SQL execution sink
SINK_REGEX = re.compile(r".*cursor\.execute\((.*)\)")


class TaintAnalyzer:
    
    def __init__(self):
        """Initialize the taint analyzer."""
        self.tainted_variables = set()
        self.inputs = []
        self.vulnerable_paths = []
        self.current_path = []
    
    def mark_as_tainted(self, var):
        """Mark a specific variable as tainted."""
        self.tainted_variables.add(id(var))
    
    def generate_inputs(self):
        """
        Generate inputs for x and y based on symbolic execution
        and constraint solving using Z3.
        
        This method:
        1. Parses the vulnerable_function to extract its AST
        2. Collects all possible path conditions
        3. Uses Z3 solver to find concrete values for x and y
        4. Creates test inputs with SQL injection payloads
        """
        # Get the source code of vulnerable_function
        function_source = inspect.getsource(vulnerable_function)
        function_ast = ast.parse(function_source)
        
        # Collect path conditions from the AST
        paths = self.collect_conditions(function_ast)
        
        # For each path, use Z3 to solve for x and y
        for i, path_constraint in enumerate(paths):
            print(f"\n[*] Solving Path {i + 1}: {path_constraint}")
            
            # Create Z3 solver and variables
            solver = z3.Solver()
            x = z3.Int("x")
            y = z3.Int("y")
            
            try:
                # Add the path constraint
                solver.add(eval(path_constraint))
                
                # Check if satisfiable
                if solver.check() == z3.sat:
                    model = solver.model()
                    x_val = model[x].as_long() if model[x] is not None else 0
                    y_val = model[y].as_long() if model[y] is not None else 0
                    
                    print(f"   Solution found: x={x_val}, y={y_val}")
                    
                    # Create test input with SQL injection payload
                    # Using a tainted SQL query that exploits the vulnerability
                    # This payload bypasses authentication by making the WHERE clause always true
                    query = "SELECT * FROM users WHERE username = 'admin' OR '1'='1' --"
                    
                    self.inputs.append({
                        'query': query,
                        'x': x_val,
                        'y': y_val,
                        'path': i + 1
                    })
                    
                    # Mark the query as tainted (this is our source)
                    self.mark_as_tainted(query)
                else:
                    print(f"    Unsatisfiable")
            except Exception as e:
                print(f"    Error solving constraints: {e}")
    
    def collect_conditions(self, tree):
        """
        Collect all path conditions from the AST using symbolic execution.
        
        This method traverses the AST to identify all possible execution paths
        through if-else statements and builds path conditions for each path.
        
        Args:
            tree: The AST of the function to analyze
            
        Returns:
            A list of path constraints as Z3-compatible strings
        """
        paths = []
        
        def traverse_if_children(children, context, cond):
            """
            Traverse the children of an if statement and accumulate path conditions.
            
            Args:
                children: Child nodes to traverse
                context: Current path conditions leading to this point
                cond: The condition to add to the context
            """
            previous_len = len(paths)
            for child in children:
                traverse(child, context + [cond])
            # If no paths were added, add the current context as a complete path
            if len(paths) == previous_len:
                paths.append(context + [cond])
        
        def traverse(node, context):
            """
            Recursively traverse the AST and collect path conditions.
            
            Args:
                node: Current AST node
                context: Current path conditions
            """
            if isinstance(node, ast.If):
                # Extract condition and create negation for else branch
                cond = ast.unparse(node.test).strip()
                not_cond = f"z3.Not({cond})"
                
                # Traverse both the if branch (with condition) and else branch (with negation)
                traverse_if_children(node.body, context, cond)
                traverse_if_children(node.orelse, context, not_cond)
            else:
                # Continue traversing child nodes
                for child in ast.iter_child_nodes(node):
                    traverse(child, context)
        
        # Start traversal from the root
        traverse(tree, [])
        
        # Convert collected paths to Z3 constraint strings
        constraints = []
        for path in paths:
            if path:  # Only add non-empty paths
                path_constraints = ", ".join(path)
                constraints.append(f"z3.And({path_constraints})")
        
        return constraints
    
    def check_taint(self, frame, event, arg, code_line):
        """Check whether a tainted variable reached a sink (SQL execution)."""
        if event == "line":
            m = SINK_REGEX.match(code_line)
            if m:
                # Found SQL execution sink
                var_name = m.group(1).strip()
                
                # Check if the variable used in SQL execution is tainted
                if var_name in frame.f_locals:
                    var_id = id(frame.f_locals[var_name])
                    if var_id in self.tainted_variables:
                        # Vulnerability found!
                        self.vulnerable_paths.append({
                            'path': self.current_path.copy(),
                            'input': self.current_input
                        })
    
    def run(self):
        """Run the dynamic taint analysis."""
        
        def tracer(frame, event, arg):
            """Tracer function for dynamic analysis."""
            function_code = frame.f_code
            function_name = function_code.co_name
            lineno = frame.f_lineno
            executed_line = linecache.getline(function_code.co_filename, lineno).rstrip()
            
            # Track execution path
            self.current_path.append(f"{function_name}:{lineno} {executed_line}")
            
            # Check for taint propagation to sinks
            self.check_taint(frame, event, arg, executed_line)
            
            return tracer
        
        # Generate inputs using symbolic execution
        print("[*] Generating inputs using symbolic execution...")
        self.generate_inputs()
        
        print(f"\n[*] Generated {len(self.inputs)} test inputs")
        
        # Fuzz the vulnerable function with generated inputs
        print("\n[*] Fuzzing vulnerable_function with generated inputs...")
        for test_input in self.inputs:
            self.current_path = []
            self.current_input = test_input
            
            print(f"\n[+] Testing Path {test_input['path']} with x={test_input['x']}, y={test_input['y']}")
            
            # Enable tracing
            sys.settrace(tracer)
            
            try:
                # Execute the vulnerable function
                result = vulnerable_function(
                    test_input['query'],
                    test_input['x'],
                    test_input['y']
                )
                print(f"    Result: {result}")
            except Exception as e:
                print(f"    Exception: {e}")
            
            # Disable tracing
            sys.settrace(None)
        
        return self.vulnerable_paths


def main():
    """Main function to run the taint analyzer........"""
    print("=" * 70)
    print("Dynamic Taint Analyzer......")
    print("=" * 70)
    
    analyzer = TaintAnalyzer()
    vulnerable_paths = analyzer.run()
    
    # Report results
    print("\n" + "=" * 70)
    print("ANALYSIS RESULTS")
    print("=" * 70)
    
    if len(vulnerable_paths) > 0:
        print(f"\n\033[95m❌ VULNERABLE: Found {len(vulnerable_paths)} vulnerable path(s)\033[00m\n")
        
        for i, vuln in enumerate(vulnerable_paths):
            print(f"\033[91m[Vulnerability {i + 1}]\033[00m")
            print(f"  Input: query='{vuln['input']['query']}'")
            print(f"         x={vuln['input']['x']}, y={vuln['input']['y']}")
            print(f"  Execution Path:")
            for line in vuln['path']:
                print(f"    \033[94m» {line}\033[00m")
            print()
    else:
        print("\n\033[92m✅ NOT VULNERABLE: No tainted data reached SQL execution sink\033[00m\n")


if __name__ == '__main__':
    main()
