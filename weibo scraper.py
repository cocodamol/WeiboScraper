from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def login(username, password):
    driver.get('https://www.weibo.com/')
    usernameBox = WebDriverWait(driver, 60).until(EC.visibility_of_element_located
                                                  ((By.XPATH, '//*[@id="loginname"]')))
    usernameBox.send_keys(username)
    passwordBox = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
    passwordBox.send_keys(password)
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
    time.sleep(15)


def scroll():
    SCROLL_PAUSE_TIME = 8
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_feeds():
    html = driver.page_source
    soup = BeautifulSoup(html,"lxml")
    feeds = soup.find_all("div", {"action-type": "feed_list_item"})
    return feeds


def scrape(feeds):
    with open("output.txt", 'a', encoding='utf-8-sig') as f:
        for feed in feeds:
            post = feed.find("div", {"class": "WB_text W_f14"}).text.strip()
            forward = feed.find("em", {"class": "W_ficon ficon_forward S_ficon"}).find_next('em').text.strip()
            comment = feed.find("em", {"class": "W_ficon ficon_repeat S_ficon"}).find_next('em').text.strip()
            like = feed.find("em", {"class": "W_ficon ficon_praised S_txt2"}).find_next('em').text.strip()
            date = feed.find("div",attrs={"class": "WB_from S_txt2"}).find('a')['title']
            link = feed.find("div",attrs={"class": "WB_from S_txt2"}).find('a')['href'].split('?')[0]
            link = 'https://www.weibo.com'+str(link)
            row = "{}|{}|{}|{}|{}|{}\n".format(post, forward, comment, like, date, link)
            print(row)
            f.write(row)


if __name__ == "__main__":
    username = ""
    # replace with username
    password = ""
    # replace with password
    accountname = ''
    # replace with account ID you'd like to scrape  
    accountURL = 'https://www.weibo.com/{}?profile_ftype=1&is_all=1#_0'.format(accountname)
    driver = webdriver.Chrome()
    start_page = 1
    end_page = 6
    login(username, password)

    if start_page == 1:
        driver.get(accountURL)
        scroll()
        scrape(get_feeds())
        cur = start_page + 1
    else:
        cur = start_page

    while cur <= maxpage-1:
        cur = cur + 1
        driver.get('https://www.weibo.com/{}?&page={}'.format(accoutname, cur))
        time.sleep(20)
        scroll()
        scrape(get_feeds())
