from selenium import webdriver  
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("--incognito")
DRIVER_PATH = 'C:\\Users\\hp\\Desktop\\WebScrapping\\chromedriver'

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

driver.get('https://www.fractal.is/games')
time.sleep(10)
soup=BeautifulSoup(driver.page_source,'html5lib')

rr=soup.find('div',attrs={'class':'mt-20 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4 2xl:grid-cols-6 gap-6'})

results=[]

for content in rr.find_all('div',attrs={'class':'MuiPaper-root MuiPaper-outlined MuiPaper-rounded MuiCard-root css-4tnk4k'}):
    result={}
    result['Name']=content.find('h5').text
    innerlink='https://www.fractal.is'+content.find('a')['href']
    driver.get(innerlink)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'html5lib')
    links=soup.find_all('a',attrs={'class':'MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineAlways css-3wvkg3'})
    
    if len(links)==3:
        result['Twitter']=links[0]['href']
        result['Discord']=links[1]['href']
        result['Website']=links[2]['href']
    else:
        continue

    btn=driver.find_element(By.XPATH,'/html/body/div[1]/div/main/div/div[2]/div[1]/div/div/div/div[3]/button')
    btn.click()
    soup=BeautifulSoup(driver.page_source,'html5lib')
    result['Description']=soup.find('p',attrs={'class':'MuiTypography-root MuiTypography-body1 css-158kgyh'}).text
    results.append(result)
    print(result)

def export_data(results):
    filename='fractal.csv'
    with open(filename,'w',newline="") as f:
        w = csv.DictWriter(f,['Name','Twitter','Discord','Website','Description'])
        w.writeheader()
        for row in results:
            try:
                w.writerow(row)
            except Exception as e:
                continue

export_data(results)





