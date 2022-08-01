import requests, config
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import os,re,csv
import time
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings, random, string
warnings.filterwarnings("ignore", category=DeprecationWarning) 
cwd = os.getcwd()
opts = webdriver.ChromeOptions()
 
opts.headless = True
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--disable-setuid-sandbox')
opts.add_argument('--log-level=3') 
opts.add_argument('--disable-infobars')
opts.add_argument('--no-sandbox')
opts.add_argument('--ignore-certifcate-errors')
opts.add_argument('--ignore-certifcate-errors-spki-list')
opts.add_argument("--incognito")
opts.add_argument('--no-first-run')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument("--disable-infobars")
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option("useAutomationExtension", False)
opts.add_experimental_option("excludeSwitches",["enable-automation"])
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
opts.add_argument('--disable-notifications')
 
def xpath_type(el,mount):
    return wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)

def xpath_el(el):
    element_all = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el)))

    # browser.execute_script("arguments[0].scrollIntoView();", element_all)
    
    
    return browser.execute_script("arguments[0].click();", element_all)

def scrape(link_hotel):
    global browser
    try:
        try:
            browser = webdriver.Chrome(options=opts, desired_capabilities=dc)
            browser.get(link_hotel)
        except:
            sleep(1)
            pass
        try:
            xpath_el('//*[text()="Lanjutkan pencarian di situs mobile"]')
        except:
            pass

        hotel_name =  wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//*[@data-id="hotel.hotelName"]'))).text
        hotel_address = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hotelAppContent"]/div/div/div[3]/div[1]/div[2]/div[2]/span'))).text
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Name: {hotel_name}")
        response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={hotel_address}&key={config.api_key}')

        resp_json_payload = response.json()

        hotel_lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Latitude: {hotel_lat}")
        hotel_long = resp_json_payload['results'][0]['geometry']['location']['lng']
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Latitude: {hotel_long}")
        hotel_city =str(resp_json_payload['results'][0]['address_components']).split("['administrative_area_level_3', 'political']}, {'long_name': '")[1].split("', 'short_name': '")[0]
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel City: {hotel_city}")
        hotel_province = str(resp_json_payload['results'][0]['address_components']).split("['administrative_area_level_2', 'political']}, {'long_name': '")[1].split("', 'short_name': '")[0]
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Province: {hotel_province}")
        hotel_rate = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//span[@class="SqmyI"]'))).text
        hotel_rate = float(hotel_rate)/2
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Rate: {hotel_rate}")
        hotel_star = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//meta[@itemprop="ratingValue"]'))).get_attribute('content')
        hotel_size =  wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "(//*[contains(text(),'m2')])[1]"))).text
        hotel_size = hotel_size.split(' m2')[0]
        hotel_size = hotel_size.split(".0")[0]
        hotel_size = re.findall(r'\d+',hotel_size)
        hotel_size = hotel_size[0]
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Size: {hotel_size}")
        
        hotel_capacity =  wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '(//*[@dir="auto" and contains(text(),"Tamu")])'))).text
        hotel_capacity = re.findall(r'\d+',hotel_capacity)
        hotel_capacity = sum(int(n) for n in hotel_capacity)
        
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Capacity: {hotel_capacity}")
        
        hotel_price =  wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "(//*[@aria-level='3' and contains(text(),'Rp ')])[1]"))).text
        hotel_price = hotel_price.replace(".",'').replace('Rp ','')

        scroller = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Review Terbaik']")))
        browser.execute_script("arguments[0].scrollIntoView();", scroller)
        scroller = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Lihat Semua Fasilitas']")))
        browser.execute_script("arguments[0].scrollIntoView();", scroller)
        scroller = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "//*[text()='TEMPAT TERDEKAT']")))
        browser.execute_script("arguments[0].scrollIntoView();", scroller)
        scroller = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Deskripsi']")))
        browser.execute_script("arguments[0].scrollIntoView();", scroller)
        try:
            hotel_pict = wait(browser,2).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="react-swipeable-view-container"]//img)[2]')))
            browser.execute_script("arguments[0].scrollIntoView();", hotel_pict)
            hotel_pict = hotel_pict.get_attribute('src')
        except:
            hotel_pict = 'none'
        xpath_el('(//*[text()="Lihat Rincian"])[1]')
        try:
            xpath_el('(//*[text()="Fasilitas Kamar Lainnya"])[1]')
        except:
            pass
        hotel_desc = wait(browser,15).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="hotelAppContent"]/div/div/div[3]/div[6]/div/div[1]/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div')))
        hotel_collect_desc = ','.join([x.text for x in hotel_desc if x.text != ""])
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Description: {hotel_collect_desc}")
        hotel_type_room = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hotelAppContent"]/div/div/div[3]/div[6]/div/div[1]/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]'))).text
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Type: {hotel_type_room}")
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Price (RP): {hotel_price}")
        print(f"[{time.strftime('%d-%m-%y %X')}] Hotel Star: {hotel_star}")
        with open('saved.txt','a') as f:
            f.write('{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}\n'.format(hotel_name, hotel_address, hotel_city, hotel_province, hotel_type_room, hotel_collect_desc,hotel_rate,hotel_star,hotel_pict))
        browser.quit()
    except Exception as e:
        print(e)
        try:
            browser.quit()
        except:
            pass
         
def main():
  
    
    opts.add_argument(f"user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36")
    
    link_hotel = []
    print(f"[{time.strftime('%d-%m-%y %X')}] Trying to Scrape Source Hotel")
    file_list_akun = "link.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    
    akun = myfile_akun.read()

    list_accountsplit = akun.split("\n")
            
                    
    with Pool(5) as p:  
        p.map(scrape, list_accountsplit)      
    
if __name__ == '__main__':
  
    print(f"[{time.strftime('%d-%m-%y %X')}] Automation Scrapper Hotel")
    
    main()
    
