import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def fetch_job_data(job_position, years_of_experience, location_preferred):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    url = (f"https://www.foundit.in/srp/results?query=%22Python+Developer+Fresher%22&locations=pune&experienceRanges=0%7E0&experience=0&searchId=32ef2432-f615-4824-9c30-6a7153ab603d")
    print(f"Fetching data from URL: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract job cards
    job_cards = soup.find_all('span', class_='jobCompanyCard')
    if not job_cards:
        print("No job cards found.")
        return None, None

    job_data = []
    for job in tqdm(job_cards):
        # Extracting job details
        title = job.find("span", class_='jobTitle')
        company_name = job.find("div", class_='aboutCompanyName')
        location = job.find("div", class_='details location')
        date_posted = job.find("span", class_='timeText')

        job_data.append({
            "Title": title.text.strip() if title else "Not specified",
            "Company Name": company_name.text.strip() if company_name else "Not specified",
            "Location": location.text.strip() if location else "Not specified",
            "Date Posted": date_posted.text.strip() if date_posted else "Not specified",
        })

    return pd.DataFrame(job_data), f"{len(job_cards)} job(s) found"


def main():
    # # Collect user input
    # job_position = input("Enter job position: ").strip()
    # years_of_experience = int(input("How many years of experience do you have? "))
    # location_preferred = input("Preferred Location: ").strip()
    job_position = "Python developer"
    years_of_experience = 0
    location_preferred = "pune"

    # Fetch job data
    job_data, total_openings = fetch_job_data(job_position, years_of_experience, location_preferred)

    if job_data is not None and not job_data.empty:
        # Export data to Excel
        file_name = f"{job_position}_{location_preferred}.xlsx".replace(" ", "_")
        job_data.to_excel(file_name, index=False)
        print(f"Job data exported to '{file_name}'")
        print(f"Number of job openings: {total_openings}")
    else:
        print("No jobs found for the given criteria.")


# Entry point for the script
if __name__ == "__main__":
    main()
