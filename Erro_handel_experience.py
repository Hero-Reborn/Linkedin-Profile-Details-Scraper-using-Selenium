from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from collections import OrderedDict

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
driver.get(f"https://www.linkedin.com/search/results/people/?keywords={search_query}")
time.sleep(5)

print(f"🔎 Searching LinkedIn Profiles for: {search_query}")

# **Step 2: Navigate Through Pages to Collect Unique Profile Links**
profile_urls = OrderedDict()  # Using OrderedDict to maintain order & avoid duplicates
max_profiles = 100  
max_pages = 3  
current_page = 1

while len(profile_urls) < max_profiles and current_page <= max_pages:
    print(f"\n🔎 Processing Page {current_page}...")

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

            if main_profile_link and "linkedin.com/in/" in main_profile_link:
                profile_urls[main_profile_link] = None  # Using OrderedDict to store unique links
        except:
            continue 

    print(f"Collected {len(profile_urls)} unique profiles so far.")

    # **Navigate to the Next Page**
    try:
        next_page_button = driver.find_element(By.XPATH, f"//button[@aria-label='Page {current_page + 1}']")
        driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
        time.sleep(2)
        next_page_button.click()
        time.sleep(5) 
        current_page += 1
    except:
        print("No more pages found.")
        break  

# **Step 3: Visit Each Unique Profile & Extract Data**
def extract_text(element, default="Not Available"):
    """Helper function to extract text with fallback"""
    try:
        return element.text.strip()
    except:
        return default

# **Create a DataFrame to Store Extracted Data**
data = []

print(f"\n🎯 Visiting {len(profile_urls)} unique profiles in order...")

for profile_url in profile_urls.keys():
    driver.get(profile_url)
    time.sleep(5)

    # **Extract Name**
    name = "Name Not Found"
    try:
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text.strip()
    except:
        pass

    # **Extract Job Title**
    job_title = "Job Title Not Found"
    try:
        job_title = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text.strip()
    except:
        pass

    # **Scroll to Experience Section**
    try:
        experience_section = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "experience"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", experience_section)
        time.sleep(2)

        # **Find the closest ancestor `<section>` that contains the experience section**
        experience_section = experience_section.find_element(By.XPATH, "./ancestor::section")
    
    except:
        print(f"❌ Skipping {profile_url} - No Experience Section Found.")
        continue  # **Skip this profile and move to the next one**

    # **Extract All Experience Entries**
    experience_entries = []
    try:
        experience_list = experience_section.find_elements(By.XPATH, ".//li[contains(@class, 'artdeco-list__item')]")

        for exp in experience_list:
            try:
                company_name = extract_text(exp.find_element(By.XPATH, ".//span[contains(text(), '·')]")).split("·")[0].strip()
            except:
                company_name = "Company Not Found"

            try:
                position = extract_text(exp.find_element(By.XPATH, ".//span[contains(@aria-hidden, 'true')]"))
            except:
                position = "Position Not Found"

            try:
                employment_type = extract_text(exp.find_element(By.XPATH, ".//span[contains(text(), '·')]"))
            except:
                employment_type = "Employment Type Not Found"

            try:
                duration = extract_text(exp.find_element(By.XPATH, ".//span[contains(@aria-hidden, 'true') and contains(text(), 'Present')]"))
            except:
                duration = "Duration Not Found"

            try:
                location = extract_text(exp.find_element(By.XPATH, ".//span[contains(@aria-hidden, 'true') and contains(text(), ',')]"))
            except:
                location = "Location Not Found"

            try:
                company_linkedin = exp.find_element(By.XPATH, ".//a[contains(@href, 'linkedin.com/company')]").get_attribute("href")
            except:
                company_linkedin = "Company LinkedIn Not Found"

            experience_entries.append({
                "Company Name": company_name,
                "Position": position,
                "Employment Type": employment_type,
                "Duration": duration,
                "Location": location,
                "Company LinkedIn URL": company_linkedin
            })

    except:
        print(f"❌ No experience data found for {profile_url}")
        continue  # **Skip the profile if experience data is missing**

    # **Save Data in List for Processing**
    for entry in experience_entries:
        data.append({
            "Profile URL": profile_url,
            "Name": name,
            "Job Title": job_title,
            "Company Name": entry["Company Name"],
            "Position": entry["Position"],
            "Employment Type": entry["Employment Type"],
            "Duration": entry["Duration"],
            "Location": entry["Location"],
            "Company LinkedIn URL": entry["Company LinkedIn URL"]
        })

    time.sleep(3)

# Close the driver
driver.quit()
