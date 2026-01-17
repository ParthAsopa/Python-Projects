from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

# from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By

load_dotenv()
username=os.getenv("username")
password=os.getenv("password")


options = webdriver.EdgeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Edge(options=options)

driver.get("https://hfw.vitap.ac.in:8090/httpclient.html")
original_window = driver.current_window_handle
all_tabs = driver.window_handles
for tab in all_tabs:
    if tab != original_window:
        driver.switch_to.window(tab)
        break

wait = WebDriverWait(driver, 100)


# wait = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.ID, "details-button"))
# )

if len(driver.find_elements(By.ID, "details-button")) != 0:
    driver.find_element(By.ID, "details-button").click()
    driver.find_element(By.ID, "proceed-link").click()

wait = WebDriverWait(driver, 100)
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "loginbutton").click()
wait = WebDriverWait(driver, 10)
driver.find_element(By.ID, "loginbutton").click()
wait = WebDriverWait(driver, 100)
if driver.find_element(By.ID, "loginbutton").text == "Sign in":
    print("LOGOUT SUCCESSFUL!!!")
else:
    print("LOGOUT UNSUCCESSFUL :(((")

driver.quit()
