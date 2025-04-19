
## Linkedin Job Scraper with CI/CD

This project scrapes job listings from [LinkedIn Jobs](https://www.linkedin.com/jobs/) using the public guest API and stores the results in a CSV file. It includes a GitHub Actions workflow for **daily automated scraping** and updates to the repository.

---

### Features

- Scrapes job titles, companies, applicant counts, and job URLs.
- Supports filtering by job title and country.
- Saves data to a structured `output.csv` file.
- Automatically runs daily using GitHub Actions at **6 AM UTC**.
- Pushes new data to the repo with timestamped commits.

---

### Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`:
  ```
  pandas
  requests
  beautifulsoup4
  tabulate
  ```

Install with:
```bash
pip install -r requirements.txt
```

---

### File Structure

```
.
├── scraper.py            # Main script to scrape job data
├── output/
│   └── output.csv        # Automatically updated daily
├── .github/
│   └── workflows/
│       └── scraper.yml   # GitHub Actions CI/CD workflow
└── README.md             # Project overview
```

---

### Usage

To run locally:

```bash
python scraper.py
```

You can customize the job title, country, and max results in the `__main__` block of `scraper.py`:

```python
scraper = LinkedinJobScraper(
    title="Data Scientist",
    country="germany",
    max_results=201
)
```

---

### GitHub Actions CI/CD

The project uses GitHub Actions to:

- Run the scraper every day at `06:00 UTC`
- Commit the updated `output.csv` to the repo
- Optionally allows manual execution from GitHub's UI

You can find the CI/CD config in `.github/workflows/scraper.yml`.

---

### Sample Output

| job_id | company_name | role           | applicants | job_url         |
|--------|--------------|----------------|------------|-----------------|
| 123456 | Google       | Data Scientist | 27         | `linkedin.com/...` |

---
