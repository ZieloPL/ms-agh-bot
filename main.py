from contextlib import nullcontext

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import time
import datetime
import random
from dotenv import load_dotenv
import os

#datadad
day = input("Enter the drop day: ")
month = input("Enter the drop month: ")
facility = int(input("Choose your facility:\n1.Football Pitch\n2.AV Room\n"))
hour = 6 if facility == 1 else 21
minute = 1
length = int(input("How many hours do you want to reserve? (1/2): ")) if facility == 2 else None
sHour = input("Enter starting hour of your reservation (hh:mm) ")
eHour = input("Enter ending hour of your reservation (hh:mm) ")
sHour1 = input("Enter starting hour of your 2nd reservation (hh:mm) ") if length == 2 else None
eHour1 = input("Enter ending hour of your 2nd reservation (hh:mm) ") if length == 2 else None
drop = sHour + "\n" + eHour
drop1 = sHour1 + "\n" + eHour1 if length == 2 else None

load_dotenv()
login = os.getenv("MSAGH_EMAIL")
password = os.getenv("MSAGH_PASSWORD")

#Function for clicking the proper reservation button
def res():
    driver.execute_script("document.body.style.zoom='50%'")
    if facility == 1:
        for row in driver.find_elements(By.TAG_NAME, "tr"):
            try:
                godzina = row.find_element(By.TAG_NAME, "th").text

                if godzina == drop:
                    column = row.find_elements(By.TAG_NAME, "td")

                    komorka = column[2]
                    try:

                        reserve = komorka.find_element(By.CLASS_NAME, "reserve")
                        reserve.click()
                        break
                    except:
                        print("Not this time...")
            except:
                pass
    else:
        for row in driver.find_elements(By.TAG_NAME, "tr"):
            try:
                godzina = row.find_element(By.TAG_NAME, "th").text

                if godzina == drop:
                    column = row.find_elements(By.TAG_NAME, "td")
                    komorka = column[1]
                    try:
                        reserve = komorka.find_element(By.CLASS_NAME, "reserve")
                        reserve.click()
                        break
                    except:
                        print("Not this time...")
            except:
                pass

#Seting timer using API
local_before = time.time()
api_time = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Europe/Warsaw").json()['dateTime']
local_after = time.time()
local_at_response = (local_after + local_before) / 2
api_timestamp = datetime.datetime.fromisoformat(api_time).timestamp()
offset = api_timestamp - local_at_response

target_time = datetime.datetime(2025, int(month), int(day), hour, minute, 0)
target_ts = target_time.timestamp()

#webdriver
service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
driver = webdriver.Chrome(service=service)

wait = WebDriverWait(driver, 10)

driver.get("https://panel.dsnet.agh.edu.pl/login")


loginblock = wait.until(EC.visibility_of_element_located((By.ID, "username")))
passblock = wait.until(EC.visibility_of_element_located((By.ID, "password")))

time.sleep(1)

loginblock.send_keys(login)
passblock.send_keys(password)


subblock = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
subblock.click()

#Clicking through
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/reserv/list']"))).click()
if facility == 1:
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/reserv/rezerwujGrupe/2192?self=2192']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)  # pause for scrolling
    element.click()
else:
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/reserv/rezerwuj/2380']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)  # pause for scrolling
    element.click()

#Waiting untill proper time and making a reservation
print(f"Waiting until {target_time.strftime('%H:%M:%S')}...")
while True:
    now = time.time() + offset
    remaining = target_ts - now

    if remaining <= 0:
        driver.refresh()
        res()
        driver.refresh()
        drop = drop1 if drop1 is not None else drop
        res()
        break
    elif remaining < 0.2:
        time.sleep(0.005)
    elif remaining > 300:
        time.sleep(random.uniform(10, 200))
        driver.refresh()
    else:
        time.sleep(random.uniform(0.01, 0.015))

input("Nacisnij enter aby zamknac webdrivera...")

driver.quit()
