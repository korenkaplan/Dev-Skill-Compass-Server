![Dev-Skill-Compass-Server](https://socialify.git.ci/korenkaplan/Dev-Skill-Compass-Server/image?description=1&descriptionEditable=Server%20Repository%20for%20the%20website%20%22Skills%20Compass%22&font=Raleway&logo=https%3A%2F%2Fgithub.com%2Fkorenkaplan%2FDev-Skill-Compass-Server%2Fassets%2F99595036%2F220c6218-77e6-4ab3-b44b-abc3744635d0&name=1&owner=1&pattern=Charlie%20Brown&theme=Light)


# 🌟 Welcome to "Skills-Compass"
 Our mission is to guide you on the most in-demand technologies in Israel's tech job market. We help you stay relevant by providing the latest information on the skills you need for different tech roles.
 
 🌍 **What Makes Us Unique:**

 Every day, our system scans the latest job postings online, ensuring that our data is the freshest and most accurate, especially for jobs in Israel. This way, you get real-time insights into what employers are looking for.

🔮 **What's Coming Next:**

🚀 Exciting things are on the horizon! We're planning to add more job roles, highlight emerging and declining tech trends, and provide even more data to help you navigate the job market with confidence.

#### Website: https://skills-compass.netlify.app/
[![LinkedIn](https://img.shields.io/badge/LinkedIn-My%20Profile-blue?logo=linkedin)](https://www.linkedin.com/in/koren-kaplan/)

[![GitHub](https://img.shields.io/badge/GitHub-Frontend%20Repository-black?logo=github)](https://github.com/korenkaplan/skills_compass_react.git)
## Table of Contents

- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [How It Works?](#-how-it-works)
- [Screenshots](#-screenshots)
- [Contact Information](#-contact-information)
- [License](#-license)

## 🔰 Features

- Automated daily scanning of job postings on the internet.
- Text analysis and extraction of tech keywords from job descriptions.
- Aggregation and categorization of data.
- Visualization of in-demand skills categorized by tech roles.
## 👨‍💻 Technologies Used
- Server: Django (hosted on Render)
- Database: PostgreSQL (hosted on Neon)
- Frontend: React Vite (hosted on Netlify)
- Programming Language: Python 3.12.3
- Packages Management: Poetry
## 🏗️ Project Structure
- **Django Apps:**
    - **/core:** Base models for the project database.
    - **/usage_stats:** Advanced models for database usage statistics.
- **/init_db:** Scripts for database initialization.
- **/logic:** Business logic modules.
    - **/web_scraping:** Logic and modules for data scraping.
    - **/text_analysis:** Modules for analyzing job description texts.
    - **/data_processing:** Logic for processing keywords and grouping them.
- **/templates:** HTML templates used in the project.
- **/tmp/django_cache:** Server cache storage.
- **/utils:** Global configurations and settings.
    - **/mail_module:** SMTP configuration for email.
## ❓ How It Works?

### ✅ Data Reliability

<details>
  <summary><h4>How do you avoid collecting data from the same listings on different sites?</h4></summary>
  
  We gather job listings from aggregator sites that collect postings from various sources. To ensure comprehensive coverage, we also check individual job sites directly. If a listing is already collected from another source, we skip it to avoid duplicates.
</details>

<details>
  <summary><h4>How do you avoid collecting the same listing every day?</h4></summary>
  
  Our system scans job listings every 24 hours, focusing on posts from the past day. This method ensures we don't collect the same listing on different days.
</details>

<details>
  <summary><h4>How do you handle duplication of listings within the same list?</h4></summary>
  
  We compare company names, locations, and job titles to identify and skip duplicate listings during our scanning process.
</details>

<details>
  <summary><h4>How do you filter out non-relevant listings?</h4></summary>
  
  We analyze job titles to ensure they match the desired role. For example, we filter out listings like "Full-stack Developer" in a search for "Backend Developer."
</details>


### 🔎 Text Analysis and Data Aggregation

<details>
  <summary><h4>How do you extract relevant words from a text?</h4></summary>
  
  We use a dataset of technological keywords to identify and extract relevant terms from job descriptions.
</details>

<details>
  <summary><h4>How do you handle different spellings and synonyms of the same technology?</h4></summary>
  
  We group synonyms and different spellings, like [node.js, node, nodeJs], into a single category during our data aggregation process.
</details>

<details>
  <summary><h4>How do you count the appearance of tech keywords in a single job description?</h4></summary>
  
  We use a Set data structure to count each technology's appearance uniquely, regardless of how many times it appears in the text.
</details>

<details>
  <summary><h4>How do you count the same keyword for different roles?</h4></summary>
  
  We maintain separate counts of each technology for each role. When scanning job listings, we specify the role related to those postings, ensuring the counts are associated with the correct role.
</details>

## 📸 Screenshots
#### Website: https://skills-compass.netlify.app/
![image](https://github.com/korenkaplan/Dev-Skill-Compass-Server/assets/99595036/edefb6eb-78e2-407a-b0cd-55656d1caa42)

![image](https://github.com/korenkaplan/Dev-Skill-Compass-Server/assets/99595036/ba0f1a2b-9742-42fe-8253-34726a7fff80)


![image](https://github.com/korenkaplan/Dev-Skill-Compass-Server/assets/99595036/51b5ca1a-e5dc-4270-ab32-be683e3b54c2)


![image](https://github.com/korenkaplan/Dev-Skill-Compass-Server/assets/99595036/23d0e416-0b34-4c5b-b682-c5c8e5a6c9bc)

![image](https://github.com/korenkaplan/Dev-Skill-Compass-Server/assets/99595036/709c3a46-577c-4978-9485-a2be8c28d277)

![image](https://github.com/korenkaplan/Dev-Skill-Compass-Server/assets/99595036/4d7c2897-c2da-4612-a2f0-b03fdc5a2a77)


## Contact Information

- LinkedIn: [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/your-linkedin-profile)
- GitHub: [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/korenkaplan)
## 📜 License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) License.

### You are free to:
- **Share** — copy and redistribute the material in any medium or format.

The licensor cannot revoke these freedoms as long as you follow the license terms.

### Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, or build upon the material, you may not distribute the modified material.
- **No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

### Notices:
- You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.
- **No warranties are given.** The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.

For more details, see the [LICENSE](./LICENSE) file.
