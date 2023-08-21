
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

#provide location where chrome stores profiles
options.add_argument(r"--user-data-dir=/Users/rijudey/Library/Application Support/Google/Chrome")

#provide the profile name with which we want to open browser
options.add_argument(r'--profile-directory=Profile 1')

#specify where your chrome driver present in your pc
driver = webdriver.Chrome(options=options)

def get_page_source(url, htmlFile): # get the page source and write it to an html file.
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    with open(htmlFile, "w") as f:
        f.write(html)
    driver.close()
    return

def print_table(file: str): #file is a beautifulSoupObject
    table = file.find('table', class_ = "filter")
    rows = table.find_all("tr")

    for row in rows:
        cells = row.find_all(['th','td'])
        print(len(cells))
        for cell in cells:
            if cell.string is None:
                print(0)
            print(cell.text, end='\t')
        print()

def generate_row_data(file: str, data_columns: list[str]):
    data_rows = []
    for row in file.find_all('tr'):
        row_data = []
        for cell in row.find_all(['td','th']):
            row_data.append(cell.text)
        if len(row_data) == len(data_columns):
            data_rows.append(row_data)
    return data_rows
    




if __name__ == "__main__":
    #------------- 
    #TODO: Export the data to a csv file, with each dataframe being indexed by time.
    #-------------

    #get_page_source(url, "test.html")

    with open("test.html") as fp:
        source = BeautifulSoup(fp, 'html.parser') # open the html file
    
    
    data_columns = ["Web Link", "Building", "Single", "Double", "Single_", "Double_", "2", "3", "4", "5", "6", "7", "8"] # columns of our table.

    data_rows = generate_row_data(source, data_columns) #adding our scraped data to the dataframe.

    data = pd.DataFrame(data_rows, columns=data_columns) #turn it into a dataframe with our columns

    print(data) #print out our table.

    data = data.concat()

