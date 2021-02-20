from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

def take_strings(url):
    page = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.text, 'html.parser')
    td = soup.find_all('td', class_='table-top')
    table = td[0].parent.parent
    strings = table.find_all('tr', valign='top')
    
    return strings

def make_table_list(strings):
    table_list = []
    strings_list = []

    for string in strings:
        cell = string.find_all('td', class_='screener-body-table-nw')
        for i in cell:
            strings_list.append(i.text)
        strings_list.pop(0)    
        table_list.append(strings_list)
        strings_list = []
        
    return table_list

def market_cap_handler(df):
    for i in range(len(df)):
        if 'M' in df['Market Cap, M'].loc[i]:
            df['Market Cap, M'].loc[i] = round(float(df['Market Cap, M'].loc[i][:-1]), 0)
        elif 'B' in df['Market Cap, M'].loc[i]:
            df['Market Cap, M'].loc[i] = round(float(df['Market Cap, M'].loc[i][:-1]) * 10e3, 0)
            
    return df

def parse_screener():
    start_url = 'https://finviz.com/screener.ashx?v=111&f=cap_smallover&o=-volume&r='

    pages = [1, 21, 41, 61, 81]
    table_headers = ['Ticker', 'Company', 'Sector', 'Industry', 'Country', 'Market Cap, M', 'P/E', 'Price', 'Change', 'Volume']
    final_table = []

    for i in pages:
        url = start_url + str(i)
        strings = take_strings(url)
        final_table += make_table_list(strings)

    return pd.DataFrame(final_table, columns=table_headers)