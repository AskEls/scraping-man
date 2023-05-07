'''
Hello everyone 
thanks for coming
created at : 08/05/2023
'''

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException, TimeoutException

from downloaders import Downloader


# Variabel global untuk driver
driver = None
#memanggil Driver 
def driver_start():
    global driver
    if driver is None:
        path = 'selenium/chromedriver.exe'
        url_login = 'https://learning-ind.refocus.me/users/sign_in'
        opts = webdriver.ChromeOptions()
        opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        driver = webdriver.Chrome(executable_path=path,options=opts)
        driver.maximize_window()
        driver.get(url_login)
    return driver


def login(driver,email,password):

    id_mail = "user[email]"
    id_pass = "user[password]"
    xpath_button = "/html/body/main/div/div/article/form/div[5]/button"
    login_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, id_mail))).send_keys(email)
    login_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, id_pass))).send_keys(password)
    login_input = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath_button))).click()
    time.sleep(10)
    

    try :
                
        driver.get('https://learning-ind.refocus.me/enrollments')
        print("Login successful.")
        return True
    
    except TimeoutException:
        print("Login failed. Please check your credentials and try again.")
        return False


def LoginToClass(driver):
    wrapper = '//*[@id="main-content"]/section/div/ul/li/div/div/a[2]'
    # Menggulir ke elemen wrapper
    wrapper_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, wrapper)))
    driver.execute_script("arguments[0].scrollIntoView();", wrapper_element)
    time.sleep(2)  # Tunggu 2 detik setelah menggulir
    
    # Klik tombol "play"
    play = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, wrapper)))
    play.click()
    
    return driver

    
    

def navigasi(driver):
    #//*[@id="ui-id-5"]/div/span[3]
    small_navigasi = '//*[@id="ui-id-3"]/div/span[3]/i'
    navigasi = WebDriverWait(driver, 16).until(EC.element_to_be_clickable((By.XPATH, small_navigasi)))
    navigasi.click()
    return driver

def wrapper(driver):
    #xpathWrapper = '//*[@id="player-wrapper"]/div/nav'
    wrapper = '//*[@id="player-wrapper"]/div/nav/div/div[4]'
    # Menggulir ke elemen xpathWrapper
    wrapper_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, wrapper)))
    wrapper = driver.execute_script("arguments[0].scrollIntoView();", wrapper_element)
    time.sleep(2)  # Tunggu 2 detik setelah menggulir
    return driver

def module(driver,module_name):
    
    mapping = {
        ##Paket module :
        'modul2' : '//*[@id="ui-id-3"]/div/span[3]',
        'modul3_v1' : '//*[@id="ui-id-5"]/div/span[3]',
        'modul3_v2' : '//*[@id="ui-id-17"]/div/span[3]',
        'modul4' : '//*[@id="ui-id-9"]/div/span[3]',
        'modul5' : '//*[@id="ui-id-11"]/div/span[3]',
        'modul6' : '//*[@id="ui-id-15"]/div/span[3]'
        }

    module_map = mapping[module_name]
    module = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, module_map))).click()
    
    return module

'''
def chose_module(driver, choice):
    if choice == '1':  # (sheet)1 = modul2
        module(driver, 'modul2')
    elif choice == '2':  # (sql_v)1 = modul3_v1
        module(driver, 'modul3_v1')
    elif choice == '3':  # (sql_v2) == modul3_v2
        module(driver, 'modul3_v2')
    elif choice == '4':  # (PowerBI) == modul4
        module(driver, 'modul4')
    elif choice == '5':  # (PowerBI2) == modul5
        module(driver, 'modul5')
    elif choice == '6':  # Python == modul6
        module(driver, 'modul6')
    else:
        print("Pilihan Tidak ada yang tepat")
'''
def chose_module(driver, choice,start_index,end_index):
    if choice == '1':  # (sheet)1 = modul2
        module(driver, 'modul2')
        process_list_items(driver, 'modul2', start_index, end_index)
    elif choice == '2':  # (sql_v)1 = modul3_v1
        module(driver, 'modul3_v1')
        process_list_items(driver, 'modul3_v1', start_index, end_index)
    elif choice == '3':  # (sql_v2) == modul3_v2
        module(driver, 'modul3_v2')
        process_list_items(driver, 'modul3_v2', start_index, end_index)
    elif choice == '4':  # (PowerBI) == modul4
        module(driver, 'modul4')
        process_list_items(driver, 'modul4', start_index, end_index)
    elif choice == '5':  # (PowerBI2) == modul5
        module(driver, 'modul5')
        process_list_items(driver, 'modul5', start_index, end_index)
    elif choice == '6':  # Python == modul6
        module(driver, 'modul6')
        process_list_items(driver, 'modul6', start_index, end_index)
    else:
        print("Pilihan Tidak ada yang tepat")



        
## Proses mengunduh video 
def save_file(url):
    downloader = Downloader()
    downloader.download(url)        
        
        
def process_list_items(driver,module_name_li,start_index, end_index):
    video_data = []
    for index_li in range(start_index, end_index + 1):
       
        try:
            mapping_li = {                              
                'modul2' : '//*[@id="ui-id-4"]/ul/li[{}]',
                'modul3_v1' : '//*[@id="ui-id-6"]/ul/li[{}]',
                'modul3_v2' : '//*[@id="ui-id-18"]/ul/li[{}]',
                'modul4' : '//*[@id="ui-id-10"]/ul/li[{}]',
                'modul5' : '//*[@id="ui-id-12"]/ul/li[{}]',
                'modul6' : '//*[@id="ui-id-16"]/ul/li[{}]'
                }
            
            #path_li = '//*[@id="ui-id-6"]/ul/li[{}]'
            path_li = mapping_li[module_name_li]
            current_li_xpath = path_li.format(index_li)

            li_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, current_li_xpath)))

            driver.execute_script("arguments[0].scrollIntoView();", li_element)
            li_element.click()
            
            time.sleep(15)

            try:
                ## Mengambil atribut src dari elemen iframe
                iframe_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
                iframe_src = iframe_element.get_attribute('src')
                
                ## Downloading FIle
                save_file(iframe_src)
                time.sleep(5)
            except TimeoutException:
                print(f"TimeoutException: iframe element dengan XPath {iframe_xpath} tidak ditemukan dalam waktu yang ditentukan \n")
                iframe_src = None
                continue

            # Mengambil teks judul
            title_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, title_xpath)))
            title = title_element.text
            
            

            # Menyimpan data video dalam format JSON
            video_data.append({
                'index': index_li,
                'title': title,
                'iframe_src': iframe_src
            })
            
            


            # Mencetak data video
            print(f"Video index {index_li}")
            print(f"Title: {title}")
            print(f"Video Source: {iframe_src}")
            print("************************** \n")
            ## Variabel def save_file()
            
        

        except NoSuchElementException:
            ## Jika tidak ada elemen li berikutnya, keluar dari loop
            print(f"Gagal pada li index: {index_li}")
            break
        except UnexpectedAlertPresentException:
            ## Menangani pesan peringatan yang tidak terduga
            alert = driver.switch_to.alert
            print(f"Unexpected alert: {alert.text} \n")
            alert.accept()  # Klik 'OK' pada peringatan
            continue  # Lanjutkan ke iterasi berikutnya dari loop

    ## Menyimpan data video dalam file JSON
    with open('video_data.json', 'w') as json_file:
        json.dump(video_data, json_file)

    return video_data




## Proses Memasukan User Credential    
def config_login():
    email = input("Email: ")
    password = input("Password: ")
    return email, password

## Proses Pemilihan Module
def config_module():
    print(
        ''' Pilih Module Kamu :
        1. SpreedSheet 
        2. SQL V1
        3. SQL V2
        4. PowerBI
        5. PowerBI - Tahap Lanjut
        '''
    )
    choice = input("Pilihan Kamu: ")
    return choice

## Proses Pemilihan Item
def config_process_list_items():
    print("Masukkan berapa url yang Kamu ambil..? ")
    print("************************************")
    start = input("masukkan dimulai dari berapa: ")
    end = input("Masukan total default (10): ")
    return int(start), int(end)

def main():
    email, password = config_login()
    choice = config_module()
    start, end = config_process_list_items()
    return email, password, choice, start, end

def micro_run(): 
    print('''

    ██╗  ███████████╗    ██╗     ██████╗     ██╗    ██╗██████╗██████╗██╗    ██████╗ 
    ██║  ████╔════██║    ██║    ██╔═══██╗    ██║    ████╔═══████╔══████║    ██╔══██╗
    ████████████╗ ██║    ██║    ██║   ██║    ██║ █╗ ████║   ████████╔██║    ██║  ██║
    ██╔══████╔══╝ ██║    ██║    ██║   ██║    ██║███╗████║   ████╔══████║    ██║  ██║
    ██║  ███████████████████████╚██████╔╝    ╚███╔███╔╚██████╔██║  ███████████████╔╝
    ╚═╝  ╚═╚══════╚══════╚══════╝╚═════╝      ╚══╝╚══╝ ╚═════╝╚═╝  ╚═╚══════╚═════╝    ''')

    email, password, choice, start, end = main()
    driver = driver_start()
    login_status = login(driver,email, password)
    if login_status:
        driver = LoginToClass(driver)
        time.sleep(2)
        wrapper(driver)
        time.sleep(5)
        navigasi(driver)
        while True:
                  
            try:
                  chose_module(driver,choice,start,end)
            except Exception as e:
                print(f"An error occurred: {e}")
                break
    else :
        print("Gagal Ada Kesalahan Periksa Lagi")
        


# Jalankan micro_run untuk mulai menjalankan program
if __name__ == "__main__":
    micro_run()

