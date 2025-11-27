import ast
import inspect
import linecache
import re
import sys
import z3
from vuln import vulnerable_function

# Regex to detect the sink (cursor.execute)
SINK_REGEX = re.compile(r".*cursor\.execute\((.*)\)")

def collect_conditions(tree):
    paths = []

    def traverse_if_children(children, context, cond):
        previous_len = len(paths)
        for child in children:
            traverse(child, context + [cond])
        # If no paths were added by children (e.g. leaf nodes or no children), add the current context
        if len(paths) == previous_len:
            paths.append(context + [cond])

    def traverse(node, context):
        if isinstance(node, ast.If):
            cond = ast.unparse(node.test).strip()
            not_cond = f"z3.Not({cond})"
            traverse_if_children(node.body, context, cond)
            traverse_if_children(node.orelse, context, not_cond)
        else:
            for child in ast.iter_child_nodes(node):
                traverse(child, context)

    traverse(tree, [])
    return paths

class TaintAnalyzer:
    def __init__(self):
        self.tainted_variables = set()
        self.vulnerable_paths = []
        self.current_path = []

    def mark_as_tainted(self, var):
        self.tainted_variables.add(id(var))

    def check_taint(self, frame, event, arg, code_line):
        if event == "line":
            m = SINK_REGEX.match(code_line)
            if m:
                # Extract variable name from the sink call
                # This is a simple regex and might fail on complex expressions, 
                # but for this homework it should suffice.
                arg_str = m.group(1).strip()
                
                # We need to evaluate or find the object referred to by arg_str
                # Since it's likely a variable name, we check locals.
                if arg_str in frame.f_locals:
                    var_obj = frame.f_locals[arg_str]
                    if id(var_obj) in self.tainted_variables:
                        # Found a tainted sink!
                        self.vulnerable_paths.append(list(self.current_path))

    def tracer(self, frame, event, arg):
        function_code = frame.f_code
        function_name = function_code.co_name
        
        # We only care about tracing inside vulnerable_function
        if function_name != "vulnerable_function":
            return self.tracer

        lineno = frame.f_lineno
        filename = function_code.co_filename
        executed_line = linecache.getline(filename, lineno).strip()
        
        # Capture variable values for the trace log
        # We filter out internal python vars
        variable_values = ", ".join([f"{name}={frame.f_locals[name]}" for name in frame.f_locals if not name.startswith('_')])
        
        trace_entry = f"{function_name}:{lineno} {executed_line} ({variable_values})"
        self.current_path.append(trace_entry)
        
        self.check_taint(frame, event, arg, executed_line)
        return self.tracer

    def solve_path_constraint(self, constraints):
        x = z3.Int('x')
        y = z3.Int('y')
        solver = z3.Solver()
        
        for cond in constraints:
            try:
                # Evaluate the condition string to a Z3 expression
                # We pass x, y, and z3 to the context
                c = eval(cond, {"x": x, "y": y, "z3": z3})
                solver.add(c)
            except Exception as e:
                # print(f"Error parsing condition '{cond}': {e}")
                return None
        
        if solver.check() == z3.sat:
            model = solver.model()
            return (model[x].as_long(), model[y].as_long())
        else:
            return None

    def run(self):
        print("======================================================================")
        print("Dynamic Taint Analyzer - HW5")
        print("======================================================================")
        print("[*] Generating inputs using symbolic execution...")

        # 1. Get AST and paths
        source = inspect.getsource(vulnerable_function)
        tree = ast.parse(source)
        # Find the FunctionDef node
        func_node = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
        
        paths = collect_conditions(func_node)
        
        print(f"[*] Found {len(paths)} paths in vulnerable_function.")
        
        for i, path_conditions in enumerate(paths):
            print(f"\n[*] Analyzing Path {i+1}: {path_conditions}")
            
            # 2. Solve constraints
            solution = self.solve_path_constraint(path_conditions)
            
            if solution:
                x_val, y_val = solution
                print(f"    [+] Satisfiable! Inputs: x={x_val}, y={y_val}")
                
                # 3. Fuzz/Trace
                query = "SELECT * FROM users" # Hardcoded valid SQL
                
                # Reset state for this run
                self.current_path = []
                self.tainted_variables = set()
                self.mark_as_tainted(query)
                
                print(f"    [+] Fuzzing with inputs...")
                sys.settrace(self.tracer)
                try:
                    vulnerable_function(query, x_val, y_val)
                except Exception as e:
                    print(f"    [!] Exception during execution: {e}")
                finally:
                    sys.settrace(None)
                    
            else:
                print(f"    [-] Unsatisfiable.")
                
        return self.vulnerable_paths

if __name__ == '__main__':
    analyzer = TaintAnalyzer()
    vuln_paths = analyzer.run()
    
    print("\n======================================================================")
    if len(vuln_paths) > 0:
        print(f"\033[95m Vulnerable Paths Found: {len(vuln_paths)}\033[00m")
        for i, path in enumerate(vuln_paths):
            print(f"\033[91m\tPath {i + 1}\033[00m")
            for line in path:
                print(f"\033[94m\t\t» {line}\033[00m")
    else:
        print("\033[92m Not vulnerable\033[00m")
