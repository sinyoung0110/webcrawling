# 크롤링을 위한 셀레니움
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 데이터 프레임 작성을 위한 판다스
import pandas as pd

# 대기시간을 휘한 라이브러리
import random
import time

def croll():
    for x in range(1, 101):
        try:
            driver.find_element(By.XPATH, f'//*[@id="divContent"]/div/div[2]/div/div[3]/div[2]/ul/li[{x}]/div[2]/p[1]/a').send_keys(Keys.CONTROL+"\n")
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
        except:
            break

        try:
            title = driver.find_element(By.CSS_SELECTOR, '#thesisInfoDiv > div.thesisInfoTop > h3').text
        except:
            title = None

        try:
            date  = driver.find_element(By.CSS_SELECTOR, '#thesisInfoDiv > div.infoDetail.on > div.infoDetailL > ul > li:nth-child(5) > div > p').text
        except:
            date = None
        
        try:
            abstract_text = driver.find_element(By.CSS_SELECTOR, '#additionalInfoDiv > div > div:nth-child(1) > p').text
            if abstract_text == '국문 초록 (Abstract)':
                driver.find_element(By.CSS_SELECTOR, '#additionalInfoDiv > div > div:nth-child(1) > a').click()
                time.sleep(0.2)
                abstract = driver.find_element(By.CSS_SELECTOR, '#additionalInfoDiv > div > div:nth-child(1) > div:nth-child(5) > p').text
                try:
                    driver.find_element(By.CSS_SELECTOR, '#additionalInfoDiv > div > div:nth-child(2) > a').click()
                    time.sleep(0.2)
                    multi_abstract = driver.find_element(By.CSS_SELECTOR, '#additionalInfoDiv > div > div:nth-child(2) > div:nth-child(5) > p').text
                except:
                    multi_abstract = None
            elif abstract_text == '다국어 초록 (Multilingual Abstract)':
                driver.find_element(By.CSS_SELECTOR, '#additionalInfoDiv > div > div:nth-child(1) > a').click()
                time.sleep(0.2)
                multi_abstract =driver.find_element(By.CSS_SELECTOR, '#additionalInfoDiv > div > div:nth-child(1) > div:nth-child(5) > p').text
                try:
                    driver.find_element(By.CSS_SELECTOR, '#additionalInfoDiv > div > div:nth-child(2) > a').click()
                    time.sleep(0.2)
                    abstract = driver.find_element(By.CSS_SELECTOR, '#additionalInfoDiv > div > div:nth-child(2) > div:nth-child(5) > p').text
                except:
                    abstract = None
            else:
                abstract = None
                multi_abstract = None
        except:
            abstract = None
            multi_abstract = None
        
        titles.append(title)
        dates.append(date)
        abstracts.append(abstract)
        multi_abstracts.append(multi_abstract)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1.5)


# 크롤링한 논문 설정
search = input('검색할 단어를 입력 : ')
year = input('지금으로부터 몇년 전의 논문을 가져올지 입력 : ')
time.sleep(2)

# 크롬 드라이버를 실행하고 메인페이지 실행
driver = webdriver.Chrome()
driver.get('https://www.riss.kr/index.do')
time.sleep(3)

# 원하는 키워드로 논문을 검색
driver.find_element(By.XPATH, '//*[@id="query"]').click()
driver.find_element(By.XPATH, '//*[@id="query"]').send_keys(search)
driver.find_element(By.CSS_SELECTOR, '#in > div > button').click()
time.sleep(3)

# 학술논문 페이지로 넘어가기
driver.find_element(By.CSS_SELECTOR, '#divContent > div > div > div.srchResultW.totalSrch > div:nth-child(1) > div.topRight > a > img').click()
time.sleep(3)

# 년도 설정
driver.find_element(By.CSS_SELECTOR, f'#mCSB_7_container > li:nth-child({year}) > label > span.checkBox').click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, f'#mCSB_7_container > li:nth-child({year}) > a').click()
time.sleep(3)

# 논문을 100개씩 보기로 설정
driver.find_element(By.XPATH, '//*[@id="divContent"]/div/div[2]/div/div[3]/div[1]/div[2]/div[3]/div[1]/label').click()
time.sleep(0.3)
driver.find_element(By.XPATH, '//*[@id="divContent"]/div/div[2]/div/div[3]/div[1]/div[2]/div[3]/div[2]/div/ul/li[5]/a').click()
time.sleep(0.3)
driver.find_element(By.XPATH, '//*[@id="divContent"]/div/div[2]/div/div[3]/div[1]/div[2]/button').click()
time.sleep(3)

# 페이지 수 계산
thesis_num = driver.find_element(By.XPATH, '//*[@id="divContent"]/div/div[2]/div/div[1]/dl/dd/span/span').text
thesis_num = int(thesis_num[:].replace(',',''))
page_num = thesis_num // 100 + 1
print('추출할 논문의 수 : ',thesis_num)

# 자료들을 모아둘 리스트 선언
titles = []
dates = []
abstracts = []
multi_abstracts = []

# 첫 페이지 크롤링
croll()

# 나머지 페이지 크롤링
for p in range(2, page_num+1):
    try:
        if p <= 10:
            driver.find_element(By.XPATH, f'//*[@id="divContent"]/div/div[2]/div/div[4]/a[{p+1}]').click()
        else:
            if p == 11:
                driver.find_element(By.XPATH, '//*[@id="divContent"]/div/div[2]/div/div[4]/a[12]').click()
            elif p % 10 == 1:
                driver.find_element(By.XPATH, '//*[@id="divContent"]/div/div[2]/div/div[4]/a[13]').click()
            else:
                if p % 10 == 0:
                    driver.find_element(By.XPATH, '//*[@id="divContent"]/div/div[2]/div/div[4]/a[12]').click()
                else:
                    driver.find_element(By.XPATH, f'//*[@id="divContent"]/div/div[2]/div/div[4]/a[{p%10+2}]').click()
        time.sleep(3)
        if p % 3 == 0:
            time.sleep(random.randint(5,7))
        croll()
    except:
        break

# 크롤링한 데이터로 데이터 프레임 생성
data = pd.DataFrame({
    'title' : titles,
    'date' : dates,
    'abstract' : abstracts,
    'multilingual' : multi_abstracts
})
    

# 데이터 프레임 저장
now = str(time.strftime('%Y_%m_%d_%H_%M_%S'))
csv_file_path = f'{now}___riss_academic.csv'
data.to_csv(csv_file_path, index=False)

# 드라이버 종료
driver.close()

print('추출한 논문의 수 : ', len(titles))