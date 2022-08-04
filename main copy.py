from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import timedelta, datetime
import os, time, string, random, json



def rstring(length):
   letters=string.ascii_lowercase
   return ''.join(random.choice(letters) for x in range(length))

full_xpath = {
        'email_input': '/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[1]/div[2]/div/auto-check/input[1]',
        'email_button': '/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[1]/div[2]/button',
        'password_input': '/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[2]/div[2]/div/visible-password/auto-check/input[1]',
        'password_button': '/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[2]/div[2]/button',
        'username_input': '/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[3]/div[2]/div/auto-check/input[1]',
        'username_button': '/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[3]/div[2]/button',
        'username_feedback': '/html/body/div[4]/main/div[2]/text-suggester/div[2]/p[3]',
        'too_many_requests_feedback': '/html/body/div[4]/main/div[2]/text-suggester/div[2]/p[3]/div/h1'
    }

os.environ["webdriver.chrome.driver"] = os.path.join(os.path.dirname(__file__), "chromedriver")
coptions=webdriver.ChromeOptions()
coptions.add_argument("--headless")
coptions.add_argument("--incognito")
coptions.add_argument("--start-maximized")
coptions.add_argument("--disable-logging")
coptions.add_argument("--log-level=3")
coptions.add_argument("--disable-crash-reporter")
coptions.add_argument("--disable-dev-shm-usage")
coptions.add_argument("--output=/dev/null")
coptions.add_argument("--disable-in-process-stack-traces")
coptions.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.3610")

if __name__=="__main__":
    # get list of usernames to check
    with open('availability.json') as username_record:
        username_list = json.load(username_record)
        #  username: {
        #    is_available: bool,
        #    dt-timestamp: int // secs since epoch
        #    manual: bool // checked manually or using selenium
        # },
        check_username_list = [u for u in username_list
                         if username_list[u].get('is_available',0)
                         and not username_list[u].get('manual',0)]

    records_since_last_cooldown = 0
    valid_response_list_generic = ['{u} is available.','Username {u} is not available.','Username \'{u}\' is unavailable.']
    retrieve_time = 0
    cooldown_time = int(datetime.utcnow().timestamp())

    # load github join page
    print("Opening chrome")
    driver=webdriver.Chrome(options=coptions, service_log_path=None)
    driver.get("https://github.com/signup")
    print("Waiting for github")
    time.sleep(20)
    
    # enter email
    print("Entering random email")
    email=driver.find_element(By.XPATH, value=full_xpath['email_input'])
    email.click()
    email.send_keys(f"{rstring(10)}@gmail.com")
    time.sleep(2)
    continue1=driver.find_element(By.XPATH, value=full_xpath['email_button']) 
    continue1.click()

    # enter password
    print("Entering random password")
    password=driver.find_element(By.XPATH, value=full_xpath['password_input'])
    password.click()
    password.send_keys(rstring(72))
    time.sleep(2)
    continue2=driver.find_element(By.XPATH, value=full_xpath['password_button']) 
    continue2.click()
    time.sleep(1)

    # get username
    username_input=driver.find_element(By.XPATH, value=full_xpath['username_input']) 
    username_input.click()
    continue3=driver.find_element(By.XPATH, value=full_xpath['username_button'])

    for u in check_username_list:
        username_status = False
        retrieve_time = int(datetime.utcnow().timestamp())
        r_list_user = [r.format(u=u) for r in valid_response_list_generic]
        
        # enter username
        username_input.send_keys(u)

        # wait 5 secs for username feedback (should probably use WebDriverWait here)
        while not (username_status := driver.find_element(By.XPATH, value=full_xpath['username_feedback']).text) in r_list_user:
            if int(datetime.utcnow().timestamp()) - retrieve_time > 5:
                break

        # record username feedback
        if username_status:
            if (username_available := not continue3.get_property("disabled")):
                print(f'√ {u} (is available)')
            else:
                print(f'X {u} (is taken)')

            username_list[u] = {'is_available': username_available, 'dt-updated': retrieve_time, 'manual': True}
            with open('availability.json','w') as record_file:
                json.dump(username_list, record_file, indent= 4)

        else:
            print('Timed out waiting for username feedback on {u=}')
        
        # cooldown
        records_since_last_cooldown += 1
        try:
            # this line throws exception if not rate limited yet
            driver.find_element(By.XPATH, value=full_xpath['too_many_requests_feedback'])

            # do cooldown, show stats
            time_since_last_cooldown = int(datetime.utcnow().timestamp()) - cooldown_time
            cooldown_time = int(datetime.utcnow().timestamp())
            cooldown_length = 90 # seconds
            print(f'Checked {records_since_last_cooldown} usernames in {time_since_last_cooldown} secs')
            cooldown_end_time_local = str(datetime.now().astimezone() + timedelta(seconds=cooldown_length))
            print(f'Cooling until {cooldown_end_time_local}')
            time.sleep(cooldown_length)
            records_since_last_cooldown = 0
        except:
            pass
        
        username_input.send_keys(Keys.CONTROL+"a")
        username_input.send_keys(Keys.BACKSPACE)

    time.sleep(2)
    print('Finished.')
