import pandas as pd
import yfinance as yf
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.style.use('seaborn')

# download quarterly data table
def download_quarterly_data(ticker, data_type):

    data = pd.read_excel(f'./data/{ticker}_quarterly_{data_type}_report.xlsx')
    data.index = data['values in Millions, USD']
    data = data.drop(columns=['values in Millions, USD'])

    return data


############################################################################################
########################################STOCK PRICE#########################################
############################################################################################


def stock_price(ticker):
    data = yf.download(ticker, '2020-01-01')
    fig, ax = plt.subplots(figsize=(20, 12))

    ax.plot(data.index, data['Close'])
    ax.set_title(f"{ticker} daily stock's price", fontsize=22)
    ax.set_xlabel('Dates')
    ax.set_ylabel('$')

    plt.savefig(f"./graphs/{ticker} daily stock's price")
    plt.show()


############################################################################################
################################REVENUE AND NET INCOME######################################
############################################################################################


def quarterly_total_revenue(ticker):
    data = download_quarterly_data(ticker, 'income statments')
    fig, ax = plt.subplots(figsize=(20, 12))

    x = data.columns[::-1]
    y = data.iloc[0][::-1]

    ax.plot(x, y)
    ax.set_title(f"{ticker} quarterly total revenue (last 8 quarters)", fontsize=22)
    ax.set_xlabel('Dates')
    ax.set_ylabel(data.index.name)

    for x_0, y_0 in zip(x, y):
        ax.text(x_0, y_0 + 0.09, '%d' % y_0, ha='center', va='bottom')
    
    plt.savefig(f"./graphs/{ticker} quarterly total revenue (last 8 quarters)")
    plt.show()


def quarterly_net_income(ticker):
    data = download_quarterly_data(ticker, 'income statments')
    fig, ax = plt.subplots(figsize=(20, 12))

    x = data.columns[::-1]
    y = data.iloc[-6][::-1]

    ax.bar(x, y)
    ax.set_title(f"{ticker} quarterly net income (last 8 quarters)", fontsize=22)
    ax.set_xlabel('Dates')
    ax.set_ylabel(data.index.name)

    for x_0, y_0 in zip(x, y):
        if y_0 >= 0:
            ax.text(x_0, y_0 + 0.05, '%d' % y_0, ha='center', va='bottom')
        else:
            ax.text(x_0, y_0 - 0.05, '%d' % y_0, ha='center', va='top')

    plt.savefig(f"./graphs/{ticker} quarterly net income (last 8 quarters)")
    plt.show()


def quarterly_gross_margine(ticker):
    data = download_quarterly_data(ticker, 'income statments')
    fig, ax = plt.subplots(figsize=(20, 12))

    x = data.columns[::-1]
    y = data.iloc[2][::-1] / data.iloc[0][::-1] * 100

    ax.plot(x, y)
    ax.set_title(f"{ticker} gross margin in % (last 8 quarters)", fontsize=22)
    ax.set_xlabel('Dates')
    ax.set_ylabel('%')

    for x_0, y_0 in zip(x, y):
        ax.text(x_0, y_0 + 0.09, f'{round(y_0, 2)}', ha='center', va='bottom')

    plt.savefig(f"./graphs/{ticker} gross margin in % (last 8 quarters)")
    plt.show()


def quarterly_operating_margine(ticker):
    data = download_quarterly_data(ticker, 'income statments')
    fig, ax = plt.subplots(figsize=(20, 12))

    x = data.columns[::-1]
    y = data.iloc[7][::-1] / data.iloc[0][::-1] * 100

    ax.plot(x, y)
    ax.set_title(f"{ticker} operating margin in % (last 8 quarters)", fontsize=22)
    ax.set_xlabel('Dates')
    ax.set_ylabel('%')

    for x_0, y_0 in zip(x, y):
        ax.text(x_0, y_0 + 0.09, f'{round(y_0, 2)}', ha='center', va='bottom')

    plt.savefig(f"./graphs/{ticker} operating margin in % (last 8 quarters)")
    plt.show()

############################################################################################
#######################################CASH FLOWS###########################################
############################################################################################


def cash_flow_plot(ticker, cash_flow_type):
    data = download_quarterly_data(ticker, 'cash flow')
    fig, ax = plt.subplots(figsize=(20, 12))

    x = data.columns[::-1]

    if cash_flow_type == 'operating':
        y = data.iloc[6][::-1]
    elif cash_flow_type == 'investing':
        y = data.iloc[9][::-1]
    elif cash_flow_type == 'financing':
        y = data.iloc[-7][::-1]
    elif cash_flow_type == 'net':
        y = data.iloc[6][::-1] + data.iloc[9][::-1] + data.iloc[-7][::-1]
    elif cash_flow_type == 'OCF - ICF':
        y = data.iloc[6][::-1] - data.iloc[9][::-1]

    ax.bar(x, y)
    ax.set_title(f"{ticker} {cash_flow_type} cash flow (last 8 quarters)", fontsize=22)
    ax.set_xlabel('Dates')
    ax.set_ylabel(data.index.name)

    for x_0, y_0 in zip(x, y):
        if y_0 >= 0:
            ax.text(x_0, y_0 + 0.05, '%d' % y_0, ha='center', va='bottom')
        else:
            ax.text(x_0, y_0 - 0.05, '%d' % y_0, ha='center', va='top')

    plt.savefig(f"./graphs/{ticker} {cash_flow_type} cash flow (last 8 quarters)")
    plt.show()


def quarterly_operating_cash_flow(ticker):
    cash_flow_plot(ticker, 'operating')


def quarterly_investing_cash_flow(ticker):
    cash_flow_plot(ticker, 'investing')    


def quarterly_financing_cash_flow(ticker):
    cash_flow_plot(ticker, 'financing')


def quarterly_net_cash_flow(ticker):
    cash_flow_plot(ticker, 'net')


def quarterly_ocf_icf(ticker):
    cash_flow_plot(ticker, 'OCF - ICF')
