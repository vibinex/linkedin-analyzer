import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys



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
