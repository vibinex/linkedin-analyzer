import selector as selector
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver import Keys
import lxml
import time
import pandas
import datetime


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

# driver.get("https://www.google.com")
# search_query = driver.find_element_by_name('q')
# search_query.send_keys('site:linkedin.com/in/ AND "Indian Institute of Technology, Kanpur" AND "Pragya Jain" ')
# search_query.send_keys(Keys.RETURN)

# linkedin_urls = driver.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/div/a')
# time.sleep(5)

linkedin_urls = ['https://www.linkedin.com/in/pragyajain73/?originalSubdomain=in']
collegesyearofgrad = []
colleges = []
degrees = []
collegesyearofjoining = []
collegesduration = []

firstjobtitles = []
firstjobdurations = []
firstjobcompanies = []
firstjobjoiningdates = []
firstjobleavingdates = []

count = 0


def removeFullTime(text):
    temp = text.split()
    for t in temp:
        if t == 'Full-time':
            if (text.replace('Full-time · ', '')) == None:
                return text.replace(' · Full-time', '')
            else:
                return text.replace('Full-time · ', '')


def convertingMonthToNumber(month):
    datetime_object = datetime.datetime.strptime(month, "%b")
    return datetime_object.month



for linkedin_url in linkedin_urls:
    companies = []
    jobs = []
    jobsduration = []
    joiningdates = []
    leavingdates = []

    driver.get('https://www.linkedin.com/in/pragyajain73/?originalSubdomain=in')
    time.sleep(5)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')


    #SCRAPING EXPERIENCE SECTION

    experience = soup.find(lambda tag:tag.name=="section" and "Experience" in tag.text).find('ul')
    formatcheck = experience.find_all('li', {'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})

    for f in formatcheck:
        if (f.find('div', {'class' : 'display-flex flex-column full-width align-self-center'})).find('a') == None:
            job_titles= f.find_all("span", {'class': 'mr1 t-bold'})
            for j in job_titles:
                job = j.find("span", {'class' : 'visually-hidden'}).get_text().strip()
                jobs.append(job)

            company_names = f.find_all("span", {'class' : 't-14 t-normal'})
            for c in company_names:
                company = c.find("span", {'class' : 'visually-hidden'}).get_text().strip()
                removeFullTime(company)
                companies.append(company)

            joining_datesANDduration = f.find_all("span", {'class': 't-14 t-normal t-black--light'})[0]
            dateANDduration = joining_datesANDduration.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            joiningdate = dateANDduration.split(' - ')[0]
            leavingdate = (dateANDduration.split(' - ')[1]).split(' · ')[0]
            jobduration = dateANDduration.split(' · ')[1]
            joiningdates.append(joiningdate)
            jobsduration.append(jobduration)
            leavingdates.append(leavingdate)

        else:
            job_titles = f.find_all('span', {'class': 'mr1 hoverable-link-text t-bold'})[(len(f.find_all('li'))) -1]
            job = job_titles.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            jobs.append(job)

            company_titles = f.find_all('span', {'class': 'mr1 hoverable-link-text t-bold'})[0]
            company = company_titles.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            companies.append(company)

            leaving_dates = f.find_all("span", {'class': 't-14 t-normal t-black--light'})[0]
            leavingdatetemp = leaving_dates.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            leavingdate = (leavingdatetemp.split(' - ')[1]).split(' · ')[0]
            leavingdates.append(leavingdate)

            joining_dates = f.find_all("span", {'class': 't-14 t-normal t-black--light'})[(len(f.find_all('li')))*2 - 2]
            joiningdatetemp = joining_dates.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            joiningdate = joiningdatetemp.split(' - ')[0]
            joiningdates.append(joiningdate)

            job_duration = f.find_all("span", {'class': 't-14 t-normal'})[0]
            jobduration = job_duration.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            jobduration = removeFullTime(jobduration)
            jobsduration.append(jobduration)

    #SCRAPING EDUCATION SECTION

    education = soup.find(lambda tag:tag.name=="section" and "Education" in tag.text).find('ul')
    schoolsection = education.find(lambda tag:tag.name=="li" and "Indian Institute of Technology, Kanpur" in tag.text)

    years_of_schooling = schoolsection.find("span", {'class': 't-14 t-normal t-black--light'})
    yearofschooling = years_of_schooling.find("span", {'class' : 'visually-hidden'}).get_text().strip()

    collegeyearofgrad = yearofschooling.split(' - ')[1]
    collegeyearofjoin = yearofschooling.split(' - ')[0]
    collegesyearofgrad.append(collegeyearofgrad)
    collegesyearofjoining.append(collegeyearofjoin)

    collegeduration = int(collegeyearofgrad)-int(collegeyearofjoin)
    collegesduration.append(collegeduration)

    college_names = schoolsection.find('span', {'class':'mr1 hoverable-link-text t-bold'})
    college = college_names.find("span", {'class' : 'visually-hidden'}).get_text().strip()
    colleges.append(college)

    degree_names = schoolsection.find('span', {'class':'t-14 t-normal'})
    degree = degree_names.find("span", {'class' : 'visually-hidden'}).get_text().strip()
    degrees.append(degree)

    #FINDING FIRST JOB

    collegeleavingdate = datetime.datetime(int(collegesyearofgrad[count]),6,1)
    firstjobindex = None
    for i in range(len(formatcheck)):
        index = len(formatcheck) - (i+1)
        jobjoiningdate = datetime.datetime(int(joiningdates[index].split()[1]),convertingMonthToNumber(joiningdates[index].split()[0]),1)
        if collegeleavingdate < jobjoiningdate:
            firstjobindex = index
        if firstjobindex != None:
            break

    firstjobtitles.append(jobs[firstjobindex])
    firstjobcompanies.append(companies[firstjobindex])
    firstjobdurations.append(jobsduration[firstjobindex])
    firstjobjoiningdates.append(joiningdates[firstjobindex])
    firstjobleavingdates.append(leavingdates[firstjobindex])

    count = count + 1





driver.quit()

print(jobs)
print(companies)
print(joiningdates)
print(leavingdates)
print(jobsduration)
print(collegesyearofgrad)
print(collegesyearofjoining)
print(colleges)
print(collegesduration)
print(degrees)
print(firstjobtitles)
print(firstjobcompanies)
print(firstjobdurations)
print(firstjobjoiningdates)
print(firstjobleavingdates)
