from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import pandas

import profile_links_from_school_getter
import profile_data_getter
import linkedin_login



def getting_data_from_profiles():

    driver = webdriver.Chrome()

    iitk_id = 157268

    linkedin_urls = []

    linkedin_login.logging_in(driver)
    profile_links_from_school_getter.getting_links_and_clicking_next_page(iitk_id, driver, linkedin_urls)

    all_experience_data = {'User id': None, 'Names':None, 'Job Titles': None, 'Companies': None, 'Job Duration': None , 'Job Joining Dates': None, 'Job Leaving Dates': None}
    all_education_data = {'User id': None, 'Names': None,'School Names': None, 'Degree Names': None, 'School Joining Dates': None, 'School Leaving Dates': None, 'School Duration': None}

    person_num = 1
    num_jobs_list = []
    num_degrees_list = []

    for linkedin_url in linkedin_urls:

        driver.get(linkedin_url)
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID, "experience")))
        src = driver.page_source
        soup = BeautifulSoup(src, 'html.parser')

        names = []
        users_id = []
        userid = driver.current_url.split('in/')[1].split('/')[0]

        name = profile_data_getter.extracting_from_personal_info_section_from_profile(soup)
        profile_data_getter.extracting_from_experience_section_from_profile(soup, driver, all_experience_data, person_num, num_jobs_list)
        profile_data_getter.extracting_from_education_section_from_profile(soup, all_education_data, person_num, num_degrees_list)

        for i in range(num_jobs_list[person_num - 1]):
            names.append(name)
            users_id.append(userid)

        if person_num > 1:
            all_experience_data['Names'].extend(names)
            all_experience_data['User id'].extend(users_id)
        else:
            all_experience_data['Names'] = names
            all_experience_data['User id'] = users_id

        names = []
        users_id = []

        for i in range(num_degrees_list[person_num - 1]):
            names.append(name)
            users_id.append(userid)

        if person_num > 1:
            all_education_data['Names'].extend(names)
            all_education_data['User id'].extend(users_id)
        else:
            all_education_data['Names'] = names
            all_education_data['User id'] = users_id

        person_num = person_num + 1







    driver.quit()

    experience_df = pandas.DataFrame(data=all_experience_data)
    education_df = pandas.DataFrame(data=all_education_data)
    education_df.to_csv('iitk_education_df40.csv',index = False)
    experience_df.to_csv('iitk_experience_df40.csv',index = False)



def main():
   getting_data_from_profiles()



main()





