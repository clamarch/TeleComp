#Type /*/ to find places ripe for improvement

import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import logging

import Selenium #used when the html page we try to load is generated client-side

#dictionnary containing appropriate URLs to use depending on company
def url(company):
    cases = {
        "Videotron": 'https://videotron.com/internet/forfaits-internet-illimite',
        "Bell": 'https://www.bell.ca/Bell_Internet/Internet_access',
        "Distributel": 'https://www.distributel.ca/shop/internet-quebec'
    }
    return cases.get(company)

def extract_num(vector):
    for index, text in enumerate(vector):
        match = re.search(r'\d+\.\d+|\d+', text)
        vector[index] = match.group() if match else None

#function used to pull information from website
def main(company, name_tag, price_tag, speed_tag):
    
    #Bell uses client side JS to produce its webpage
    if company==("Bell", "Distributel"):
        response = Selenium.get_page_sel(url(company))
        logging.info("Getting soup")
        soup = BeautifulSoup(response, 'html.parser') #don't need the .text here since it is already in that format
    else:
        response = requests.get(url(company))
        logging.info("Getting soup")
        soup = BeautifulSoup(response.text, 'html.parser') #html page

    names = soup.find_all(name_tag[0], attrs=name_tag[1])  # find Name of internet plans offered
    prices = soup.find_all(price_tag[0], attrs=price_tag[1])  # find prices of internet plans offered
    speeds = soup.find_all(speed_tag[0], attrs=speed_tag[1])

    vnames= [name.get_text().strip() for name in names]
    vprices= [price.get_text().strip() for price in prices]
    vspeeds= [speed.get_text().strip() for speed in speeds[::2]] #need to skip second element becaus it is not the speed info
    
    print(vspeeds)

    #/*/need to do an additional pass through for Bell
    if company == "Bell":
        vspeeds= [speed for speed in vspeeds[::2]]

    #use regular expressions to extract numerical values from a list of strings
    extract_num(vspeeds)
    extract_num(vprices)

    d={'Plan_Name': vnames,'Speed':vspeeds, 'Price':vprices} #create table
    
    df = pd.DataFrame(d) #make the panda dataframe
    
    #Convert 'Speed' and 'Price' columns to numeric
    df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce') 
    
    #need to rebase speeds so that they are all on a mb basis
    is_mb = df['Speed'] < 25 # worst mb speed available
    df.loc[is_mb, 'Speed'] *= 1000

    df['Speed_Per_Dollar'] = df['Speed'] / df['Price']
    df['Speed_Per_Dollar'] = df['Speed_Per_Dollar'].round(3) #format column at 3 decimals
    
    df['Company']=company #add the company to the table

    all_companies_dict[company] = df

#globally declare a dictionnary to hold all the dfs.  used to merge all dfs at the end
all_companies_dict = {}

######## videotron html calls for main function #########
vdtr_name_tag = ("h1", {'class': 'h3 mt-0 mb-1'})
vdtr_price_tag = ("span", {'class': 'bf-price__dollar'})
vdtr_speed_tag = ("li", {'class': 'd-flex flex-row mb-2'})

#main("Videotron", vdtr_name_tag, vdtr_price_tag, vdtr_speed_tag)

######## bell html calls for main function #########
bell_name_tag = ("h2", {'class': 'small-title margin-l-xs-15'})
bell_price_tag = ("div", {'class': 'big-price priceText'}) #/*/returns prices in this format : '$60.00/mo. per month'
bell_speed_tag = ("div", {'class': 'subtitle-2-reg margin-b-5'}) #format is: '3 GbpsGiga bits per second\xa0Footnote2A wired connection, or multiple wired/wireless connections are required to obtain speeds of up to 3 Gbps'

#main("Bell", bell_name_tag, bell_price_tag, bell_speed_tag)

######## distributel html calls for main function #########
dist_name_tag = ("h4", {'class': 'tiletitle'})
dist_price_tag = ("h3", {'class': 'tileprice dablu'}) 
dist_speed_tag = ("h2", {'class': 'tilespeed'})

main("Distributel", dist_name_tag, dist_price_tag, dist_speed_tag)

all_companies = pd.concat(all_companies_dict.values(), ignore_index=True)  # merge all DataFrames
all_companies = all_companies.sort_values(by='Speed_Per_Dollar', ascending=False)
print(all_companies)