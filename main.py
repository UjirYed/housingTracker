from autoLoginTwo import autoLogin
from getTableData import generate_row_data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime

options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--no-sandbox")

#provide location where chrome stores profiles
#options.add_argument(r"--user-data-dir=/Users/rijudey/Library/Application Support/Google/Chrome")

#provide the profile name with which we want to open browser
#options.add_argument(r'--profile-directory=Profile 1')

#specify where your chrome driver present in your pc
driver = webdriver.Chrome(options=options)

#provide website url here
driver.get("https://orsview.cuf.columbia.edu/Summary.aspx")

if __name__ == "__main__":
    all_data = pd.DataFrame(np.arange(13).reshape(1,-13))
    all_data.columns = ["Web Link", "Building", "Single", "Double", "Single_", "Double_", "2", "3", "4", "5", "6", "7", "8"]
    timeInterval = 300 #5 minutes
    numItr = 20

    for i in range(numItr):
        try: #find the table element.
            element = driver.find_element(By.CLASS_NAME, "filter")
            html = driver.page_source
        except:
            html = autoLogin(driver)
            html = driver.page_source
        print(f"{i + 1}th iteration done.")

        source = BeautifulSoup(html, 'html.parser') # open the html file
        
        data_columns = ["Web Link", "Building", "Single", "Double", "Single_", "Double_", "2", "3", "4", "5", "6", "7", "8"] # columns of our table.
        data_rows = generate_row_data(source, data_columns) # adding our scraped data to the dataframe.

        data = pd.DataFrame(data_rows, columns=data_columns) # turn it into a dataframe with our columns
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dt_df = np.array(dt_string).repeat(23)
        data["Time"] = dt_df

        all_data = pd.concat([all_data, data])
        all_data.to_csv("housing.csv")
        data.to_csv('housingTwo.csv', mode='a', index=False, header=False)
        print(all_data) #print out our table.
        time.sleep(timeInterval)
        try:
            # try to refresh the page
            driver.refresh()
        except WebDriverException:
        # if the WebDriver instance is not connected to the DevTools, reinitialize it and navigate to the target webpage
            driver.quit()
            river = webdriver.Chrome(options=options)
            driver.get("https://orsview.cuf.columbia.edu/Summary.aspx")


driver.quit()



