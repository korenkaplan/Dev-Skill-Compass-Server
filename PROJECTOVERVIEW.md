**Skills Compass** is an innovative project designed to provide real-time insights into the most in-demand skills and technologies within Israel's tech job market. This tool is aimed at helping developers, data analysts, QA engineers, and other tech professionals stay updated on the latest industry trends and requirements.

#### Key Features:
- **🔍 Automated Job Scraping**: Daily scraping of job postings from multiple sources, including LinkedIn and Google Jobs.
- **🧠 Text Analysis**: Extraction and processing of tech-related keywords from job descriptions using regular expressions and a predefined dataset of technological terms.
- **📊 Data Aggregation**: Categorization and visualization of the extracted data to showcase in-demand skills for various tech roles.
- **🧩 Synonym Handling**: Grouping different spellings and synonyms of the same technology (e.g., node.js, node, nodeJs) to ensure accurate representation of the data.
- **🎯 Role-Specific Data**: Separate tracking of keyword appearances for different roles to provide targeted insights.

#### Project Structure:
- **🔙 Backend**: 
  - **Django**: The backend server is built using Django, hosted on Render.
  - **PostgreSQL**: The database is hosted on Neon.
  - **Modules**:
    - **🌐 Web Scraping**: Collects job postings using BeautifulSoup and Selenium.
    - **🔎 Text Analysis**: Cleans and extracts keywords from job descriptions.
    - **⚙️ Data Processing**: Aggregates and processes the extracted data.
- **🔜 Frontend**:
  - **React Vite**: The frontend application, hosted on Netlify, provides a user-friendly interface for accessing the insights.
- **⚙️ Additional Technologies**:
  - **Python 3.12.3**: The primary programming language used.
  - **Poetry**: For package management and dependency resolution.

#### Workflow:
1. **🗂️ Data Collection**: Job postings are scraped daily from various sources.
2. **🧹 Data Cleaning**: Regular expressions are used to clean and standardize job description texts.
3. **📝 Keyword Extraction**: Relevant tech keywords are extracted from the cleaned texts.
4. **🔄 Aggregation and Analysis**: The extracted keywords are aggregated, and synonyms are grouped together.
5. **📈 Visualization**: The aggregated data is visualized on the frontend, allowing users to see the most in-demand skills for different tech roles.

#### Challenges and Solutions:
- **⚖️ Handling Synonyms**: Different spellings and synonyms are grouped into a single category using a table of synonyms linked to a technology.
- **🚫 Avoiding Duplicates**: Job listings are compared based on company names, locations, and job titles to skip duplicates.
- **🚦 Filtering Non-Relevant Listings**: Job titles are analyzed to ensure they match the desired roles, filtering out irrelevant postings.

Skills Compass aims to be a comprehensive tool for tech professionals in Israel, providing up-to-date insights to help them stay relevant and competitive in the job market.
