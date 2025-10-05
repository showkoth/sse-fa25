

## **Part 1: Fixing Issues from HW2**

In HW2, you played the role of a *software consultant* hired to identify the security vulnerabilities in a Web application. In this homework, you will now play the role of the *software developer* that will fix the identified security vulnerabilities. 

* **Q1:** Change the code provided to fix ~~all~~ ***at least two*** of the vulnerabilities you found in the web application.   
* **Q2:** Include in the code comments with an explanation about the fix. 

## **Part 2: Identification of Threats**

| Trust Levels |  |  |
| :---: | ----- | ----- |
| **ID** | **Name** | **Description** |
| 1 | Anonymous Web User | A user who has connected to the website but has not provided valid credentials. |
| 2 | User with Valid Login Credentials | A user who has connected to the website and has logged in using valid login credentials. |
| 3 | User with Invalid Login Credentials | A user who has connected to the website and is attempting to log in using invalid login credentials. |
| 4 | Website Administrator | The Website administrator can configure the website. |

| Assets |  |  |  |
| :---: | :---: | ----- | :---- |
| ID | Name | Description | Trust Levels |
| 1.1 | User Login Details | The login credentials that a user has to log into the website. | (2) User with Valid Login Credentials(4) Website Administrator  |
| 1.2 | Task Details | The task details stored by the database. | (1) Anonymous Web User (2) User with Valid Login Credentials (3) User with Invalid Login Credentials (4) Website Administrator |

| Entrypoints |  |  |  |
| :---: | :---: | :---: | ----- |
| **ID** | **Name** | **Description** | **Trust Levels** |
| 1.1 | Index Page | The index page for the website is the entry point for all users. | (1) Anonymous Web User (2) User with Valid Login Credentials (3) User with Invalid Login Credentials (4) Website Administrator |
| 1.2 | Add task page | The page where users can add tasks. | (2) User with Valid Login Credentials (4) Website Administrator |
| 1.3 | Login page | The login function accepts user supplied credentials and compares them with those in the database. | (2) User with Valid Login Credentials(3) User with Invalid Login Credentials (4) Website Administrator |
| 1.4 | Delete task page | The page used to delete a task. | (2) User with Valid Login Credentials (4) Website Administrator |

**Q1**) Consider that we have the (simplified) list of entry points, trust levels, and assets above for the application provided in the HW2 as shown in the tables above. Write down 1 threat for this application using the threat model profile shown in class:

| ID | *Answer* |
| :---- | :---- |
| **Name** | *Answer* |
| **Description** | *Answer* |
| **STRIDE Classification** | *Answer* |
| **Mitigated?** | *Answer* |
| **Known Mitigations** | *Answer* |
| **Entry Points** | *Answer* |
| **Assets** | *Answer* |

**Q2**) Create a data flow diagram for ***one feature of your choice*** of the HW2’s application.

## **Part 3: Research Synthesis** 

Graduate students are expected to have evidence of *research synthesis* during the semester. To fulfill this requirement, please read the following paper and answer the questions below:  
Mai, Phu X., et al. "Modeling security and privacy requirements: a use case-driven approach." Information and Software Technology 100 (2018): 165-182.

1) **Summarize the lessons learned while the authors  applied their approach to an industrial healthcare project and from the interviews with engineers.**

   *Answer will be roughly 1 page in length.*

# **Grading Rubric**

The HW will be evaluated based on the following criteria:

| Part 1  4.5 pts / CSE60770 | Is the implemented solution correctly fixing the identified vulnerabilities? Is the code free from runtime errors? |
| :---- | :---- |
| **Part 2**  4.5 pts / CSE60770 | Are the question answers showing applicable security threats? Is the diagram using the DFD notation shown in class? Is the DFD depicting correct data flows? |
| **Part 3**  1 pt / CSE60770 | Are the questions answered with enough detail? |

