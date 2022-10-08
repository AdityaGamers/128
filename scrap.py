import time
import csv
from webbrowser import BaseBrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


starturl="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome("chromedriver.exe")
browser.get(starturl)
time.sleep(10)
headers=["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planetData=[]
def scrape():
     
     for i in range(1,208):
        while True:
            time.sleep(2)
            soup=BeautifulSoup(browser.page_source,"html.parser")
            currentpage=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if currentpage<i:
                browser.find_element(By.XPATH,value="/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/footer/div/div/div/nav/span[2]/a").click()
            elif currentpage>i:
                browser.find_element(By.XPATH,value="/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/footer/div/div/div/nav/span[1]/a").click()
            else:
                break

        for ul in soup.find_all("ul",attrs={"class","exoplanet"}):
            litags=ul.find_all("li")
            templist=[]
            for i,li in enumerate(litags):
                if  i==0:
                    templist.append(li.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(li.contents[0])
                    except:
                        templist.append("")
            hyperlinktag=litags[0]
            templist.append("https://exoplanets.nasa.gov"+hyperlinktag.find_all("a", href=True)[0]["href"])
            planetData.append(templist)
        print(f"page {i} done")
        browser.find_element(By.XPATH,value="/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/footer/div/div/div/nav/span[2]/a").click()
    
scrape()
newdata=[]
def scrapedata(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        templist=[]
        for tr in soup.find_all("tr",attrs={"class":"fact_row"}):
            tdtags=tr.find_all("td")
            for td in tdtags:
                try:
                    templist.append(td.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        newdata.append(templist)
    except:
        time.sleep(1)
        scrapedata(hyperlink)
for i ,data in enumerate(planetData):
    scrapedata(data[5])
finaldata=[]
for i,data in enumerate(planetData):
    x=newdata[i]
    x=[y.replace("\n","") for y in x]
    x=x[:7]
    finaldata.append(data+x)
with open("final.csv","w") as Z:
        writer=csv.writer(Z)
        writer.writerow(headers)
        writer.writerows(finaldata)