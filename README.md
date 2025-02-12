# LinkedIn Profile Details Scraper using Selenium

## Overview
This project is a **LinkedIn Profile Details Scraper** built using **Selenium**. It automates the process of extracting profile details from LinkedIn, such as name, headline, experience, education, and skills.

⚠ **Disclaimer:** Scraping LinkedIn may violate its terms of service. Use this tool responsibly and ensure compliance with LinkedIn's policies.

## Features

### 🔹 Automated Login
- Uses Selenium to automate LinkedIn login with provided credentials.
- Bypasses CAPTCHA using manual intervention when needed.

### 🔹 Profile Data Extraction
- Extracts **basic details** (name, headline, location, profile image URL).
- Scrapes **experience** (job titles, company names, duration, and descriptions).
- Retrieves **education** (institutions, degrees, years attended).
- Gathers **skills** listed on the profile.
- Collects **certifications** and additional information.

### 🔹 CSV/JSON Export
- Saves extracted data in structured CSV or JSON format for easy analysis.

### 🔹 Headless Mode (Optional)
- Supports headless browsing for running the scraper without opening a browser window.

### 🔹 Proxy & User-Agent Support
- Prevents detection by rotating user-agents and using proxy servers.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Google Chrome
- ChromeDriver (compatible with your Chrome version)
- Selenium (`pip install selenium`)

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/Linkedin-Profile-Details-Scraper-using-Selenium.git
   cd Linkedin-Profile-Details-Scraper-using-Selenium
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure your LinkedIn credentials in a `.env` file (or directly in the script, not recommended for security reasons).
   ```env
   LINKEDIN_USERNAME=your_email@example.com
   LINKEDIN_PASSWORD=your_password
   ```

## Usage

### Running the Scraper
```sh
python scraper.py
```

### Command-line Arguments (Optional)
```sh
python scraper.py --headless --output format.json --profile https://www.linkedin.com/in/sample-profile/
```
- `--headless`: Run in headless mode.
- `--output format.json`: Save output as JSON.
- `--profile`: Specify the LinkedIn profile URL to scrape.

## Output
The extracted data will be saved as `output.csv` or `output.json` (depending on your settings).

## Troubleshooting
- **Issue:** `Session Expired or Login Blocked`
  - Solution: Try logging in manually first and ensure your credentials are correct.
- **Issue:** `LinkedIn CAPTCHA`
  - Solution: Manually solve the CAPTCHA or use Selenium’s wait and retry mechanism.

## Future Enhancements
- Implementing **AI-based CAPTCHA Solvers**.
- Using **Scrapy + Selenium for better efficiency**.
- Adding **Database Support** (MongoDB, PostgreSQL, etc.).

## License
This project is licensed under the **MIT License**.

## Disclaimer
This tool is intended for educational purposes only. Use it responsibly and comply with LinkedIn's policies.

---

### 🚀 Happy Scraping! 🎯

