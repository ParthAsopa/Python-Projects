from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By

options = webdriver.EdgeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# service=EdgeService(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(options=options)

usernames = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
]
for i in usernames:
    driver.get("https://www.saucedemo.com/")
    try:
        driver.find_element(By.ID, "user-name").send_keys(i)
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
    except:
        print("\nCan't find login fields\n")
        continue

    try:
        assert driver.find_element(By.ID, "inventory_container")
        print(
            f"Login successful for Username: {i}\n_____________________________________________________________________________________________"
        )
    except:
        print(f"Error for usename: {i}")
        l = driver.find_elements(By.CLASS_NAME, "error-message-container")
        for i in l:
            print(
                f"\nError: {i.find_element(By.TAG_NAME, "h3").text}\n_____________________________________________________________________________________________"
            )

driver.quit()
