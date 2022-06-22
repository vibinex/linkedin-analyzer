import lxml as lxml
import selector as selector
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver import Keys
import lxml
import time

driver = webdriver.Chrome()
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

#DELETE LATER
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

    #SCRAPING EXPERIENCE SECTION
    experience = soup.find(lambda tag:tag.name=="section" and "Experience" in tag.text).find('ul')

    job_titles= experience.find_all("span", {'class': 'mr1 t-bold'})
    for j in job_titles:
        x = j.find("span", {'class' : 'visually-hidden'})
        job = x.get_text().strip()
        print(job)

    company_names = experience.find_all("span", {'class' : 't-14 t-normal'})
    for c in company_names:
        x = c.find("span", {'class' : 'visually-hidden'})
        company = x.get_text().strip()
        print(company)

    joining_datesANDduration = experience.find_all("span", {'class': 't-14 t-normal t-black--light'})
    var = 0
    for j in joining_datesANDduration:
        x = j.find("span", {'class' : 'visually-hidden'})
        dateANDduration = x.get_text().strip()
        if var % 2 == 0:
            joiningdate = dateANDduration.split('-')[0]
            jobduration = dateANDduration.split(' · ')[1]
            print(joiningdate)
            print(jobduration)
        var = var + 1

    #SCRAPING EDUCATION SECTION
    studentofiitk = False
    education = soup.find(lambda tag:tag.name=="section" and "Education" in tag.text).find('ul')
    school =  education.find(lambda tag:tag.name=="span" and "Indian Institute of Technology, Kanpur" in tag.text)
    # degree = education.find(lambda tag:tag.name=="span" and "Bachelor" in tag.text)
    # print(degree)
    print(school)
    if school != "[ ]":
        studentofiitk = True
    yearsof_grad = education.find_all("span", {'class': 't-14 t-normal t-black--light'})
    for y in yearsof_grad:
         x = y.find("span", {'class' : 'visually-hidden'})
         yearofschooling = x.get_text().strip()
         yearofgrad = yearofschooling.split(' - ')[1]
         print(yearofgrad)
driver.quit() x = j.find("span", {'class' : 'visually-hidden'})
        dateANDduration = x.get_text().strip()
