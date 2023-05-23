import os 
import datetime
import time
import json
import pandas as pd
from Database import *
from scrape import *


''' Get Data '''
def lk_table(conn):
    #
    linkedin_table_query='''
    CREATE TABLE IF NOT EXISTS linkedin_data(
        uid VARCHAR(255) PRIMARY KEY,
        title VARCHAR(255),
        category_job VARCHAR(255),
        company VARCHAR(255),
        country_name VARCHAR(255),
        location VARCHAR(255),
        datetime VARCHAR(255),
        time_log VARCHAR(255),
        apply VARCHAR(255));
    '''
    cursor = conn.cursor()
    cursor.execute(linkedin_table_query)
    conn.commit()


def js_table(conn):
    #
    jobstreet_table_query='''
        CREATE TABLE IF NOT EXISTS jobstreet_data(
            uid VARCHAR(255) PRIMARY KEY,
            title VARCHAR(255),
            category_job VARCHAR(255),
            company VARCHAR(255),
            country_name VARCHAR(255),
            location VARCHAR(255),
            datetime VARCHAR(255),
            time_log VARCHAR(255),
            apply VARCHAR(255));
        '''
    cursor = conn.cursor()
    create = cursor.execute(jobstreet_table_query)
    conn.commit()
    return create
        
def run_linkedin(url):
    linkedin_scrape=[]
    linkedins.get_linkedin(url, 0, linkedin_scrape)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    linkedinPath = "./log_linkedin"
    linkedinFile = "linkedin-" + current_date + ".json"
    linkedinLog = os.path.join(linkedinPath, linkedinFile)
    
    if not os.path.exists(linkedinPath):
        os.makedirs(linkedinPath)
        
    # Write jobs data to JSON file
    with open(linkedinLog, 'w') as json_file:
        json.dump(linkedin_scrape, json_file, indent=4)
        
def run_jobstreet(url):
    jobstreet_scrape=[]
    jobstreets.get_jobstreet(url, 0, jobstreet_scrape)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    jobstreetPath = "./log_jobstreet"
    jobstreetFile = "jobstreet-" + current_date + ".json"
    jobstreetLog = os.path.join(jobstreetPath, jobstreetFile)
    
    if not os.path.exists(jobstreetPath):
        os.makedirs(jobstreetPath)
    
    with open(jobstreetLog , 'w') as json_file:
        json.dump(jobstreet_scrape, json_file, indent=4)
        
 
        
def linkedin_cleansing(conn):
    linkedinPath = "./log_linkedin"
    
    # Dapatkan daftar file dalam direktori tersebut 
    files = os.listdir(linkedinPath)
    
    # Filter the files to only include the ones starting with 'jobstreet' and ending with '.json'
    files = [f for f in files if f.startswith('linkedin') and f.endswith('.json')]

    # Then get the latest file based on the date in the filename
    latest_file = max(files, key=lambda x: pd.to_datetime(x.split('-')[1]))

    #Baca file JSON terbaru menggunakan Pandas 
    lk = pd.read_json(os.path.join(linkedinPath, latest_file))
    
    # Membuat category 
    lk.loc[lk['title'].str.lower().str.contains('scientist|science'), 'category_job'] = 'data scientist'
    lk.loc[lk['title'].str.lower().str.contains('analys|data analyst|analisis|analyst'), 'category_job'] = 'data analys'
    lk.loc[lk['title'].str.lower().str.contains('machine learning|ml'), 'category_job'] = 'machine learning'
    lk.loc[lk['title'].str.lower().str.contains('back end'), 'category_job'] = 'back end engineer'
    lk.loc[lk['title'].str.lower().str.contains('front end'), 'category_job'] = 'front end engineer'
    lk.loc[lk['title'].str.lower().str.contains('software'), 'category_job'] = 'software engineer'
    lk['category_job'] = lk['category_job'].fillna('Others')
    
    # Mengkategorikan Negara 
    lk.loc[lk['location'].str.lower().str.contains('indonesia'), 'country_name'] = 'indonesia'
    lk.loc[lk['location'].str.lower().str.contains('singapore'), 'country_name'] = 'singapore'
    lk.loc[lk['title'].str.lower().str.contains('united states'), 'country_name'] = 'united states'
    #lk.loc[check['Title'].str.lower().str.contains('filipina'), 'category_job'] = 'Front End Engineer'
    #lk.loc[check['Title'].str.lower().str.contains('software'), 'category_job'] = 'Software Engineer'
    lk['country_name'] = lk['country_name'].fillna('others')
    
    #setup database
    # Pengaturan koneksi ke database
    #onn = dbConn.acces()
    cursor = conn.cursor()
    
    # Menjalankan perulangan untuk pengisian data ke tabel
    for row in lk.itertuples(index=False):
        # Menyiapkan query SQL untuk pengisian data
        insert_query = """
        INSERT INTO linkedin_data ( uid, title, category_job, company, country_name, location, datetime, time_log, apply)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        #index	uid	title	category_job	company	country_name	location	datetime	time_log	apply

        values = (
            #ow.index,
            row.uid,
            row.title,
            row.category_job,
            row.company,
            row.country_name,
            row.location,
            row.datetime,
            row.time_log,
            row.apply
        )
        
        try:
            # Menjalankan query SQL untuk pengisian data
            cursor.execute(insert_query, values)
            conn.commit()
            print("lk inserted successfully lk_table.")
        except (Exception, OSError)as e:
            print(f"Error inserting data: {e}")
            conn.rollback()




    
def jobstreet_cleansing(conn):
    jobstreetPath = "./log_jobstreet"
    
    # Dapatkan daftar file dalam direktori tersebut 
    files = os.listdir(jobstreetPath)
    # Filter the files to only include the ones starting with 'jobstreet' and ending with '.json'
    files = [f for f in files if f.startswith('jobstreet') and f.endswith('.json')]

    # Then get the latest file based on the date in the filename
    
    latest_file = max(files, key=lambda x: pd.to_datetime(x.split('-')[1]))

    #Baca file JSON terbaru menggunakan Pandas 
    js = pd.read_json(os.path.join(jobstreetPath, latest_file))
    # Membuat category 
    js.loc[js['title'].str.lower().str.contains('scientist|science'), 'category_job'] = 'data scientist'
    js.loc[js['title'].str.lower().str.contains('analys|data analyst|analisis|analyst'), 'category_job'] = 'data analyst'
    js.loc[js['title'].str.lower().str.contains('machine learning|ml'), 'category_job'] = 'machine learning'
    js.loc[js['title'].str.lower().str.contains('software'), 'category_job'] = 'software engineer'
    js.loc[js['title'].str.lower().str.contains('back end'), 'category_job'] = 'back end engineer' 
    js.loc[js['title'].str.lower().str.contains('front end'), 'category_job'] = 'front end engineer'
    js.loc[js['title'].str.lower().str.contains('busines analyst|ba|business analyst'), 'category_job'] = 'back end engineer'
    js.loc[js['title'].str.lower().str.contains('database|database|data engineer|sql'), 'category_job'] = 'data engineer'
    js.loc[js['title'].str.lower().str.contains('front end'), 'category_job'] = 'front end engineer'
    js.loc[js['title'].str.lower().str.contains('data entry|entry'), 'category_job'] = 'data entry'
    js['category_job'] = js['category_job'].fillna('Others')
    
    # mengkategorikan negara 
    js.loc[js['location'].str.lower().str.contains('indonesia'), 'country_name'] = 'indonesia'
    js.loc[js['location'].str.lower().str.contains('singpore'), 'country_name'] = 'singapore'
    js.loc[js['location'].str.lower().str.contains('united states'), 'country_name'] = 'united states'
    js['country_name'] = js['country_name'].fillna('others')
   # Pengaturan koneksi ke database
    #onn = dbConn.acces()
    cursor = conn.cursor()
    
    # Menjalankan perulangan untuk pengisian data ke tabel
    for row in js.itertuples(index=False):
        # Menyiapkan query SQL untuk pengisian data
        insert_query = """
        INSERT INTO jobstreet_data (uid, title, category_job, company, country_name, location, datetime, time_log, apply)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            #ow.index,
            row.uid,
            row.title,
            row.category_job,
            row.company,
            row.country_name,
            row.location,
            row.datetime,
            row.time_log,
            row.apply
        )
        
        try:
            # Menjalankan query SQL untuk pengisian data
            cursor.execute(insert_query, values)
            conn.commit()
            print("js inserted successfully.")
        except (Exception, OSError)as e:
            print(f"Error inserting data: {e}")
            conn.rollback()

    # Menutup kursor dan koneksi ke database
    #cursor.close()
    #conn.close()
    
def linkedin_start(engine):
    ''' URL list '''
    lk_url_id ='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data&location=Indonesia&start='
    lk_url_us ='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data&location=United%20Stated&start='
    lk_url_sgp = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data&location=Singapore&start='
    
    run_linkedin(lk_url_id)
    linkedin_cleansing(engine)
    #time.sleep(10)
    
    run_linkedin(lk_url_us)
    linkedin_cleansing(engine)
    #time.sleep(10)
    
    run_linkedin(lk_url_sgp)
    linkedin_cleansing(engine)
    #lk_table(engine)  # membut new table
    
    
def jobstreet_start(engine):
    
    js_url_id ='https://www.jobstreet.co.id/id/data-jobs/in-Indonesia?pg='
    
    run_jobstreet(js_url_id)
    jobstreet_cleansing(engine)
    
    #js_table(engine)  # Menggunakan objek db_connection untuk memanggil metode jobstreet_table



def main():
    engine = dbConn.acces()  
    jobstreet_start(engine)
    linkedin_start(engine)
    
    
if __name__ == "__main__":
    main()
