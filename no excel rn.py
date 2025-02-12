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

    # **Locate Experience Section Dynamically**
    try:
        experience_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "experience"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", experience_section)
        time.sleep(2)

        # **Find the closest ancestor `<section>` that contains the experience section**
        experience_section = experience_section.find_element(By.XPATH, "./ancestor::section")
    
    except:
        print(f"❌ Experience section not found for {profile_url}")
        continue

    # **Use the Given Absolute XPath but Dynamically Replace `section[4]`**
    first_company_url = "Not Available"
    try:
        company_xpath = experience_section.find_element(By.XPATH, ".//div[3]/ul/li/div/div[1]/a")
        first_company_url = company_xpath.get_attribute("href")

        if not first_company_url or "linkedin.com/company" not in first_company_url:
            print(f"⚠️ Extracted an invalid company link: {first_company_url}")
            continue

    except:
        print(f"❌ No company link found in experience for {profile_url}")
        continue

    # **Visit the Company Page**
    driver.get(first_company_url)
    time.sleep(5)

    # **Extract Company Name Using the Provided Absolute XPath**
    company_name = "Company Name Not Found"
    try:
        company_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[2]/div[1]/div[2]/div/h1"))
        ).text.strip()
    except:
        pass

    # **Extract Number of Employees**
    num_employees = "Employees Not Found"
    try:
        employees_element = driver.find_element(By.XPATH, "//a[contains(@class, 'org-top-card-summary-info-list__info-item-link')]/span[contains(@class, 't-normal')]")
        num_employees = employees_element.text.strip()
    except:
        pass

    # **Print Extracted Data**
    print(f"\n🔹 Profile: {profile_url}")
    print(f"Name: {name}")
    print(f"Job Title: {job_title}")
    print(f"🏢 Company Name: {company_name}")
    print(f"👥 Number of Employees: {num_employees}")

    time.sleep(3)

# Close the driver
driver.quit()


#this uses complete xpath to locate company name

#it does work but some of the times it fails to extract company name, idk why tho

# 1st code that works with company n employee
