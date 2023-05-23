import json
import time
import os
import datetime
import requests
import toml 
from bs4 import BeautifulSoup

class linkedins:
    @staticmethod
    def get_linkedin(webpage, page_number, linkedin_jobs):
        
        next_page = webpage + str(page_number)
        print(next_page)
        response = requests.get(next_page)
        soup = BeautifulSoup(response.content, 'html.parser')

        job_cards = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        index = 0
        for card in job_cards:
            index_uid = card['data-tracking-id']
            job_title = card.find('h3', class_='base-search-card__title').text.strip()
            job_company = card.find('h4', class_='base-search-card__subtitle').text.strip()
            job_location = card.find('span', class_='job-search-card__location').text.strip()
            release_time = card.find('time', class_="job-search-card__listdate--new")
            old_time = card.find('time', class_="job-search-card__listdate")
            datetime = None
            times = None
            if release_time is not None:
                datetime = release_time.get('datetime')
                times = release_time.text.strip()
            else:
                if old_time is not None:
                    datetime = old_time.get('datetime')
                    times = old_time.text.strip()
            job_link = card.find('a', class_='base-card__full-link')['href']

            index += 1
            linkedin_job = {
                #'index': index,
                'uid': index_uid,
                'title': job_title,
                'company': job_company,
                'location': job_location,
                'datetime': datetime,
                'time_log': times,
                'apply': job_link
            }

            linkedin_jobs.append(linkedin_job)
            
        lk_page = toml.load('config.toml')
        if page_number < lk_page['page']['total']:
            page_number = page_number + 1
            linkedins.get_linkedin(webpage, page_number, linkedin_jobs)

    def run_linkedin(url): ## Contoh pemanggilan
        linkedin_jobs = []
        get_linkedin(url, 0, linkedin_jobs)
        #example url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%20scientist&location=Indonesia&start='
        
        current_data = datetime.datetime.now().strftime("%Y-%m-%d")
        linkedinPath = "./log_linkedin"
        linkedinFile = "linkedin" + current_date + ".json"
        linkedinLog = os.path.join(linkedinPath, linkedinName)
        
        # Write jobs data to JSON file
        with open(linkedinLog, 'w') as json_file:
            json.dump(linkedin_jobs, json_file, indent=4)
    
    


class jobstreets():
    @staticmethod
    def get_jobstreet(webpage, page_number, jobs):
        
        next_page = webpage + str(page_number)
        print(next_page)
        response = requests.get(next_page)
        soup = BeautifulSoup(response.content, 'html.parser')

        job_card = soup.find_all('div', class_='z1s6m00 _1hbhsw67i _1hbhsw66e _1hbhsw69q _1hbhsw68m _1hbhsw6n _1hbhsw65a _1hbhsw6ga _1hbhsw6fy')
        index = 0
        for test in job_card:
            title = test.find('span', class_='z1s6m00').text.strip()
            company = test.find('a',class_="_6xa4xb0 z1s6m00 z1s6m0f rqoqz4").text.strip()
            link = test.find('a',class_="jdlu994 jdlu996 jdlu999 y44q7i2 z1s6m00 z1s6m0f _1hbhsw6h")['href']
            uid = link.split('jobId=')[1].split('&')[0]
            url = 'https://www.jobstreet.co.id' + link

            location = test.find('span',class_="z1s6m00 _1hbhsw64y y44q7i0 y44q7i3 y44q7i21 y44q7ih").text

            datetime = test.find('time',class_="z1s6m00 _1hbhsw64y")['datetime']
            duration = test.find('time',class_="z1s6m00 _1hbhsw64y").text.strip()

            job_benefit = test.find('ul',class_="z1s6m00 z1s6m03 _5135ge0 _5135ge5")
            if job_benefit is not None:
                job = job_benefit.text.strip()
            else :
                job = None
            index += 1
            jobstreet_job={
                #'index':index,
                'uid' : uid,
                'title' :title,
                'company' : company,
                'location': location,
                'datetime': datetime,
                'time_log': duration,
                'apply' : url
            }
            jobs.append(jobstreet_job)
            
        js_page = toml.load('config.toml')
        if page_number < js_page['page']['total']:
            page_number = page_number + 1
            jobstreets.get_jobstreet(webpage, page_number, jobs)
            
        #return jobs

    
    def run_jobstreet(url):

        url='https://www.jobstreet.co.id/id/data-jobs/in-Indonesia?pg='
        jobs = []
        get_jobstreet(url, 1, jobs)
        
        current_date = datetime.datetime.now.strftime("%Y-%m-%d")
        jobstreetPath = "./log_jobstreet"
        jobstreetFile = "jobstreet" + current_date + ".json"
        jobstreetLog = os.path.join(jobstreetPath, jobstreetFile)
        # Write jobs data to JSON file
        with open(jobstreetLog, 'w') as json_file:
            json.dump(jobs, json_file, indent=4)

