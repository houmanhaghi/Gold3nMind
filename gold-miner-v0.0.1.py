import requests
import re
from bs4 import BeautifulSoup


def str2num(price):
    try:
        return int(price.replace(",", "").replace(".", ""))
    except ValueError:
        return f"{price} : Invalid price format"


# The URL of the target website
url = "https://www.tgju.org/"

# Send a GET request to fetch the HTML content
response = requests.get(url)

# Data retreval
with open("response.txt", 'w') as writter:
    writter.writelines(response.text)

Au_ounce, Au_shekel, dollar = 0, 0, 0

with open("response.txt", 'r') as reader:
    counter = 100000
    value = 3
    for line in reader.readlines():

        if '<h3><em></em> انس طلا</h3>' in line:
            counter = 0
            value = 0

        if counter == 2 and value == 0: 
            Au_ounce = (line.strip().split('<span class="info-price">')[1].split('</span>')[0].replace(",", ""))
            value = 3
            continue
            

        if '<h3><em></em> مثقال طلا</h3>' in line:
            counter = 0
            value = 1

        if counter == 2 and value == 1: 
            Au_shekel = (line.strip().split('<span class="info-price">')[1].split('</span>')[0].replace(",", ""))
            value = 3
            continue
            


        if '<h3><em></em> دلار</h3>' in line:
            counter = 0
            value = 2

        if counter == 2 and value == 2: 
            dollar = (line.strip().split('<span class="info-price">')[1].split('</span>')[0].replace(",", ""))
            value = 3
            continue
            

        counter += 1


def price_style(price : float):
    price = str(int(price))
    price = price[::-1]
    styled_price = str()
    for i in range(len(price)):
        styled_price = styled_price + price[i]
        if (i+1) % 3 == 0 and i+1 != len(price):
            styled_price = styled_price + ','
    return styled_price[::-1]



Au_ounce = float(Au_ounce)
Au_shekel = float(Au_shekel) / 10
dollar = float(dollar) / 10
Au_abroad = Au_ounce * dollar / 9.5742
delta_inout = Au_shekel - Au_abroad

# Print data
print(f"Dollar      {price_style(dollar) :<10}")
print(f"Au ounce    {price_style(Au_ounce) :<10}")
print(f"Au IRAN     {price_style(Au_shekel) :<10}")
print(f"Au WORLD    {price_style(Au_abroad) :<10}")
print('========================')
print(f"Delta       {price_style(delta_inout) :<10}")
if delta_inout > 500000:
    print(f"Process     {'Sell' :<10}")
elif delta_inout < 100000:
    print(f"Process     {'Buy' :<10}")
else:
    print(f"Process     {'Wait' :<10}")
