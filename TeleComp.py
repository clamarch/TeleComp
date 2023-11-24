import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

#dictionnary containing appropriate URLs to use depending on company
def url(company):
    cases = {
        "Videotron": 'https://videotron.com/internet/forfaits-internet-illimite'
    }
    return cases.get(company)

#function used to pull information from website
def main(company, name_tag, price_tag, speed_tag):
    
    response = requests.get(url(company))
    soup = BeautifulSoup(response.text, 'html.parser') #html page
    
    names = soup.find_all(name_tag[0], attrs=name_tag[1])  # find Name of internet plans offered
    prices = soup.find_all(price_tag[0], attrs=price_tag[1])  # find prices of internet plans offered
    speeds = soup.find_all(speed_tag[0], attrs=speed_tag[1]) 
    
    vnames= [name.get_text().strip() for name in names]
    vprices= [price.get_text().strip() for price in prices]
    vspeeds= [speed.get_text().strip() for speed in speeds[::2]] #need to skip second element becaus it is not the speed info
    
    for index, speeds in enumerate(vspeeds):
        match = re.search(r'\d+\.\d+|\d+', speeds)
        vspeeds[index] = match.group() if match else None
    
    d={'Plan_Name': vnames,'Speed':vspeeds, 'Price':vprices} #create table
    
    df = pd.DataFrame(d) #make the panda dataframe
    
    #Convert 'Speed' and 'Price' columns to numeric
    df['Speed'] = pd.to_numeric(df['Speed'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    
    df['Speed_Per_Dollar'] = df['Speed'] / df['Price']
    df['Speed_Per_Dollar'] = df['Speed_Per_Dollar'].round(3) #format column at 3 decimals
    
    df['Company']=company #add the company to the table

    return df

#videotron html calls for main function
vdtr_name_tag = ("h1", {'class': 'h3 mt-0 mb-1'})
vdtr_price_tag = ("span", {'class': 'bf-price__dollar'})
vdtr_speed_tag = ("li", {'class': 'd-flex flex-row mb-2'})

print(main("Videotron", vdtr_name_tag, vdtr_price_tag, vdtr_speed_tag))