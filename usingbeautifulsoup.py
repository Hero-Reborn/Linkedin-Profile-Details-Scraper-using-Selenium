import sys
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlparse


def extract_slug(url):
    path = urlparse(url).path  # Extract path after domain
    parts = path.split("/")  # Split URL path
    return parts[2] if len(parts) > 2 and parts[2] and not parts[2].startswith("?") else None  # Ensure slug exists and isn't just query params

# Filter URLs: Keep only those with a valid slug


# Set up WebDriver options
chrome_options = Options()
chrome_options.add_argument("--disable-features=WebRtc")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# LinkedIn credentials
linkedin_email = 

# Log in to LinkedIn
driver.get("https://www.linkedin.com/login")
time.sleep(8)

email_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")
email_field.send_keys(linkedin_email)
password_field.send_keys(linkedin_password)
password_field.send_keys(Keys.RETURN)
time.sleep(8)

# **Step 1: Search for a Specific Query on LinkedIn**
search_query = "Software Engineer"
# geo_id = "106204383"  # Dubai geoId
base_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query}"

# **Step 2: Navigate Through Pages to Collect Unique Profile Links**
profile_urls = OrderedDict()  # Using OrderedDict to maintain order & avoid duplicates
max_profiles = 5
max_pages = 1
current_page = 1

while len(profile_urls) < max_profiles and current_page <= max_pages:
    print(f"\n🔎 Processing Page {current_page}...")

    # Construct the new URL for the current page
    page_url = f"{base_url}&page={current_page}"
    driver.get(page_url)
    time.sleep(5)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='linkedin.com/in/']"))
        )
    except:
        print("No profiles found or page load issue.")
        break

    profiles = driver.find_elements(By.CSS_SELECTOR, "a[href*='linkedin.com/in/']")
    
    for profile in profiles:
        try:
            main_profile_link = profile.get_attribute("href")
            print(f"link {main_profile_link}")
            if extract_slug(main_profile_link) is None:
                continue
            if main_profile_link and "linkedin.com/in/" in main_profile_link:
                profile_urls[main_profile_link] = None  # Using OrderedDict to store unique links
        except:
            continue 

    print(f"Collected {len(profile_urls)} unique profiles so far.")
    current_page += 1  # Increment page for next iteration

# -------------------- Storing Data in Excel ---------------------
all_data = []  # Will store data from each valid profile

print(f"\n🎯 Visiting {len(profile_urls)} unique profiles in order...")

for profile_url in profile_urls.keys():
    driver.get(profile_url)
    time.sleep(5)

    # **Extract Page Source for BeautifulSoup**
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # **Extract Name**
    name = "Name Not Found"
    try:
        name_element = soup.find("h1")
        if name_element:
            name = name_element.get_text(strip=True)
    except:
        pass

    # **Extract Job Title**
    job_title = "Job Title Not Found"
    try:
        job_title_element = soup.select_one("div.text-body-medium.break-words")
        if job_title_element:
            job_title = job_title_element.get_text(strip=True)
    except:
        pass

    # **Locate Experience Section**
    # experience_section = soup.find("section", {"id": "experience"})
    first_location = "Location Not Found"
    # print(f"experieeeeenccceee {experience_section}")
    # if experience_section:
        # **Extract First Experience Entry**
    first_experience = soup.find("li", class_="artdeco-list__item")
    print(f"first_locationnnnnn {first_experience}")
        
    if first_experience:
            try:
                # Extract all spans with location class
                location_elements = first_experience.find_all("span", class_="t-14 t-normal t-black--light")
                
                if location_elements:
                    # Get the last occurrence
                    first_location = location_elements[-1].get_text(strip=True)

            except:
                pass

    # **Extract Company Name and Employee Count (Retaining Existing Functionality)**
    company_name, num_employees = "Company Name Not Found", "Employees Not Found"

    try:
        company_name_element = soup.find("span", class_="t-14 t-normal")  # Adjust class based on HTML structure
        if company_name_element:
            company_name = company_name_element.get_text(strip=True)
    except:
        pass

    # **Extract Contact Info (Existing Functionality)**
    email, phone_number = "Email Not Found", "Phone Number Not Found"
    
    try:
        contact_info_button = driver.find_element(By.XPATH, "//a[contains(@href, 'overlay/contact-info')]")
        contact_info_button.click()
        time.sleep(3)

        # Email
        email_element = driver.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]")
        email = email_element.get_attribute("href").replace("mailto:", "")
        
        # Phone
        phone_number_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Phone')]/following-sibling::span")
        phone_number = phone_number_element.text.strip()

        # Close Contact Info Modal
        dismiss_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Dismiss') and contains(@class, 'artdeco-button')]"))
        )
        driver.execute_script("arguments[0].style.zIndex = 9999;", dismiss_button)
        dismiss_button.click()
        time.sleep(3)

    except:
        pass

    # **Optional Logging**
    print(f"\n🔹 Profile: {profile_url}")
    print(f"Name: {name}")
    print(f"Job Title: {job_title}")
    print(f"🏢 Company Name: {company_name}")
    print(f"🌍 First Company Location: {first_location}")
    print(f"📧 Email: {email}")
    print(f"📞 Phone Number: {phone_number}")

    # **Append Data to the all_data List** 
    all_data.append({
        "Name": name,
        "Job Title": job_title,
        "Company Name": company_name,
        "Employee Count": num_employees,
        "First Company Location": first_location,
        "Profile URL": f'=HYPERLINK("{profile_url}", "{profile_url}")',  # Clickable link
        "Email": email,
        "Phone": phone_number
    })

    time.sleep(3)

# **Write Data to Excel**
output_file = "linkedin_profiles.xlsx"
df = pd.DataFrame(all_data)

# Keep columns in the user-specified order
df = df[["Name", "Job Title", "Company Name", "Employee Count", "First Company Location", "Profile URL", "Email", "Phone"]]

df.to_excel(output_file, index=False)
print(f"\n✅ Data successfully saved to {output_file}")

# Close the driver
driver.quit()
