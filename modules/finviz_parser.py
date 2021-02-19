from selenium import webdriver
import pandas as pd
import numpy as np
import time


# function for logging in to finviz.com
def login_on_finviz(email, password):
    wb = webdriver.Chrome()
    wb.get('https://finviz.com/login.ashx')

    inputs = wb.find_elements_by_class_name('input')
    inputs[0].send_keys(email)
    inputs[1].send_keys(password)

    btn = wb.find_element_by_class_name('button')

    time.sleep(1)
    btn.click()
    time.sleep(1.5)
    
    return wb


# function to go to the desired page by the ticker
def go_to_company_page(wb, ticker):
    wb.get(f'https://elite.finviz.com/quote.ashx?t={ticker}')
    time.sleep(5)
    
    return wb


# function to change the form of a table
def quarterly_table(wb):
    tables = wb.find_elements_by_class_name('fullview-links')

    for table in tables:
        if 'quarterly' in table.text:
            btn = table.find_elements_by_class_name('tab-link')
            btn[-1].click()
    
    time.sleep(2)
    return wb


# function to getting table data to list
def get_table_list(wb):
    tables = wb.find_elements_by_class_name('snapshot-table2')
    for table in tables:
        if 'Period End Date' in table.text:
            data = table
            
    td = data.find_elements_by_class_name('snapshot-td2')

    table_list = []

    for el in td:
        table_list.append(el.text.replace(',', ''))
            
    return table_list


# function to reformating table list
def reformat_table_list(table_list):
    np_table_list = np.array(table_list)
    np_table_list = np_table_list.reshape(-1, 10)
    np_table_list = np.delete(np_table_list, 1, 0)
    
    return np_table_list

# function to making dataframe from lines
def make_df(table_list, wb):
    
    np_table_list = reformat_table_list(table_list)
    
    index = np_table_list[1:, 0]
    columns = np_table_list[0, 2:]
    values = np_table_list[1:, 2:]
    
    df = pd.DataFrame(values, columns=columns, index=index)
    
    dimension = wb.find_elements_by_css_selector('td[align="right"]')
    for el in dimension:
        if 'values in' in el.text:
            title = el.text
            
    df.index.name = title
    
    return df


# function to making dataframe from lines
def make_yearly_df(table_list, wb):
    
    np_table_list = reformat_table_list(table_list)
    
    index = np_table_list[1:, 0]
    columns = np_table_list[0, 2:]
    values = np_table_list[1:, 2:]
    
    df = pd.DataFrame(values, columns=columns, index=index)
    
    dimension = wb.find_elements_by_css_selector('td[align="right"]')
    for el in dimension:
        if 'values in' in el.text:
            title = el.text
            
    df.index.name = title
    
    columns = df.columns[1:3]
    new_df = df[columns]
    new_df = new_df.replace('', np.nan)
    new_df.dropna(how='any', inplace=True)
    
    new_df = new_df.astype(float)
    new_df['The difference between the indicators'] = new_df[columns[0]] - new_df[columns[1]]
    
    return new_df