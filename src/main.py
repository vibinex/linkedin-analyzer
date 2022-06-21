import selector as selector
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver import Keys

driver = webdriver.Chrome()
import time
driver.get("https://linkedin.com/uas/login")

time.sleep(5)

# PATH = input("Enter the webdriver path:\n")
# EMAIL = input("Enter the email:\n")
# PASSWORD = input("Enter the password:\n")
# username = driver.find_element_by_id("username")
# pword = driver.find_element_by_id("password")
# username.send_keys(EMAIL)
# pword.send_keys(PASSWORD)
# driver = webdriver.Chrome(PATH)


username = driver.find_element_by_id("username")
username.send_keys("inika.agarwal@icloud.com")
pword = driver.find_element_by_id("password")
pword.send_keys("Keyboard1")

log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
log_in_button.click()

driver.get("https://www.google.com")
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "Indian Institute of Technology, Kanpur" AND "Pragya Jain" ')
search_query.send_keys(Keys.RETURN)

linkedin_urls = driver.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/div/a')
time.sleep(5)

company = []
jobtitle = []
jobduration = []
yearofgrad = []

for linkedin_url in linkedin_urls:
    driver.get(linkedin_url.get_attribute('href'))
    time.sleep(5)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    experience = soup.find(lambda tag:tag.name=="section" and "Experience" in tag.text).find('ul')
    job_titles= experience.find_all("span", {'class': 'mr1 t-bold'})
    experience.find_all("")
    for j in job_titles:
        x = j.find("span", {'class' : 'visually-hidden'})
        job = x.get_text().strip()
        print(job)
    driver.quit()
    # job_titles = experience.find("span", {'class': 'mr1 t-bold'}).get_text().strip()

    # company_name = li_tags.find_all("span")[1].get_text().strip()
    # print(company_name)
    #
    #    joining_date = a_tags.find_all("h4")[0].find_all("span")[1].get_text().strip()
    #
    #    employment_duration = a_tags.find_all("h4")[1].find_all("span")[1].get_text().strip()
    #
    #    print(joining_date + ", " + employment_duration)


