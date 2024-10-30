"""
data crawling using Selenium
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import subprocess

def str2num(price):
    try:
        return int(price.replace(",", "").replace(".", ""))
    except ValueError:
        return f"{price} : Invalid price format"

# Configure Selenium to use headless mode for running without opening a visible browser
options = Options()
options.headless = False  # Ensure headless mode is enabled
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

# Replace 'chromedriver' with the path to your ChromeDriver if it's not in your PATH
driver = webdriver.Chrome(options=options)

try:
    # The URL of the target website
    url = "https://www.tgju.org/"
    
    # Open the website and wait for it to load
    driver.get(url)
    time.sleep(5)  # Allow time for JavaScript to load content

    # Extract the page source after JavaScript execution
    page_source = driver.page_source

    # Clean up old file if it exists
    try:
        subprocess.run(["rm", "/home/h00man/Desktop/responses.txt"])
    except:
        pass

    # Write the page source to file for data extraction
    with open("/home/h00man/Desktop/responses.txt", 'w') as writer:
        writer.writelines(page_source)

finally:
    # Close the Selenium browser
    driver.quit()

Au_ounce, Au_shekel, Au_gram, dollar = 0, 0, 0, 0

with open("/home/h00man/Desktop/responses.txt", 'r') as reader:
    counter = 100000
    value = 10
    for line in reader.readlines():
        if '<h3><em></em> انس طلا</h3>' in line:
            counter = 0
            value = 0
        if counter == 2 and value == 0: 
            Au_ounce = (line.strip().split('<span class="info-price">')[1].split('</span>')[0].replace(",", ""))
            value = 10
            continue

        if '<h3><em></em> مثقال طلا</h3>' in line:
            counter = 0
            value = 1
        if counter == 2 and value == 1: 
            Au_shekel = (line.strip().split('<span class="info-price">')[1].split('</span>')[0].replace(",", ""))
            value = 10
            continue

        if '<h3><em></em> طلا ۱۸</h3>' in line:
            counter = 0
            value = 2
        if counter == 2 and value == 2: 
            Au_gram = (line.strip().split('<span class="info-price">')[1].split('</span>')[0].replace(",", ""))
            value = 10
            continue

        if '<h3><em></em> دلار</h3>' in line:
            counter = 0
            value = 3
        if counter == 2 and value == 3: 
            dollar = (line.strip().split('<span class="info-price">')[1].split('</span>')[0].replace(",", ""))
            value = 10
            continue

        counter += 1

def price_style(price : float):
    price = str(int(price))
    price = price[::-1]
    styled_price = str()
    for i in range(len(price)):
        styled_price += price[i]
        if (i+1) % 3 == 0 and i+1 != len(price):
            styled_price += ','
    return styled_price[::-1]

# Process prices
Au_ounce = float(Au_ounce)
Au_shekel = float(Au_shekel) / 10
Au_gram = float(Au_gram) / 10
dollar = float(dollar) / 10
Au_abroad = Au_ounce * dollar / 9.5742
delta_inout = Au_shekel - Au_abroad

# Print data
print(f"Dollar      {price_style(dollar) :<10}")
print(f"Au grm18    {price_style(Au_gram) :<10}")
print(f"Au ounce    {price_style(Au_ounce) :<10}")
print(f"Au Mesghl   {price_style(Au_shekel) :<10}")
print(f"Au WORLD    {price_style(Au_abroad) :<10}")
print('========================')
print(f"Delta       {price_style(delta_inout) :<10}")
if delta_inout > 500000:
    print(f"Process     {'Sell' :<10}")
elif delta_inout < 100000:
    print(f"Process     {'Buy' :<10}")
else:
    print(f"Process     {'Wait' :<10}")
