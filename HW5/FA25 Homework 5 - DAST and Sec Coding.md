**Homework \#5 (10 points)**

# **Purpose**

The purpose of this assignment is to help you demonstrate your understanding of Secure Coding and Dynamic Application Security Testing. This assignment will help prepare you for developing dynamic analyzers for finding vulnerabilities in programs written in Python. 

# **Task**

## **Machine Requirements:** 

This homework requires that you have [Python 3.9+](https://www.python.org/downloads/) and [z3](https://github.com/Z3Prover/z3#python) installed on your machine. To install z3, you can use the following command (assuming you have pip installed):  
`pip install z3-solver`

**Notice**: if you have multiple python versions installed, make sure you are using the right alias for the pip command (that is, the pip version that will install to the python version you are going to use for the Homework. As an example, I use python3.9 to execute my scripts, so I use pip3.9 to install dependencies).

## **Part 1: Conceptual Questions**

* **Q1:** Is the regular expression below safe to be used? If not, what is the problem with it?


| `<html>.*?<head>.*?<title>.*?</title>.*?</head>.*?<body[^>]*>.*?</body>.*?</html>` |
| :---- |


* **Q2:** Suppose that **x** and **y** in the following program are symbolic. When the symbolic executor reaches the line that prints "everywhere" what will the path condition be?

| /\* assume x and y are both symbolic \*/ void foo(int x, int y) {  if (x \> 5) {    if (y \> 7) {      printf("here\\n");    } else {      if (x \< 20)        printf("everywhere\\n");      else        printf("nowhere\\n");    }  } } |
| :---- |

## **Part 2: Implementation**

* What you need for this homework is in the folder HW5 in the course repository.  
* **Q1:** Implement in Python a dynamic taint analyzer to analyze vulnerable\_function within HW5/vuln.py :  
  * it will generate the values for **x** and **y** based on symbolic execution and constraint solving.  
  * It will fuzz the vulnerable\_function with these values in order to find and report  the vulnerable path and its corresponding input.

## **🤔 Hints/FAQs:** 

- For Part2-Q1 you can use the taint\_anlyzer script shown in class as a starting point. The areas that would need to be changed are:  
  - Input generation for x and y would be based on conditions collected via AST parsing (this was also demonstrated in class)  
    - For the string input value (ie. query parameter) you can hardcode that input to a valid SQL command (e.g.: "select \* from users")  
  - The sink is now the statement that executes the SQL query

# **Grading Rubric**

The HW will be evaluated based on the following criteria:

| Part 1 3 pts  | \- Do the answers correctly define and/or explain concepts? |
| :---- | :---- |
| **Part 2** 7 pts  | \- Is the implemented solution correctly performing dynamic taint analysis? \- Is the code free from runtime errors? |

