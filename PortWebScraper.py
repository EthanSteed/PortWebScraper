from ast import List, Not
from asyncio.windows_events import NULL
import dataclasses
from pickle import NONE
from time import sleep
from tkinter import W
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pytest_embedded.plugin import port
import requests
import csv

i=0

ListOfPorts = []
VistedUrl = []

def GetCountryFromTable(CountryString, page):
    Country = page.find("span", string=CountryString)
    if Country is not None:
        CountryData = Country.parent.find_next_sibling().findChild()
        if CountryData is None:
            CountryRecord = "n/a"
        else:
            CountryRecord = CountryData.string
    else:
        CountryRecord = "n/a"
    return CountryRecord

def GetPhoneFromTable(PhoneString, page):
    Phone = page.find("span", string=PhoneString)
    if Phone is not None:
        PhoneData = Phone.parent.find_next_sibling().next
        if PhoneData is None:
            PhoneRecord = "n/a"
        else:
            PhoneRecord = PhoneData.strip("(")
    else:
        PhoneRecord = "n/a"
    return PhoneRecord

def GetWebsiteFromTable(WebsiteString, page):
    Website = page.find("span", string=WebsiteString)
    if Website is not None:
        WebsiteData = Website.parent.find_next_sibling()
        if WebsiteData is None:
            WebsiteRecord = "n/a"
        else:
            WebsiteRecord = WebsiteData.string
    else:
        WebsiteRecord = "n/a"    
    return WebsiteRecord

def GetEmailFromTable(EmailString, page):
    Email = page.find("span", string=EmailString)
    if Email is not None:
        EmailData = Email.parent.find_next_sibling()
        if EmailData is None:
            EmailRecord = "n/a"
        else:
            EmailRecord = EmailData.string
    else:
        EmailRecord = "n/a"
    return EmailRecord


## get port details from port page
def GetPort(hyperlink):
    if hyperlink not in VistedUrl:
        if hyperlink.find("/browse/") == -1:    
            VistedUrl.append(hyperlink)
            hyperlinkpage = requests.get(hyperlink)
            page = BeautifulSoup(hyperlinkpage.content, "html.parser")
            if page.findAll("h3", string="Location details") is not []:
               portname = page.find("h2", {"class": "prepend-1 splash"})
               if portname is not None:
                   portcountry = GetCountryFromTable("Country:", page)
                   portPhone = GetPhoneFromTable("Phone:", page)
                   portWebsite = GetWebsiteFromTable("Web site:", page)
                   portEmail = GetEmailFromTable("E-mail:", page)
                   newport = [portname.string, portcountry, portPhone, portEmail, portWebsite]
                   print(newport)
                   writer.writerow(newport)
                   
def GetHyperLinks(page):
    for hyperlink in page.findAll("a", href=True):
        nexturl = "http://ports.com" + hyperlink.attrs['href']
        GetPort(nexturl)
        GetBrowsePage(nexturl)
                   
def GetBrowsePage(hyperlink):
    if hyperlink not in VistedUrl:
        VistedUrl.append(hyperlink)
        browseingpage = requests.get(hyperlink)
        browse = BeautifulSoup(browseingpage.content, "html.parser")
        for record in browse.findAll("li", {"class": "record container"}):
            GetHyperLinks(record)
        for paging in browse.findAll("div", {"class": "paging"}):
            GetHyperLinks(paging)
       
def ExhuastiveSearch():


    for browse in soup.findAll("a", href=True):
        if browse.attrs['href'].find("/browse/") != -1:
            GetBrowsePage("http://ports.com" + browse.attrs['href'])
        


url = "http://ports.com"

VistedUrl.append(url)

portpage = requests.get(url)
header = ["port", "country", "phone", "email", "website"]

soup = BeautifulSoup(portpage.content, "html.parser")

with open('ports.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    
    writer.writerow(header)

## find lists of port pages
    ExhuastiveSearch()
f.close()
        
print(len(ListOfPorts))

        
        



    
    




