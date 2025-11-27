# HW5 Part 2: Dynamic Taint Analyzer

## Overview
This implementation performs dynamic taint analysis on `vulnerable_function` in `vuln.py` to detect SQL injection vulnerabilities.

## Implementation Details

### Key Components

1. **Symbolic Execution for Input Generation**
   - Uses AST parsing to extract path conditions from the vulnerable function
   - Employs Z3 solver to generate concrete values for `x` and `y` that satisfy each path
   - Creates test inputs combining Z3-generated values with SQL injection payloads

2. **Dynamic Taint Analysis**
   - Marks the SQL query parameter as tainted (source)
   - Traces execution using `sys.settrace()`
   - Monitors when tainted data reaches the SQL execution sink (`cursor.execute()`)

3. **Vulnerability Detection**
   - Identifies the vulnerable path: `x + y > 100` AND `x - y < 10`
   - Reports the exact execution path and input values that trigger the vulnerability

## How to Run

```bash
cd HW5
python dynamic_taint_analyzer.py
```

## Requirements

- Python 3.9+
- z3-solver (`pip install z3-solver`)

## Output

The analyzer will:
1. Generate test inputs using symbolic execution
2. Fuzz the vulnerable function with these inputs
3. Report any vulnerable paths where tainted SQL queries are executed

## Example Output

```
======================================================================
Dynamic Taint Analyzer - HW5 Part 2
======================================================================
[*] Generating inputs using symbolic execution...

[*] Solving Path 1: z3.And(x + y > 100, x - y < 10)
    ✓ Solution found: x=0, y=101

[*] Generated 3 test inputs

[*] Fuzzing vulnerable_function with generated inputs...

[+] Testing Path 1 with x=0, y=101
    Result: (1, 'admin', 'admin_pass')

======================================================================
ANALYSIS RESULTS
======================================================================

❌ VULNERABLE: Found 1 vulnerable path(s)

[Vulnerability 1]
  Input: query='SELECT * FROM users WHERE username = 'admin' OR '1'='1' --'
         x=0, y=101
  Execution Path:
    » vulnerable_function:19     if x + y > 100:
    » vulnerable_function:20         if x - y < 10:
    » vulnerable_function:21             cursor.execute(query)
```

## Vulnerability Analysis

The vulnerable path occurs when:
- `x + y > 100` (first condition is true)
- `x - y < 10` (second condition is true)

With these conditions satisfied, the SQL query parameter is executed directly without sanitization, allowing SQL injection attacks.
