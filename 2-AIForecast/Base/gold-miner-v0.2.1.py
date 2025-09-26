from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import subprocess

def str2num(price):
    try:
        return int(price.replace(",", "").replace(".", ""))
    except ValueError:
        return f"{price} : Invalid price format"


def price_style(price : float):
    price = str(int(price))
    price = price[::-1]
    styled_price = str()
    for i in range(len(price)):
        styled_price += price[i]
        if (i+1) % 3 == 0 and i+1 != len(price):
            styled_price += ','
    return styled_price[::-1]



def day_max_delta():
    max_delta_of_day = 0
    Au_grm18_avg_list = list()
    now = time.time()

    with open("delta.txt", 'r') as delta_reader:
        for line in delta_reader.readlines():
            saved_time, value = line.strip().split(':')
            saved_delta, saves_Au_gram = value.strip().split(';')
            saved_time = float(saved_time.strip())
            saved_delta = float(saved_delta.strip())
            saves_Au_gram = float(saves_Au_gram.strip())
            Au_grm18_avg_list.append(saves_Au_gram)

            if now < saved_time + 86400:
                if saved_delta > max_delta_of_day:
                    max_delta_of_day = saved_delta

    Au_grm18_avg = sum(Au_grm18_avg_list) / len(Au_grm18_avg_list) if Au_grm18_avg_list else 0
    return max_delta_of_day, Au_grm18_avg


def recommandation(delta : float, maximum = 500000):
    maximize = maximum
    maximize_diff = maximum / 10
    global Au_gram
    alert = str()

    # check if over max
    if delta > maximum:
        if delta - maximum > maximize_diff:
            maximize = delta - maximize_diff

    # precess over chart
    max_delta_day , Au_grm18_avg = day_max_delta()

    if max_delta_day != 0 :
        if delta < max_delta_day:
            maximize = max_delta_day - maximize_diff

    else:
        print("No Day Data History")

    if Au_grm18_avg > Au_gram and (maximize - delta > 1.8 * maximize_diff) : 
        print(f"Sell Urgentely")
    
    elif Au_grm18_avg > Au_gram and (maximize - delta > 1.2 * maximize_diff) : 
        print(f"Sell Preferably")

    elif Au_grm18_avg > Au_gram and (maximize - delta > 0.8 * maximize_diff) : 
        print(f"Sell Recommandly")
    else:
        print("No Selling Recommand")
 



# Configure Selenium to use headless mode for running without opening a visible browser
options = Options()
options.headless = True
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

# Process prices
Au_ounce = float(Au_ounce)
Au_shekel = float(Au_shekel) / 10
Au_gram = float(Au_gram) / 10
dollar = float(dollar) / 10
Au_abroad = Au_ounce * dollar / 9.5742
delta_inout = Au_shekel - Au_abroad

# save delta
with open("delta.txt", 'a') as delta_adder:
    delta_adder.writelines(f"{time.time() :<15} : {delta_inout :<15}; {Au_gram :<15}\n")

       
# Print data
print(f"Dollar      {price_style(dollar) :<10}")
print(f"Au Grm18    {price_style(Au_gram) :<10}")
print(f"Au Ounce    {price_style(Au_ounce) :<10}")
print(f"Au Mesghl   {price_style(Au_shekel) :<10}")
print(f"Au WORLD    {price_style(Au_abroad) :<10}")
print('=======================')
print(f"Delta       {price_style(delta_inout) :<10}")
if delta_inout > 500000:
    print(f"Mode        {'Sell' :<10}")
elif delta_inout < 100000:
    print(f"Mode        {'Buy' :<10}")
else:
    print(f"Mode        {'Wait' :<10}")
print('=======================')    
recommandation(delta_inout)
print('=======================')
