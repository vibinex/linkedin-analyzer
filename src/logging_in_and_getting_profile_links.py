from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import lxml





def logging_in(driver):

    driver.get("https://linkedin.com/uas/login")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "username")))
    EMAIL = input("Enter the email:\n")
    username = driver.find_element_by_id("username")
    pword = driver.find_element_by_id("password")
    PASSWORD = input("Enter the password:\n")
    username.send_keys(EMAIL)
    pword.send_keys(PASSWORD)

    log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    log_in_button.click()


def getting_profile_urls(schoolid,driver,urls):
    filter_src = driver.page_source
    filter_soup = BeautifulSoup(filter_src, 'html.parser')
    filter_urls = filter_soup.find('main', {'id':'main'}).find('ul').find_all('li')

    for filter_url in filter_urls:
        if filter_url.find('div', {'class' : 't-roman t-sans'}).find('a')['href'] != 'https://www.linkedin.com/search/results/people/headless?schoolFilter=%5B' + str(schoolid) + '%5D&origin=FACETED_SEARCH':
            urls.append(filter_url.find('div', {'class' : 't-roman t-sans'}).find('a')['href'])

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and @aria-label="Next"]')))


def getting_urls_and_clicking_next_page(schoolid,driver,urls):
    driver.get('https://www.linkedin.com/search/results/people/?origin=FACETED_SEARCH&schoolFilter=%5B%22' + str(schoolid) + '%22%5D&sid=(X1')
    loop = True
    while loop:
        getting_profile_urls(schoolid,driver,urls)

        old_url = driver.current_url

        next_button = driver.find_element_by_xpath('//button[@type="button" and @aria-label="Next"]')
        next_button.click()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "main")))

        if driver.current_url == old_url:
            loop = False
            print('All links obtained.')
