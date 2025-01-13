# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from selenium.webdriver.common.by import By

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time
import random

# 데이터프레임을 다루기 위한 pandas import
import pandas as pd

# 크롷링하는 함수
def croll():
    for i in range(1, 102):
        if i == 6:
            continue
        try:
            driver.find_element(By.XPATH, f'/html/body/main/article[2]/section/section[2]/section[2]/article[{i}]/section[1]/section[2]/article/a/h2').click()
        except:
            break
        
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)
        
        try:
            title = driver.find_element(By.XPATH, '//*[@id="thesisTitle"]').text
        except:
            title = None

        try:
            date = driver.find_element(By.CSS_SELECTOR, '#dpMain > section > section.thesisDetail__info > section.thesisDetail__journal > ul > li:nth-child(4) > span:nth-child(1)').text
        except:
            try:
                date = driver.find_element(By.CSS_SELECTOR, '#dpMain > section > section.thesisDetail__info > section.thesisDetail__journal.projectDetail__journal > ul > li:nth-child(2) > p.projectDetail__advisoir__desc').text
            except:
                date = None
        
        try:
            abstract = driver.find_element(By.CSS_SELECTOR, '#dpMain > section > section.thesisDetail__abstract > div.abstractTxt').text
        except:
            try:
                abstract = driver.find_element(By.CSS_SELECTOR, '#dpMain > section > section.thesisDetail__abstract > div').text
            except:
                abstract = None
        
        titles.append(title)
        dates.append(date)
        abstracts.append(abstract)
        
        time.sleep(1.5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1.5)
        if i % 3 == 0:
            time.sleep(random.randint(3,7))


# 논문 검색 설정
search = input('검색할 키워드 : ')
min_year = input('추출할 최소 년도를 입력 : ')
max_year = input('추출할 최대 년도를 입력 : ')
time.sleep(1)

# 크롬드라이버 및 메인페이지 실행
driver = webdriver.Chrome()
driver.get('https://www.dbpia.co.kr/')

# 페이지가 완전히 로딩되도록 5초동안 기다림
time.sleep(5)

# 설정한 키워드로 검색
driver.find_element(By.XPATH, '//*[@id="searchInput"]').click()
time.sleep(0.5)
driver.find_element(By.XPATH, '//*[@id="searchInput"]').send_keys(search)
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="submitSearchInput"]').click()
time.sleep(3)

# 페이지를 100개씩 보기로 설정
driver.find_element(By.XPATH, '//*[@id="selectTitle"]').click()
driver.find_element(By.XPATH, '//*[@id="get100PerPage"]').click()
time.sleep(3)

# 페이지를 불러올 년도 설정
driver.find_element(By.XPATH, '//*[@id="yearRangeMin"]').click()
driver.find_element(By.XPATH, '//*[@id="yearRangeMin"]').send_keys(min_year)
time.sleep(0.3)
driver.find_element(By.XPATH, '//*[@id="yearRangeMax"]').click()
driver.find_element(By.XPATH, '//*[@id="yearRangeMax"]').send_keys(max_year)
time.sleep(0.3)
driver.find_element(By.XPATH, '//*[@id="yearRangeSearch"]').click()
time.sleep(3)

# 페이지 수 게산
article_num = driver.find_element(By.XPATH, '//*[@id="totalCount"]').text
article_num = int(article_num[:-1].replace(',',''))
page_num = article_num // 100 + 1
print('추출할 논문의 수 : ', article_num)

# 정보를 저장해둘 리스트 선언
titles = []
dates = []
abstracts = []

# 첫 페이지 크롤링
croll()

# 나머지 페이지 크롤링
for x in range(2,page_num+1):
    try:
        if x % 10 == 1:
            driver.find_element(By.XPATH, '//*[@id="goNextPage"]').click()
        else:
            if x % 10 ==0:
                driver.find_element(By.XPATH, '//*[@id="pageList"]/a[10]').click()
            else:
                driver.find_element(By.XPATH, f'//*[@id="pageList"]/a[{x%10}]').click()
        time.sleep(random.randint(5,7))
        if x % 5 == 0:
            time.sleep(random.randint(10, 15))
        croll()
    except:
        break

# 데이터 프레임 생성
data = pd.DataFrame({
    'title' : titles,
    'date' : dates,
    'abstract' : abstracts
})
    

# 데이터 프레임을 csv 형태로 저장
now = str(time.strftime('%Y_%m_%d_%H_%M_%S'))
csv_file_path = f'{now}___dbpia.csv'
data.to_csv(csv_file_path, index=False)

driver.close()
print('추출한 논문의 수 : ', len(titles))
