from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import time





def getting_profile_links_from_school_id(schoolid,driver,urls):
    filter_src = driver.page_source
    filter_soup = BeautifulSoup(filter_src, 'html.parser')
    filter_urls = filter_soup.find('main', {'id':'main'}).find('ul').find_all('li')

    for filter_url in filter_urls:
        if filter_url.find('div', {'class' : 't-roman t-sans'}).find('a')['href'] != 'https://www.linkedin.com/search/results/people/headless?schoolFilter=%5B' + str(schoolid) + '%5D&origin=FACETED_SEARCH':
            urls.append(filter_url.find('div', {'class' : 't-roman t-sans'}).find('a')['href'])



def getting_links_and_clicking_next_page(schoolid,driver,urls):

    driver.get('https://www.linkedin.com/search/results/people/?origin=FACETED_SEARCH&schoolFilter=%5B%22' + str(schoolid) + '%22%5D&sid=(X1')
    WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))

    page_number = 0
    starting_page = int(input('What page would you like to start at?\n'))
    page_amount = int(input('How many pages would you like to scrape?\n'))
    go = True

    while go:
        if page_number >= starting_page:
            getting_profile_links_from_school_id(schoolid,driver,urls)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and @aria-label="Next"]')))
        except:
            print('all loops obtained')
            break


        old_url = driver.current_url

        next_button = driver.find_element_by_xpath('//button[@type="button" and @aria-label="Next"]')
        next_button.click()

        WebDriverWait(driver,15).until_not(EC.url_contains(old_url))

        WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))

        page_number = page_number + 1

        if page_number == (starting_page + page_amount):
            break




