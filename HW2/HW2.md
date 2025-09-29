**Homework \#2 (10 points)**

# **Purpose**

The purpose of this individual assignment is to help you demonstrate your understanding of software weaknesses in web applications. This assignment will help prepare you for finding and fixing vulnerabilities in Web applications written using Python. 

# **How to Submit it**

Upload your deliverables on Gradescope.   
You can zip all the files and upload the zip file (Gradescope will automatically extract the files upon submission).  
*If there is any large file in the submission, gradescope throws an error message. Please remove any large file prior to submission.*  
*If the error persists, please contact the instructor and TA immediately (attach your submission to the e-mail or share it is a Google Drive link).* 

## **Deliverables**

* A PDF file with your answers to the conceptual questions in **Part 1**, **Part 2** and **Part 4** (it can be a combined PDF or a separate PDF for each part). **PDF file only** (do not upload in other format).  
* The source code for the password cracking you implemented in **Part 3**  
  * If you’re using pipenv/virtualenv, make sure to ***not*** include the hidden folders with all the binaries for Python libraries (that would make the zip file too large for Gradescope to accept).

  When submitting to gradescope, create a **\*ZIP\*** file and then upload this file to it.

    **DO NOT use another compression format (ex: rar, tar, etc)**

# 

# **Task**

## **Machine Requirements:** 

* This homework requires that you have [Python](https://www.python.org/) and [Django](https://docs.djangoproject.com/en/4.0/intro/install/) installed on your machine. *(The code has been developed and tested using Django v3.1.13. It should work just fine on v4.x too)*.  
* Running the code:   
1. Clone the course repository   
2. “cd” into the folder that has the source code for the Django web application

   `cd HW2/website` 

3. Run the web application using:

   `python manage.py runserver` (in your machine, it might be python3.x)

4. Access [http://localhost:8000/tasktracker/](http://localhost:8000/tasktracker/) in your web browser  
   1. It will redirect you to a login page. There are three accounts created:

      **Username**: `user1` / **Password**: `p*2sfHQP==` 

      **Username**: `user2` / **Password**: `V?vZT+MD4e`

*If there are no issues with your environment, you’d be able to access the task tracker app.*

## **Part 1: Conceptual Questions**

* **Q1:** Read [Django’s documentation](https://docs.djangoproject.com/en/4.0/ref/csrf/) and answer the following question:   
  * What is the purpose of `{% csrf_token %}` in the template files?   
* **Q2:** What could happen if a developer forgets to add the `{% csrf_token %}` tag on their template that uses an HTML form?  
* **Q3:** What is the CWE ID associated with the security problem that arises with forgetting to use `{% csrf_token %}`?

## **Part 2: Finding Issues**

In this homework part, you will play the role of a ***software consultant*** hired to identify the security vulnerabilities in a Web application. This is a simple Web application where a user can add/delete/lists tasks (i.e., a task management app). In light of that, answer the following question:

* **Q1:** Enumerate all the vulnerabilities you found in the web application. Include in your answer the following:  
  * Where they are located in the code  
  * How to exploit it  
  * The corresponding CWE-ID (i.e., vulnerability type)

### **Answer to Q1:**

After analyzing the web application code, I identified the following 4 critical security vulnerabilities:

#### **Vulnerability 1: SQL Injection**
- **Location**: `tasktracker/views.py`, line 31 in the `add()` function
- **Code**: 
  ```python
  cursor.executescript(f"INSERT INTO tasktracker_task(user_id, status, due_date, title) VALUES ({request.user.id},'{status}', '{due_date}', '{title}')")
  ```
- **How to exploit**: An attacker can inject malicious SQL code through the `title`, `due_date`, or `status` fields. For example, setting the title to `'; DROP TABLE tasktracker_task; --` would delete the entire task table.
- **CWE-ID**: CWE-89 (SQL Injection)

#### **Vulnerability 2: Cross-Site Scripting (XSS)**
- **Location**: `tasktracker/templates/index.html`, line 12
- **Code**: 
  ```html
  <b>Task #{{t.id}}: {{t.title | safe}}</b>
  ```
- **How to exploit**: The `safe` filter disables Django's automatic HTML escaping, allowing stored XSS attacks. An attacker can create a task with a malicious title like `<script>alert('XSS')</script>` or `<img src=x onerror=alert('XSS')>` which will execute when other users view the task list.
- **CWE-ID**: CWE-79 (Cross-Site Scripting)

#### **Vulnerability 3: Insecure Direct Object Reference (IDOR)**
- **Location**: `tasktracker/views.py`, lines 38-42 in the `delete()` function
- **Code**: 
  ```python
  def delete(request, pk):
      task = Task.objects.get(id = pk)
      task.delete()
      return HttpResponseRedirect(reverse(f'tasktracker:index'))
  ```
- **How to exploit**: The function doesn't verify that the task belongs to the authenticated user. An attacker can delete any task by changing the `pk` parameter in the URL (e.g., `/tasktracker/delete/1/`, `/tasktracker/delete/2/`, etc.) to access and delete other users' tasks.
- **CWE-ID**: CWE-639 (Authorization Bypass Through User-Controlled Key)

#### **Vulnerability 4: Information Disclosure - Hard-coded Secret Key**
- **Location**: `website/settings.py`, line 23
- **Code**: 
  ```python
  SECRET_KEY = '#n6kks0cs$a-7k*67)k(nof$7z6&l+u97ea)nl_r8frg_mrmd1'
  ```
- **How to exploit**: The Django secret key is hard-coded in the source code and exposed in version control. This key is used for cryptographic signing of session data, CSRF tokens, and password reset tokens. An attacker with access to this key can forge session cookies, bypass CSRF protection, and potentially compromise user accounts.
- **CWE-ID**: CWE-798 (Use of Hard-coded Credentials)

## **Part 3: Cracking Passwords**

Now, you will play the role of a ***hacker*** that will try to brute force leaked hashed passwords. The repository has three files with 30 passwords each that were hashed using **MD5**. 

* **Q1:** Write a Python script that tries to guess these passwords. You can safely assume that:  
  * Passwords have at least 3 characters and up to 6 characters.  
  * Valid password characters are all letters in the alphabet (`a-z` and `A-Z`), digits (`0-9`) and the following special characters:  
    * ampersand: `&`  
    * at: `@`  
    * pound sign (aka hashtag): `#`  
  * The script will produce a list of passwords that it correctly guessed in a text file (`cracked_passwords.txt`). For example, if you were able to guess 3 passwords, your output would be:

| cracked\_passwords.txt |
| :---- |
| Crackedpass1 Crackedpass2 crackedpass3 |

## **Part 4: Research Synthesis** 

Graduate students are expected to have evidence of *research synthesis* during the semester. To fulfill this requirement, please read the following paper and answer the questions below:  
[Pythia: Identifying Dangerous Data-flows in Django-based Applications](https://dimitro.gr/assets/papers/GDTM19.pdf) 

1) **What is the motivation and problem being tackled by this paper and how they solve this problem?**

   *Answer will be 2-3 paragraphs in length.*

2) **Would Pythia help you in finding the vulnerabilities you identified in Part 2?** 

   *The answer will be **at least** half a page, explaining in details how Pythia could have helped you in finding vulnerabilities in Part 2\. In case you think the tool could not help you, explain in details why it is the case (i.e., what is it on this tool that makes it unsuitable to find the vulnerabilities you have found).* 

## **🤔 Hints/FAQs:** 

- For password cracking, you can use:  
  - Hashlib module to compute hashes (the repo has an example on how to do that)  
  - Rainbow tables that you found on online sources  
- Use the OWASP Top 10 list as a “checklist” for issues to look for in the code.  
  - 4 vulnerabilities were intentionally added

# **Grading Rubric**

The HW will be evaluated based on the following criteria:

| Part 1 1 pt / CSE60770 | Are the answers correctly explaining the CSRF\_TOKEN? Is the answer pinpointing the correct CWE? |
| :---- | :---- |
| **Part 2** 4 pts / CSE60770 | Does it correctly pinpoint at least 4 vulnerabilities? |
| **Part 3** 4 pts / CSE60770 | Is the implemented solution correctly guessing passwords? Is the code free from runtime errors? Is the solution finding: At least 60 passwords out of the 90 passwords provided |
| **Part 4** 1 pt / CSE60770 | Are the questions well answered with enough detail? |