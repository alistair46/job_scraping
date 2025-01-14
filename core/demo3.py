import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def fetch_job_data(job_position, years_of_experience, location_preferred):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    # Dynamically build the URL with user input
    url = (
        f"https://www.timesjobs.com/candidate/job-search.html?"
        f"searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&"
        f"txtKeywords={job_position}&cboWorkExp1={years_of_experience}&txtLocation={location_preferred}"
    )

    print(f"Fetching data from URL: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return 

    soup = BeautifulSoup(response.text, 'lxml')

    # Extract total number of openings
    total_openings = soup.find('span', class_="totolResultCountsIdLink")
    total_openings_text = total_openings.text.strip() if total_openings else "Not specified"

    # Find all job entries
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    job_data = []

    for job in tqdm(jobs):
        # Extract and clean job details
        data_posted = job.find("span", class_='sim-posted')
        company_name = job.find("h3", class_='joblist-comp-name')
        skills = job.find("div", class_='srp-skills')
        location = job.find("li", class_='srp-zindex location-tru')
        experience_required = job.find('i', class_='srp-icons experience')

        job_data.append({
            "Company Name": company_name.text.strip() if company_name else "Not specified",
            "Skills Required": skills.text.strip() if skills else "Not specified",
            "Location": location.text.strip() if location else "Not specified",
            "Date Posted": data_posted.text.strip() if data_posted else "Not specified",
            "Experience Required": experience_required.text.strip() if experience_required else "Not specified",
        })

    # Convert the job data into a DataFrame
    return pd.DataFrame(job_data), total_openings_text


def export_to_excel(dataframe, file_name):

    dataframe.to_excel(file_name, index=False)
    print(f"Job data exported to '{file_name}'")


def main():
    # Collect user input
    job_position = input("Enter job position: ").strip()
    years_of_experience = int(input("How many years of experience do you have? "))
    location_preferred = input("Preferred Location: ").strip()

# FIXME:
    # Fetch job data
    job_data, total_openings = fetch_job_data(job_position, years_of_experience, location_preferred)

    if job_data is not None and not job_data.empty:
        # Export data to Excel
        file_name = f"{job_position}_{location_preferred}.xlsx".replace(" ", "_")
        export_to_excel(job_data, file_name)
        
        print(f"Number of job openings: {total_openings}")
    else:
        print("No jobs found for the given criteria.")


# Entry point for the script
if __name__ == "__main__":
    main()
