import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate

class LinkedinJobScraper():
    """
    A scraper for LinkedIn job postings using the LinkedIn Jobs Guest API.
    Extracts job IDs, job details (company, role, applicants, job URL), 
    and allows export to CSV or table format.
    """
    def __init__(self, country, title, max_results):
        """
        Initialize the scraper with the job search parameters.

        Parameters:
        - country (str): The country in which to search for jobs.
        - title (str): The job title or keywords.
        - max_results (int): Maximum number of job postings to retrieve (multiples of 25 +1).
        """
        self.title = title
        self.country = country
        self.max_results = max_results
        self.job_formatter = lambda job:job.replace(" ", "%2B")
        self.jobs = []
    
    def get_job_ids(self, start):
        """
        Retrieve a list of job IDs from LinkedIn search results starting from a specific offset.

        Parameters:
        - start (int): Pagination start index (0, 25, 50, ...).

        Returns:
        - job_ids (list): A list of job ID strings.
        """
        formatted_title = self.job_formatter(self.title)
        base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        url = f"{base_url}?keywords={formatted_title}&location={self.country}&start={start}"
        response = requests.get(url)

        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        job_elements = soup.find_all("li")

        job_ids = []

        for job in job_elements:
            base_card = job.find("div", {"class": "base-card"})
            if base_card:
                job_ids.append(base_card.get("data-entity-urn").split(":")[3])

        return job_ids

    def get_job_details(self, job_id):
        """
        Retrieve job details for a given job ID.

        Parameters:
        - job_id (str): The job posting ID.

        Returns:
        - job (dict): Dictionary containing job_id, company_name, role, applicants, and job_url.
        """
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        response = requests.get(job_url)
        soup = BeautifulSoup(response.text, "html.parser")

        job = {"job_id": job_id}

        try:
            job["company_name"] = soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).get_text(strip=True)
        except:
            job["company_name"] = None

        try:
            job["role"] = soup.find("h2", {"class": "top-card-layout__title"}).get_text(strip=True)
        except:
            job["role"] = None

        applicants = soup.find("figcaption", {"class": "num-applicants__caption"})
        if applicants:
            match = re.search(r'\d+', applicants.get_text(strip=True))
            if match:
                job["applicants"] = match.group()

        try:
            job["job_url"] = soup.find("a", {"class": "topcard__link"}).get("href")
        except:
            job["job_url"] = None

        print(f"Scraped: {job['job_url']}")
        return job
    
    def scrape_jobs(self):
        """
        Main method to control job scraping process. Iterates over paginated results,
        fetches job IDs and their corresponding job details.
        """
        for start in range(0, self.max_results, 25):
            job_ids = self.get_job_ids(start)
            for job_id in job_ids:
                job_details = self.get_job_details(job_id)
                self.jobs.append(job_details)

    def to_csv(self):
        self.df = pd.DataFrame(self.jobs)
        self.df.to_csv("output.csv", index=False, encoding="utf-8")

    def print_tabulated(self):
        df = self.to_csv()
        print(tabulate(df, headers='keys', tablefmt='fancy_grid'))


if __name__ == "__main__":
    scraper = LinkedinJobScraper(title="Data Scientist", country="germany", max_results=201)
    scraper.scrape_jobs()
    scraper.to_csv()

