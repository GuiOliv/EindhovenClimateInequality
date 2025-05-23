from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time

# Setup
start_date = datetime(2023, 6, 30)
end_date = datetime(2025, 5, 20)
interval = timedelta(days=69)
download_dir = "../Datasets/Air Pollution Datasets"

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_dir}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.get("https://ilm2.site.dustmonitoring.nl/download")

wait = WebDriverWait(driver, 5)

def download_data(start, end):
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)  
    wait.until(EC.presence_of_element_located((By.NAME, "from")))
    wait.until(EC.presence_of_element_located((By.NAME, "to")))

    from_input = driver.find_element(By.NAME, "from")
    until_input = driver.find_element(By.NAME, "to")
    
    from_input.clear()
    from_input.send_keys(start.strftime("%Y-%m-%d"))

    until_input.clear()
    until_input.send_keys(end.strftime("%Y-%m-%d"))

    Select(driver.find_element(By.NAME, "interval")).select_by_visible_text("1 day")
    Select(driver.find_element(By.NAME, "align")).select_by_visible_text("beginning")

    time.sleep(1) 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    webdriver.ActionChains(driver).move_by_offset(0, 0).click().perform()
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Download']").click()
    time.sleep(5) 

# Loop through time windows
current = start_date
while current < end_date:
    until = min(current + interval, end_date)
    print(f"Downloading: {current} to {until}")
    download_data(current, until)
    current = until + timedelta(days=1)

driver.quit()
