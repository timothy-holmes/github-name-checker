from selenium import webdriver
from webdriver_auto_update import check_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, os, string, random, ctypes
from itertools import product
from colorama import Fore, init

miss_accs=0
hit_accs=0

init()
os.system("cls")
os.system("mode 80, 40")
check_driver(".")

def rstring(length):
   letters=string.ascii_lowercase
   return ''.join(random.choice(letters) for x in range(length))

def title(text):
    ctypes.windll.kernel32.SetConsoleTitleW(f"Github Username Checker | {text}")

coptions=webdriver.ChromeOptions()
# coptions.add_argument("--headless")
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
    minium_length=int(input(f"{Fore.LIGHTGREEN_EX}Min letters{Fore.RESET}: "))
    maximum_length=int(input(f"{Fore.LIGHTGREEN_EX}Max letters{Fore.RESET}: "))
    os.system("cls")
    last_cooldown=0

    title("Opening chrome")
    driver=webdriver.Chrome(options=coptions, service_log_path=None)
    driver.get("https://github.com/signup")
    title("Waiting for github")
    time.sleep(1.9)
    
    # enter email
    title("Entering random email")
    email=driver.find_element(By.XPATH, value="/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[1]/div[2]/div/auto-check/input[1]")
    email.click()
    email.send_keys(f"{rstring(10)}@gmail.com")
    time.sleep(.5)
    continue1=driver.find_element(By.XPATH, value="/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[1]/div[2]/button") 
    continue1.click()

    # enter password
    title("Entering random password")
    password=driver.find_element(By.XPATH, value="/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[2]/div[2]/div/visible-password/auto-check/input[1]")
    password.click()
    password.send_keys(rstring(72))

    time.sleep(.5)

    continue2=driver.find_element(By.XPATH, value="/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[2]/div[2]/button") 
    continue2.click()

    username=driver.find_element(By.XPATH, value="/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[3]/div[2]/div/auto-check/input[1]") 
    username.click()

    ctypes.windll.kernel32.SetConsoleTitleW(f"Github Username Checker | Starting to bruteforce")
    for length in range(minium_length, maximum_length + 1):
        for combo in product(string.ascii_lowercase+string.digits, repeat=length):
            username.send_keys("".join(combo))
            time.sleep(0.45)
            continue3=driver.find_element(By.XPATH, value="/html/body/div[4]/main/div[2]/text-suggester/div[1]/form/div[3]/div[2]/button")

            if continue3.get_property("disabled")==False:
                print(f"{Fore.LIGHTGREEN_EX}HIT {Fore.RESET}| {Fore.LIGHTRED_EX}{''.join(combo)} {Fore.RESET}| {Fore.LIGHTGREEN_EX}github.com{Fore.RESET}/{Fore.LIGHTRED_EX}{''.join(combo)}")
                with open("hits.txt", "a") as f:
                    f.write(f"{''.join(combo)}\n")
                f.close()
                hit_accs=hit_accs+1
            else:
                miss_accs=miss_accs+1
            try:
                driver.find_element(By.XPATH, value="/html/body/div[4]/main/div[2]/text-suggester/div[2]/p[3]/div/h1")
                time_delay=90
                last_cooldown=last_cooldown+1

                for i in range(time_delay):
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Github Username Checker | Waiting: {time_delay}s | Last cooldown: {last_cooldown}")
                    time.sleep(1)
                    time_delay=time_delay-1

                last_cooldown=0

            except:
                last_cooldown=last_cooldown+1
            

            username.send_keys(Keys.CONTROL+"a")
            username.send_keys(Keys.BACKSPACE)

            ctypes.windll.kernel32.SetConsoleTitleW(f"Github Username Checker | Hits: {hit_accs} | Misses: {miss_accs} | Total: {hit_accs+miss_accs} | Last cooldown: {last_cooldown}")

    time.sleep(2)
