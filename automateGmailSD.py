import os
import random
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptography.fernet import Fernet

# Set Chrome User Data directory path
USER_PROFILE = os.path.expanduser("~")
CHROME_USER_DATA_DIR = os.path.join(USER_PROFILE, "AppData", "Local", "Google", "Chrome", "User Data")

ENCRYPTION_KEY = b'3ZR6KFnAJSdUgfEgaTtd2RhpQumzMwLDjT4jaMd7Gjg='
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_message(message):
    """Encrypts an error message before saving."""
    return cipher.encrypt(message.encode()).decode()

def log_encrypted_error(error_message):
    """Logs encrypted errors to a file."""
    with open("error_logs.txt", "a") as log_file:
        log_file.write(error_message + "\n")

def get_available_profiles():
    """Fetches available Chrome profiles."""
    return [p for p in os.listdir(CHROME_USER_DATA_DIR) if "Default" in p or "Profile" in p]

def setup_webdriver(profile_name):
    """Sets up and returns a Selenium WebDriver instance with the selected Chrome profile."""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
        chrome_options.add_argument(f"--profile-directory={profile_name}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--enable-unsafe-swiftshader")

        driver = webdriver.Chrome(options=chrome_options)
        return driver, WebDriverWait(driver, 10)
    except Exception as e:
        print("Error occured")
        log_encrypted_error(encrypt_message(traceback.format_exc()))
        return None, None

def login_gmail(driver, wait):
    """Logs into Gmail."""
    driver.get("https://mail.google.com")

def scroll_like_human(driver):
    """Simulates human-like scrolling behavior."""
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(random.randint(3, 6)):
            body.send_keys(random.choice([Keys.PAGE_DOWN, Keys.ARROW_DOWN]))
            time.sleep(random.uniform(0.5, 1.5))
    except Exception:
        print("Error occured")
        log_encrypted_error(encrypt_message(traceback.format_exc()))

def open_unread_email(driver, wait):
    """Finds and opens the first unread email matching specific keywords."""
    try:
        keywords = ["Ready"]
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//table[@role='grid']")))
        unread_emails = driver.find_elements(By.XPATH, "//tr[contains(@class, 'zE')]")
        
        for email_row in unread_emails:
            try:
                sender = email_row.find_element(By.XPATH, './/span[@class="bA4"]/span').text.lower()
                subject = email_row.find_element(By.XPATH, './/span[@class="bog"]').text.lower()
                
                print(f"Checking email - From: {sender}, Subject: {subject}")
                
                if any(keyword.lower() in sender or keyword.lower() in subject for keyword in keywords):
                    print(f"Found matching email with keyword - From: {sender}, Subject: {subject}")
                    ActionChains(driver).move_to_element(email_row).click().perform()
                    time.sleep(3)
                    return True
                else:
                    print("No keyword match, skipping email")
            except Exception as e:
                print(f"Error while checking email: {str(e)}")
                continue
        
        print("No matching emails found, switching to next profile")
        return False
        
    except Exception as e:
        print(f"Error in open_unread_email: {str(e)}")
        print(f"Full error details: {traceback.format_exc()}")
        return False

def main():
    """Main function to execute the script on all available profiles."""
    profiles = get_available_profiles()
    for profile in profiles:
        if profile == "Guest Profile": return 
        print(f"Starting automation on profile: {profile}")
        driver, wait = setup_webdriver(profile)
        if driver:
            try:
                login_gmail(driver, wait)
                scroll_like_human(driver)
                if open_unread_email(driver, wait):
                    click_cta_button(driver, wait)
                else:
                    print(f"No matching emails found in profile {profile}, moving to next profile")
                    continue
            finally:
                time.sleep(5)
                driver.quit()
        else:
            print(f"Skipping profile {profile} due to an error.")

def click_cta_button(driver, wait):
    """Finds and clicks a CTA button inside the email."""
    cta_text = ['Click', 'Proceed', "Verify", "Move", "Confirm", "Get", "View", "Complete", "Update", "Track", "Start"]
    xpath_expression = " | ".join([f"//a[contains(text(), '{text}')]" for text in cta_text])
    while True:
        try:
            cta_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))
            driver.execute_script("arguments[0].scrollIntoView();", cta_button)
            time.sleep(random.uniform(1, 2))
            cta_button.click()
            print("CTA button clicked!")
            driver.get("https://mail.google.com")
            time.sleep(3)
            open_unread_email(driver, wait)
            break
        except:
            driver.get("https://mail.google.com")
            time.sleep(3)
            open_unread_email(driver, wait)

def simulate_browsing(driver):
    """Simulates random browsing behavior."""
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        start_time = time.time()
        while time.time() - start_time < random.randint(10, 60):
            body.send_keys(random.choice([Keys.PAGE_DOWN, Keys.ARROW_DOWN, Keys.ARROW_UP]))
            ActionChains(driver).move_by_offset(random.randint(100, 500), random.randint(100, 300)).perform()
            time.sleep(random.uniform(2, 5))
    except Exception:
        print("Error occured")
        log_encrypted_error(encrypt_message(traceback.format_exc()))    

if __name__ == "__main__":
    main()
