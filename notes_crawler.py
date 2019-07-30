from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re
import requests



if __name__ == "__main__":
    
    main_url = "https://cims.nyu.edu/~cfgranda/pages/DSGA1002_fall15/notes.html"
    html = urlopen(main_url).read().decode('utf-8')

    soup = bs(html, features = 'lxml')
    url_containers = soup.find_all('p')    
    for url_container in url_containers:
        sub_urls = url_container.find_all("a", href = True)
        for sub_url in sub_urls: 
            url = "https://cims.nyu.edu/~cfgranda/pages/DSGA1002_fall15/" + sub_url['href']
            r = requests.get(url, stream = True)
            name =  sub_url['href'].split('/')[-1]
            with open('%s' % name, 'wb') as f:
                for chunk in r.iter_content(chunk_size = 128):
                    f.write(chunk)
            print('saved %s' % name)
