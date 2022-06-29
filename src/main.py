import selector as selector
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver import Keys
import lxml
import time
import pandas
import datetime




def logging_in(driver):

    driver.get("https://linkedin.com/uas/login")


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
        if filter_url.find('div', {'class' : 't-roman t-sans'}).find('a')['href'] != 'https://www.linkedin.com/search/results/people/headless/?schoolFilter=%5B' + str(schoolid) + '%5D&origin=FACETED_SEARCH':
            urls.append(filter_url.find('div', {'class' : 't-roman t-sans'}).find('a')['href'])

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)


def getting_urls_and_clicking_next_page(schoolid,driver,urls):
    driver.get('https://www.linkedin.com/search/results/people/?origin=FACETED_SEARCH&schoolFilter=%5B%22' + str(schoolid) + '%22%5D&sid=(X1')
    driver.implicitly_wait(5)
    loop = True
    while loop:
        getting_profile_urls(schoolid,driver,urls)

        old_url = driver.current_url

        next_button = driver.find_element_by_xpath('//button[@type="button" and @aria-label="Next"]')
        next_button.click()
        time.sleep(3)

        if driver.current_url == old_url:
            loop = False
            print('All links obtained.')

def remove_full_time(text,format_type):
    if len(text.split(' · ')) > 1:
        if format_type == 'format1':
            return text.split(' · ')[0]
        else:
            return text.split(' · ')[1]
    else:
        return text


def converting_date(date):
    if len(date.split()) == 1:
        return datetime.datetime(int(date),7,1)
    else:
        month = date.split()[0]
        datetime_object = datetime.datetime.strptime(month, "%b")
        return datetime.datetime(int(date.split()[1]),datetime_object.month,1)


def extracting_from_personal_info_section_from_profile(soup):
    return soup.find('h1', {'class':'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()


def extracting_from_experience_section_from_profile(soup,driver,dict):
    companies = []
    jobs = []
    jobs_duration = []
    joining_dates = []
    leaving_dates = []

    for s in soup.find_all('section'):
        if s.find('div', {'id' : 'experience'}) != None:
            experience_check = s

    if experience_check.find('div', {'class' : 'pvs-list__footer-wrapper'}) != None:
        experience_page = experience_check.find('div', {'class' : 'pvs-list__footer-wrapper'}).find('a')
        link = experience_page['href']
        driver.get(link)
        time.sleep(5)
        experience_src = driver.page_source
        experience_soup = BeautifulSoup(experience_src, 'html.parser')
        experience = experience_soup.find('main').find('section').find('ul')
        format_checks = experience.find_all('li', {'class':'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
    else:
        experience = experience_check.find('ul')
        format_checks = experience.find_all('li', {'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})

    for format_check in format_checks:
        if (format_check.find('div', {'class' : 'display-flex flex-row justify-space-between'})).find('a') == None:
            job_titles= format_check.find_all("span", {'class': 'mr1 t-bold'})
            for j in job_titles:
                job = j.find("span", {'class' : 'visually-hidden'}).get_text().strip()
                jobs.append(job)

            company_names = format_check.find_all("span", {'class' : 't-14 t-normal'})
            for c in company_names:
                company = c.find("span", {'class' : 'visually-hidden'}).get_text().strip()
                company = remove_full_time(company,'format1')
                companies.append(company)

            joining_dates_and_duration = format_check.find_all("span", {'class': 't-14 t-normal t-black--light'})[0]
            date_and_duration = joining_dates_and_duration.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            if len(date_and_duration.split(' - ')) == 1:
                joining_date = date_and_duration.split(' · ')[0]
                leaving_date = date_and_duration.split(' · ')[0]
            else:
                joining_date = date_and_duration.split(' - ')[0]
                leaving_date = (date_and_duration.split(' - ')[1]).split(' · ')[0]

            job_duration = date_and_duration.split(' · ')[1]

            joining_dates.append(joining_date)
            jobs_duration.append(job_duration)
            leaving_dates.append(leaving_date)

        else:
            no_of_jobs = len(format_check.find_all('span', {'class': 'mr1 hoverable-link-text t-bold'})) - 1
            job_titles = format_check.find_all('span', {'class': 'mr1 hoverable-link-text t-bold'})[no_of_jobs]
            job = job_titles.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            jobs.append(job)

            company_titles = format_check.find_all('span', {'class': 'mr1 hoverable-link-text t-bold'})[0]
            company = company_titles.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            companies.append(company)


            leaving_date_titles = format_check.find('ul').find_all("span", {'class': 't-14 t-normal t-black--light'})[0]
            leaving_date_temp = leaving_date_titles.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            leaving_date = (leaving_date_temp.split(' - ')[1]).split(' · ')[0]
            leaving_dates.append(leaving_date)

            joining_date_temps = []
            for l in format_check.find_all('li'):
                joining_date_temp = l.find_all("span", {'class': 't-14 t-normal t-black--light'})
                if joining_date_temp != []:
                    joining_date_temps.append(joining_date_temp[0])
            joining_date = joining_date_temps[no_of_jobs-1].get_text().strip().split(' - ')[0]
            joining_dates.append(joining_date)

            job_duration_titles = format_check.find_all("span", {'class': 't-14 t-normal'})[0]
            job_duration = job_duration_titles.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            job_duration = remove_full_time(job_duration,'format2')
            jobs_duration.append(job_duration)

    dict['Job Titles']= jobs
    dict['Companies'] = companies
    dict['Job Duration'] = jobs_duration
    dict['Job Joining Dates'] = joining_dates
    dict['Job Leaving Dates'] = leaving_dates


def extracting_from_education_section_from_profile(soup,dict):
    colleges_year_of_grad = []
    colleges = []
    degrees = []
    colleges_year_of_joining = []
    colleges_duration = []

    for s in soup.find_all('section'):
            if s.find('div', {'id' : 'education'}) != None:
                education = s.find('ul')

    school_sections = education.find_all('li', {'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})

    for school_section in school_sections:
        years_of_schooling = school_section.find("span", {'class': 't-14 t-normal t-black--light'})
        year_of_schooling = years_of_schooling.find("span", {'class' : 'visually-hidden'}).get_text().strip()

        college_year_of_join = year_of_schooling.split(' - ')[0]

        if len(college_year_of_join.split()) > 1:
            college_year_of_join = college_year_of_join.split()[1]

        college_year_of_grad = year_of_schooling.split(' - ')[1]

        if len(college_year_of_grad.split()) > 1:
            college_year_of_grad = college_year_of_grad.split()[1]

        colleges_year_of_grad.append(college_year_of_grad)
        colleges_year_of_joining.append(college_year_of_join)


        college_duration = int(college_year_of_grad)-int(college_year_of_join)
        colleges_duration.append(college_duration)

        college_names = school_section.find('span', {'class':'mr1 hoverable-link-text t-bold'})
        college = college_names.find("span", {'class' : 'visually-hidden'}).get_text().strip()
        colleges.append(college)

        degree_names = school_section.find('span', {'class':'t-14 t-normal'})
        if degree_names != None:
            degree = degree_names.find("span", {'class' : 'visually-hidden'}).get_text().strip()
            degrees.append(degree)
        else:
            degrees.append(' ')


    for n in range(len(dict['Job Titles'])- len(degrees)):
        degrees.append(' ')
        colleges.append(' ')
        colleges_year_of_joining.append(' ')
        colleges_duration.append(' ')
        colleges_year_of_grad.append(' ')



    dict['Degree Names']= degrees
    dict['School Names'] = colleges
    dict['School Duration'] = colleges_duration
    dict['School Joining Dates'] = colleges_year_of_joining
    dict['School Leaving Dates'] = colleges_year_of_grad


def gettingDataFromProfiles():

    PATH = input("Enter the webdriver path:\n")
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    iitk_id = 157268

    linkedin_urls = []

    logging_in(driver)
    getting_urls_and_clicking_next_page(iitk_id,driver,linkedin_urls)
    print(len(linkedin_urls))

    all_profiles_linkedin_data = {}

    for linkedin_url in linkedin_urls:

        driver.get(linkedin_url)
        time.sleep(5)
        src = driver.page_source
        soup = BeautifulSoup(src, 'html.parser')


        try:

            profile_experience_and_education_data = {'Job Titles': None, 'Companies': None, 'Job Duration': None , 'Job Joining Dates': None, 'Job Leaving Dates': None,'School Names': None, 'Degree Names': None, 'School Joining Dates': None, 'School Leaving Dates': None, 'School Duration': None}

            extracting_from_experience_section_from_profile(soup,driver,profile_experience_and_education_data)

            extracting_from_education_section_from_profile(soup,profile_experience_and_education_data)

            name = extracting_from_personal_info_section_from_profile(soup)


        except:

            print('error' + linkedin_url)

    driver.quit()


def main():
   gettingDataFromProfiles()


main()




