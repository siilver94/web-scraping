from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('window-size=1920x1080')

browser = webdriver.Chrome(
    'C:\\Users\Vector\Desktop\PythonWorkSpace\.vscode\webscraping_basic\chromedriver.exe', options=options)
browser.maximize_window()

url = 'https://play.google.com/store/movies/top'
browser.get(url)


interval = 2  # 2초에 한번씩 스크롤 내림

#현재 문서 높이를 가져와서 저장
prev_height = browser.execute_script('return document.body.scrollHeight')

#반복 수행from bs4 import BeautifulSoup
while True:
    #스크롤을 가장 아래로 내림
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')

    #페이지 로딩 대기
    time.sleep(interval)

    curr_height = browser.execute_script('return document.body.scrollHeight')
    if curr_height == prev_height:
        break

    prev_height = curr_height

print('스크롤 완료')

browser.get_screenshot_as_file('google_movie.png')  # 스크린샷

res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(browser.page_source, "lxml")

# movies = soup.find_all('div', attrs={'class': ['ImZGtf mpg5gc','Vpfmgd']})
movies = soup.find_all('div', attrs={'class': 'Vpfmgd'})
#영화 갯수
print(len(movies))

for movie in movies:
    title = movie.find('div', attrs={'class': 'WsMG1c nnK0zc'}).get_text()
    #print(title)

    #할인 전 가격
    original_price = movie.find('span', attrs={'class': 'SUZt4c djCuy'})
    if original_price:
        original_price = original_price.get_text()
    else:
        #print(title, '할인되지 않는 영화는 제외')
        continue
    #할인된 가격
    price = movie.find(
        'span', attrs={'class': 'VfPpfd ZdBevf i5DZme'}).get_text()

    #링크로 이동
    link = movie.find('a', attrs={'class': 'JC71ub'})['href']
    # 올바른 링크 : https://play.google.com + link

    print(f'제목 : {title}')
    print(f'할인 전 금액 : {original_price}')
    print(f'할인 후 금액 : {price}')
    print(f'링크 :', 'https://play.google.com' + link)
    print('-'*100)

    browser.quit()
