from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import datetime

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


def extracting_from_experience_section_from_profile(soup,driver,dict,person_no,num_job):
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
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "pvs-list")))
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
            if len(leaving_date_temp.split(' - ')) == 1:
                leaving_date = leaving_date_temp.split(' · ')[0]
            else:
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

    if person_no > 1:
        dict['Job Titles'].extend(jobs)
        dict['Companies'].extend(companies)
        dict['Job Duration'].extend(jobs_duration)
        dict['Job Joining Dates'].extend(joining_dates)
        dict['Job Leaving Dates'].extend(leaving_dates)
    else:
        dict['Job Titles'] = jobs
        dict['Companies'] = companies
        dict['Job Duration'] = jobs_duration
        dict['Job Joining Dates']= joining_dates
        dict['Job Leaving Dates'] = leaving_dates

    num_job.append(len(jobs))


def extracting_from_education_section_from_profile(soup,dict,person_no,num_degree):
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
        if years_of_schooling == None:
            colleges_year_of_joining.append('N/A')
            colleges_year_of_grad.append('N/A')
            colleges_duration.append('N/A')
        else:
            year_of_schooling = years_of_schooling.find("span", {'class' : 'visually-hidden'}).get_text().strip()

            college_year_of_join = year_of_schooling.split(' - ')[0]

            if len(college_year_of_join.split()) > 1:
                college_year_of_join = college_year_of_join.split()[1]

            if len(year_of_schooling.split(' - ')) > 1:
                college_year_of_grad = year_of_schooling.split(' - ')[1]
            else:
                college_year_of_grad = college_year_of_join

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
            degrees.append('N/A')


    if person_no > 1:
        dict['Degree Names'].extend(degrees)
        dict['School Names'].extend(colleges)
        dict['School Duration'].extend(colleges_duration)
        dict['School Joining Dates'].extend(colleges_year_of_joining)
        dict['School Leaving Dates'].extend(colleges_year_of_grad)
    else:
        dict['Degree Names'] = degrees
        dict['School Names'] = colleges
        dict['School Duration'] = colleges_duration
        dict['School Joining Dates'] = colleges_year_of_joining
        dict['School Leaving Dates'] = colleges_year_of_grad

    num_degree.append(len(degrees))
