"""
This code implements an autoLogin() function. The main function detects whether the user is logged in. If they are not, 
the autoLogin() function is called and the user is logged in. Then the website's page source is copied over to test.html.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptography.fernet import Fernet
from selenium.common.exceptions import TimeoutException

#create chromeoptions instance
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

#provide location where chrome stores profiles
#options.add_argument(r"--user-data-dir=/Users/rijudey/Library/Application Support/Google/Chrome")

#provide the profile name with which we want to open browser
#options.add_argument(r'--profile-directory=Profile 1')

#specify where your chrome driver present in your pc
driver = webdriver.Chrome(options=options)

#provide website url here
driver.get("https://orsview.cuf.columbia.edu/Summary.aspx")

def autoLogin(driver):
    print("CUFO HOUSING" in driver.title)

    submitButton = driver.find_element(By.NAME, "ctl00$mBody$btnCASLogin")
    time.sleep(0.1)

    submitButton.click()
    time.sleep(0.1)

    username = driver.find_element(By.NAME, "username")
    username.send_keys("rd3054")
    print('sucessfully sent username')
    time.sleep(0.1)

    with open("password.txt", "rb") as f:
        encrypted_password = f.read()
    fernet = Fernet(b'omAqIPsp_Bd_cV2PXWanuZorIVIBvKtKBzTvo4QjBS8=')
    password = fernet.decrypt(encrypted_password)
    passwordField = driver.find_element(By.NAME, "password")
    passwordField.send_keys(password.decode("utf-8"))
    print('sucessfully sent password')

    time.sleep(0.1)
    username.send_keys(Keys.RETURN)
    print('sucessfully clicked login')

    with open("selenium.html", "w") as f:
        f.write(driver.page_source)

    time.sleep(0.1)

    #Get the push me a code button

    iframe = driver.find_element(By.ID, "duo_iframe")
    driver.switch_to.frame(iframe)

    wait = WebDriverWait(driver, 15)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[tabindex="2"]'))) #Duo Push Button

    button.click()

    driver.switch_to.default_content()
    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "filter")))
    except TimeoutException as e:
        print('Timed out while waiting for user to authenticate using Duo.')

    return

    

if __name__ == "__main__":

    for i in range(0,10):
        time.sleep(5)
        try:
            element = driver.find_element(By.CLASS_NAME, "filter")
            with open("test.html", "w") as f:
                f.write(driver.page_source)
        except:
            with open("test.html", "w") as f:
                html = autoLogin(driver)
                f.write(driver.page_source)
        print(f"{i + 1}th iteration done.")
        driver.refresh()

driver.quit()


        
