import sys
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

# Set up WebDriver options
chrome_options = Options()
chrome_options.add_argument("--disable-features=WebRtc")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# LinkedIn credentials
linkedin_email = "ishaanraj303@gmail.com"
linkedin_password = "MAHI7784@"

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
base_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query}"

# **Step 2: Navigate Through Pages to Collect Unique Profile Links**
profile_urls = OrderedDict()  # Using OrderedDict to maintain order & avoid duplicates
max_profiles = 100  
max_pages = 3  
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

            if main_profile_link and "linkedin.com/in/" in main_profile_link:
                profile_urls[main_profile_link] = None  # Using OrderedDict to store unique links
        except:
            continue 

    print(f"Collected {len(profile_urls)} unique profiles so far.")

    # **Increment the page number for the next iteration**
    current_page += 1

# **Helper Function to Extract Company Info**
def extract_company_info(driver):
    """Extract company name and employee count from the company page."""
    company_name = "Company Name Not Found"
    num_employees = "Employees Not Found"
    
    try:
        # Extract Company Name using provided XPath
        company_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'org-top-card-summary__title')]"))
        ).text.strip()
    except:
        pass

    try:
        # Extract Employee Count using dynamic XPath
        employees_element = driver.find_element(By.XPATH, "//a[contains(@class, 'org-top-card-summary-info-list__info-item-link')]/span[contains(@class, 't-normal')]")
        num_employees = employees_element.text.strip()
    except:
        pass
    
    # Parse the employee count
    if num_employees != "Employees Not Found":
        if "-" in num_employees:  # Handle cases like "501-1K employees"
            lower_range = num_employees.split("-")[0].strip()  # Extract lower range before "-"
            # Remove the word "employees" from the extracted value
            lower_range = lower_range.replace(" employees", "").strip()
            
            # If the lower range contains 'K' or 'M', we simply store the data (no comparison)
            if "K" in lower_range or "M" in lower_range:
                return company_name, num_employees
            else:
                try:
                    lower_range = int(lower_range)  # Convert lower range to integer
                except:
                    lower_range = "Employees Not Found"
                
                # Skip data where the lower range is less than 500
                if lower_range < 500:
                    return company_name, "Employees Not Found"
        
        elif "K" in num_employees:  # Handle cases like 500K, 1K, etc.
            return company_name, num_employees  # Directly store the data without conversion
        elif "M" in num_employees:  # Handle cases like 1M, etc.
            return company_name, num_employees  # Directly store the data without conversion
        else:
            try:
                num_employees = int(num_employees.split()[0])  # If it's a plain number like '100'
            except:
                num_employees = "Employees Not Found"
    
    return company_name, num_employees

# **Helper Function to Extract Contact Info**
def extract_contact_info(driver):
    """Extract email and phone number from the Contact Info modal."""
    email = "Email Not Found"
    phone_number = "Phone Number Not Found"
    
    try:
        # Click on the "Contact Info" link to open the modal
        contact_info_button = driver.find_element(By.XPATH, "//a[contains(@href, 'overlay/contact-info')]")
        contact_info_button.click()
        time.sleep(3)
        
        # Extract the email address from the mailto link
        email_element = driver.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]")
        email = email_element.get_attribute("href").replace("mailto:", "")
        
        # Extract phone number if available in the contact info modal
        phone_number_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Phone')]/following-sibling::span")
        phone_number = phone_number_element.text.strip()

        # Close the Contact Info modal after extracting the data
        dismiss_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Dismiss') and contains(@class, 'artdeco-button')]"))
        )
        driver.execute_script("arguments[0].style.zIndex = 9999;", dismiss_button)
        time.sleep(1)
        dismiss_button.click()
        time.sleep(3)
                
    except Exception as e:
        print(f"Error while extracting contact info: {e}")
    
    return email, phone_number

# **Create a DataFrame to Store Extracted Data**
# Generate a new file each time based on the timestamp
output_path = f"LinkedIn_Profiles_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

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

    # **Find the Company Link and Visit the Company Page**
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

    # **Extract Company Name and Employee Count**
    company_name, num_employees = extract_company_info(driver)

    # **Skip Profile if Employee Count is Less than 500 or Employee range is less than 500**
    if num_employees == "Employees Not Found" or (isinstance(num_employees, int) and num_employees < 500):
        continue

    # **Return to Profile Page**
    driver.get(profile_url)
    time.sleep(3)

    # **Extract Contact Info (Email and Phone)**]
    email, phone_number = extract_contact_info(driver)

    # **Store Extracted Data in List**
    data.append({
        "Company Name": company_name,
        "Employee Count": num_employees,
        "Job Title": job_title,
        "Name": name,
        "Profile URL": f'=HYPERLINK("{profile_url}")',
        "Email": email,
        "Phone Number": phone_number
    })

    # Write each entry in real-time to the Excel file
    pd.DataFrame(data).to_excel(excel_writer, index=False, sheet_name='LinkedIn Data')

    time.sleep(3)

# **Final Closing of Excel Writer**
excel_writer.close()

# Close the driver
driver.quit()
