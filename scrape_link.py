import requests
from requests_html import HTMLSession
from multiprocessing import Pool
import time
 
def main(id):   
    
    session = HTMLSession()   
    
    print(f"[{time.strftime('%d-%m-%y %X')}] Trying to Scrape Source Hotel")
    err = 1
    link_hotel = []
    for i in range(1,120):
        if err == 5:
            break
        try:
            response = session.get(f'https://m.traveloka.com/id-id/hotel/search/GEO.{id}.2.29-07-2022.30-07-2022?guests=1&rooms=1&skip={i}-nextg')
        except:
            sleep(1)
            pass
        try:
            get_all_link = response.html.xpath('(//div[@class="tvat-hotelList"]/div/a)/@href')
            
            for hotel in get_all_link:
                link_hotel.append(hotel)
                print(f"[{time.strftime('%d-%m-%y %X')}] {hotel}")
                with open('link.txt','a') as f:
                    f.write(f'{hotel}\n')
        except:
            err = err + 1
 
    
if __name__ == '__main__':
  
    print(f"[{time.strftime('%d-%m-%y %X')}] Automation Scrapper Hotel")
    list_id_location = ['107816','107782','107824','102813','103890','102746','103760','103859','107442','103570','107703','103245','106469']

    with Pool(5) as p:  
        p.map(main, list_id_location)      
    
