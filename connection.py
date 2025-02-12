from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up WebDriver
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

# **Step 1: Search for People Based on Role & Location**
role = "Software Engineer"
location = "Saudi Arabia"

search_url = f"https://www.linkedin.com/search/results/people/?keywords={location}&{role}"
driver.get(search_url)
time.sleep(5)

# **Step 2: Collect Profile Links**
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='linkedin.com/in/']"))
    )
    profile_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='linkedin.com/in/']")
    profile_urls = [link.get_attribute("href") for link in profile_links[:10]]  # Limit to first 10 profiles
    print(f"Found {len(profile_urls)} profiles.")
except:
    print("No profiles found for the given query.")
    driver.quit()
    exit()

# **Step 3: Send Connection Requests**
custom_message = "Hi {name}, I came across your profile and would love to connect!"

for profile_url in profile_urls:
    driver.get(profile_url)
    time.sleep(5)

    try:
        # Click on Connect Button
        connect_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Connect')]"))
        )
        connect_button.click()
        time.sleep(3)

        # Add a Personalized Message
        try:
            add_note_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Add a note')]"))
            )
            add_note_button.click()
            time.sleep(2)

            # Extract Name for Personalization
            name = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").text.split()[0]
            message_box = driver.find_element(By.XPATH, "//textarea[@name='message']")
            message_box.send_keys(custom_message.format(name=name))
            time.sleep(2)

            # Send the Connection Request
            send_button = driver.find_element(By.XPATH, "//button[contains(., 'Send')]")
            send_button.click()
            print(f"✅ Sent connection request to {name}")
        except:
            print(f"⚠️ Could not personalize message for {profile_url}, sending default request.")

            # Send default request if add note option not found
            send_button = driver.find_element(By.XPATH, "//button[contains(., 'Send now')]")
            send_button.click()

    except:
        print(f"❌ Could not connect to {profile_url} (maybe already connected).")

    # Wait before the next request (to avoid spam detection)
    time.sleep(8)

# Close the driver
driver.quit()
