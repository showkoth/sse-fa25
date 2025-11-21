**Case Study (100 points)**

# **Purpose**

The purpose of this case study is to help you demonstrate your understanding of key concepts of the security principles discussed in class.   An investigation of security challenges experienced by a real software product. While in class you will be learning about security principles, common weaknesses, and threat modeling, in the case study you will put those concepts into practice. The final outcome of this assignment is a technical report that includes a threat model.

# **How to Submit it**

- Gradescope

**⏰ Deadline** 

- Nov 21, 2025 11:59 PM 

# **Task**

The case study can be performed in ***pairs,*** **triples, or individually**.  
As a team, choose a ***software project*** to study. This could be a prior project you have developed, or an existing open source project. A project is eligible if:

* Source code is available (if not posted publicly, you are able to share the code of the project under analysis via Gradescope)  
* Project must have at least 1,000 lines of code (excluding comments). You can use [cloc](https://github.com/AlDanial/cloc) to measure this.

*If you wish to study an existing open source project, there is a non-exhaustive list of OSS projects as suggestions. You do not have to select from this list; this is instead a starting point. You’re more than welcome to pick an OSS project outside this list (as long as it fulfills the requirements listed above).*

The purpose of this phase is to provide an overall assessment of the security risks posed by the domain of your case study.  Specifically, your team will be performing the first two steps in the asset-centric threat modeling process in order to address the following questions:

**\- Overview**. A description of the product itself and an overview of the findings of this chapter. Discuss users, purpose, business objectives, development team, process, and any other information that might be relevant to understanding both the project and product.

**\- Identify Product Assets**. A listing and discussion of the product resources, functionality, and intangible properties that an attacker would want to exploit (i.e. the assets). For each asset, collect their id, name, description, and trust levels. Besides that, include an answer to the following questions:

* How might this list of assets change in the future?   
* Are there some that will become obsolete?

**\- Architecture Overview**. Describe the architecture of the system. Please answer the following questions:

* Identify what the application does:  
  * What are the product's software requirements?  
* Identify the application’s components:  
  * What are the subsystems? What does each subsystem do?  
  * Are there subsystems that are expressly security features? (e.g. encryption, authentication) Describe these in more depth.  
  * Consider the cost of developer mistakes in terms of subsystems. For example "if a developer makes a mistake in this subsystem, what happens?"  
  * Do some subsystems appear to be more susceptible to code-level vulnerabilities?  
  * Do you see security built into the system at this architectural level? (e.g. distrustful decomposition)  
  * How might compromising one subsystem affect the security (integrity, reliability, etc) of the others or of the system as a whole?  
  * How does the system’s interaction with external systems put it at risk?  
  * Include a brief discussion on how the architecture might change over time.  
* Identify the technologies being used  
  * Dependencies  
  * Language(s) used to develop the system

**\- Decompose the Application**. Create a security profile for the application based on traditional areas of vulnerability. Identify trust boundaries, data flow, entry points, and privileged code. 

* Document the security profile of the application  
  * What mitigation techniques do the project have in place?   
  * Create a high level data flow diagram for the system.

**\- Identify the Threats**. Follow the systematic process explained in class to list what are the threats that can compromise the project’s assets.

**\- Document the Threats**. Based on the threats identified in the prior step, create a threat model profile. That is, document for each threat:

* ID  
* Name  
* Description  
* Category (STRIDE)  
* Corresponding Entry Points  
* Relevant Assets  
* Mitigation

**\- Rate the Threats**. Follow a systematic approach to rank the threats based on their risk. Use the DREAD model we studied in class to evaluate a threat’s risk. 

**Case Study Scope:** Since the number of threats can be quite large, for the sake of keeping this assignment within a reasonable intellectual challenge, you are required to identify at least **6** threats.

### **Deliverables:**

- `Case Study.pdf`: A PDF with the final report for this case study. This PDF shall include any diagrams in-text. Please use the following formatting:  
  - 10pt font (Arial)  
  - Justified text (no ragged edges)  
  - Tables & Figures must be numbered starting at 1 going through the whole document.  
  - Tables must have their caption be above the table  
  - Figures have their caption below the figure.  
  - Cite URLs by using hyperlinks in the text.  
  - Template:  [FA24 Case Study Report Template](https://docs.google.com/document/d/1kcWSEQo4leYs2L3p3PPuGDcvNXoJqbCCBrzB_dVQ0fg/edit#heading=h.no53hhaok57a) ( All sections listed in the template are required to be included.

## **Case Study Ideas**

Below is a list of widely used open source projects. This list is not exhaustive, and it is intended to give you ideas on possible projects that you could study. You are, however, welcome to find another project of your own choosing. The [OpenHub website](https://www.openhub.net/) can be useful in finding OSS projects and their metadata (ie., repository URL, project website, etc).

### **🤔 Hints/FAQs:** 

If you choose to study an existing open source project, Inferring the architecture for the system can be a real challenge if the project is not well-documented. Here are a few places you can look for hints on what the subsystems are: 

* Bugs. Any custom fields, or what is mentioned in discussions.  
* File system layout (packages/folders/module names).  
* Javadoc or other documentation.  
* API documentation for third-party developers can describe the subsystem layout.  
- The [OpenHub website](https://www.openhub.net/) can be useful in finding OSS projects and their metadata (ie., repository URL, project website, etc). See the “Case Study Ideas”  in the end of this document for a non-exhaustive list of OSS projects.

Tomcat  
MySQL  
PostGreSQL  
Linux kernel  
PHP  
Ruby  
Ruby on Rails  
Hibernate  
Wireshark  
Wordpress  
Firefox  
Chromium  
Drupal  
MediaWiki  
Apache httpd  
Android  
Java  
X Windows  
Gnome  
KDE  
Thunderbird  
PHPMyAdmin  
RT  
Django  
OpenSSL  
VLC  
Samba  
Quagga  
Joomla  
GLibC  
OpenMRS  
Pidgin

# **Grading Rubric**

The assignment will be evaluated based on the following criteria:

* **5pt** Project matches the minimum criteria  
  * **10pts** Overview  
  * **15pts** Identify Product Assets  
  * **20pts** Architecture Overview  
  * **10pts** Application Decomposition  
  * **30pts** Threats Identification & Documentation   
  * **10pts** Threats Rating

