import requests
from bs4 import BeautifulSoup

# Send a GET request to the webpage
url = "https://www.google.com/search?q=backend+developer+&ibp=htl;jobs&hl=en&gl=us#fpstate=tldetail&htivrt=jobs&htichips=date_posted:week&htischips=date_posted;week&htidocid=zx28E_hOH7GZhMkLAAAAAA%3D%3D"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all job listings (example, you need to inspect the webpage to find the correct CSS selectors or structure)
job_description = soup.find_all("span", class_="HBvzbc")

if job_description:
    print(job_description.text.strip())
