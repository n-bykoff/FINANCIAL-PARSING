from selenium import webdriver
import pandas as pd
import time

def go_to_search_page():
    wd = webdriver.Chrome()
    wd.get('https://www.dividend.com')
    time.sleep(3)
    
    # find lens button
    wd.find_element_by_class_name('n-nav-button').click()
    time.sleep(1)
    return wd

def get_text(wd, ticker):
    time.sleep(1)
    input_field = wd.find_element_by_class_name('full-screen-search-typeahead')
    input_field.send_keys(ticker)
    time.sleep(1)
    button = wd.find_element_by_class_name('t-px-10')
    button.click()

    history_button = wd.find_element_by_class_name('n-ticker_button_expand')
    history_button.click()
    
    time.sleep(2)

    tables = wd.find_elements_by_class_name('t-mb-2')

    for table in tables:
        if '2018' in table.text:
            text = table.text[2:]
    
    time.sleep(1)

    close_button = wd.find_elements_by_class_name('t-text-4xl')
    for i in range(len(close_button)):
        if close_button[i].text == '×':
            close_button[i].click()
        
    wd.close()
    time.sleep(1)
    
    return text

def make_div_dic(text):
    
    div_list = text.split('\n')[1:]
    div_dic = {}

    for el in div_list:
        
        if len(el.split(' ')[0]) == 4:
            k = el.split(' ')[0]
            div_dic[k] = []
        else:
            div_dic[k].append(el)

    for key in div_dic.keys():
        div_dic[key] = div_dic[key][2:]
        
    return div_dic

def reshape_div_dic(div_dic):
    
    for key in div_dic.keys():
        new_list = []
        prom_list = []
        for i in range(len(div_dic[key])):
            prom_list += div_dic[key][i].split(' ')
            
            if len(prom_list) == 10:
                prom_list[4] += ' ' + prom_list[5] + ' ' + prom_list[6]
                prom_list.pop(5)
                prom_list.pop(6)
            elif len(prom_list) == 9:
                prom_list[4] += ' ' + prom_list[5]
                prom_list.pop(5)

            if i % 2 != 0:
                new_list.append(prom_list)
                prom_list = []

        div_dic[key] = new_list
        
    return div_dic

def make_df(div_dic):
    
    columns = ['PAY DATE', 'DECLARED DATE', 'EX-DIVIDEND DATE', 
           'PAYOUT AMOUNT', 'QUALIFIED DIVIDEND?', 'PAYOUT TYPE', 'FREQUENCY', 'DAYS TAKEN FOR STOCK PRICE TO RECOVER']
    
    data = []

    for key in div_dic.keys():
        data += div_dic[key]      
        
    df = pd.DataFrame(data, columns=columns)
    
    for i in range(len(df)):
        df['PAYOUT AMOUNT'] = df['PAYOUT AMOUNT'].loc[i].replace('$', '')

    df['PAYOUT AMOUNT'] = df['PAYOUT AMOUNT'].astype(float)
    
    return df  