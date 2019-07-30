from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re

# crawler for downloading data from website  "https://skyscraperpage.com/cities/"

def retrieve_urls(main_url):
    urls = []
    html = urlopen(main_url).read().decode("utf-8")
    soup = bs(html, features="lxml") 
    city_list = soup.find_all('td') 
    
    for city in city_list:
        city_urls = city.find_all('a', href=True)
        for city_url in city_urls:
            if re.search(r'^\/cities\/', city_url['href']):
                urls.append(city_url['href'])
    return urls

def city_parser(table_list):
    buildings = {} 
    trs = table_list[0].find_all('tr')
    idx = 0 
    for tr in trs:
        building_name = ""
        floor = 0
        if idx%2 == 0:
            tds = tr.find_all('td')
            n = 0
            for td in tds:
                #print(str(n) + td.get_text())
                if n == 1 and td.get_text() != "Name":
                    building_name = td.get_text()
                if n==3 and td.get_text() != "Floors":
                    floor = td.get_text()
                n+=1
            if building_name != "":
                buildings[building_name] = floor
    return buildings 
    


if __name__ == "__main__":
    
    #chinese cities
    main_url = "https://skyscraperpage.com/database/country/3"
    base_url = "https://skyscraperpage.com"
    urls = []
    cityNames = []
    i = 0 
    urls = retrieve_urls(main_url)
    for url in urls:
        #urls.append(main_url+"?cityID="+ str(i+1))
        url = base_url+url
        print(url)
        html = urlopen(url).read().decode('utf-8')
        res = re.findall(r"<title>(.+?)</title>", html)
        cityNames.append (res[0].split(' ')[0].strip())
        print("page title is ", cityNames[i])
        f_name = cityNames[i]
        buildings = {}
        soup = bs(html, features = 'lxml')
        table_list = soup.find_all("table", {"class":"list"})
        if len(table_list) > 1:
            pages = table_list[1].find_all("a", {"class", "bhu"})
            page_urls = []
            for page in pages:
                page_urls.append(main_url + page["href"])
            page_urls = set(page_urls)

            if len(table_list)> 0:
                buildings = city_parser(table_list)
                for page_url in page_urls:
                    new_html = urlopen(page_url).read().decode('utf-8')
                    new_soup = bs(new_html, features = "lxml")
                    new_table_list = new_soup.find_all("table", {"class":"list"})
                    new_dic = {}
                    if len(new_table_list)>0:
                        new_dic = city_parser(new_table_list)
                        buildings = {**buildings , **new_dic}
                with open(f_name, "w+") as f:
                    for building in buildings:
                        f.write(building + "\t" + buildings[building]+ "\n")
            
        i+=1                                       