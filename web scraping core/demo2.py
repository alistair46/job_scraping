import requests
from bs4 import BeautifulSoup
import pandas as pd

job_data=[]

# Set the headers to mimic a browser
Job_Position=input(str("Enter job Position: "))
Years_of_experience=int(input("How many year  of experence you have? "))
Location_preferred=input(str("Preferred Location: "))


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Dynamically build the URL with user input
url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords={Job_Position}&cboWorkExp1={Years_of_experience}&txtLocation={Location_preferred}"

print(f"Fetching data from URL: {url}")

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Find all job entries
    No_of_openings_found=soup.find('span',class_="totolResultCountsIdLink")
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    
    for i in jobs:
        # Extract job details with error handling
        
        data_posted = i.find("span", class_='sim-posted')
        company_name = i.find("h3", class_='joblist-comp-name')
        skills = i.find("div", class_='srp-skills')
        location=i.find("li", class_='srp-zindex location-tru')
        No_of_experence_needed=i.find('i',class_='srp-icons experience')

        # Convert elements to text if they exist, otherwise set a default value
        data_posted_text = data_posted.text.strip() if data_posted else "Not specified"
        company_name_text = company_name.text.strip() if company_name else "Not specified"
        skills_text = skills.text.strip().split() if skills else "Not specified"
        location_text=location.text.strip().split() if location else "Not specified"
        No_of_experence_needed=No_of_experence_needed.text.strip if No_of_experence_needed else "Not specified"

        job_data.append({
            "Company Name": company_name_text,
            "Skills Required": skills_text,
            "Location": location_text,
            "Date Posted": data_posted_text,
            "Experence Required": No_of_experence_needed,
        })

    # Create a DataFrame from the list
    df = pd.DataFrame(job_data)
    
    # Export DataFrame to Excel
    file_name = f"{Job_Position}_{Location_preferred}.xlsx"
    df.to_excel(file_name, index=False)
    print(f"Job data exported to '{file_name}'")

    print(f"No of opening : {No_of_openings_found}")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
