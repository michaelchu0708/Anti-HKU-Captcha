from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import cv2
from PIL import Image
import urllib


def main(user, passcode):
    username_str = str(user) if len(str(user))!=0 else "username"
    password_str = str(passcode) if len(str(passcode)) != 0 else "password"

    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(('https://hkuportal.hku.hk/login.html'))
    username_field = browser.find_element_by_id('username')
    username_field.send_keys(username_str)
    password_field = browser.find_element_by_id('password')
    password_field.send_keys(password_str)
    signInButton = browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/form/table/tbody/tr[1]/td[2]/table/tbody/tr/td/input")
    signInButton.click()

    delay = 3 #1s loading time

    #Campus information services
    try:
        button_to_book = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[1]/ul/li[1]/table/tbody/tr[2]/td/div/nav/div[1]/ul/li[3]/a')))
        print("Button to book is up")
        button_to_book = browser.find_element_by_xpath("/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[1]/ul/li[1]/table/tbody/tr[2]/td/div/nav/div[1]/ul/li[3]/a")
        button_to_book.click()
    except TimeoutError:
        print("too much time to load")

    #Service Departments
    try:
        button_to_book1 = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[1]/ul/li[1]/table/tbody/tr[2]/td/div/nav/div[1]/ul/li[3]/ul/li[3]/a')))
        print("Button to book is up")
        button_to_book1.click()
    except TimeoutError:
        print("too much time to load")


    #Centre for Sports and Exercise
    try:
        button_to_book1 = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[1]/ul/li[1]/table/tbody/tr[2]/td/div/nav/div[1]/ul/li[3]/ul/li[3]/ul/li[1]/a')))
        print("Button to book is up")
        button_to_book1.click()
    except TimeoutError:
        print("too much time to load")

    #Sports Facilities Booking
    try:
        button_to_book1 = WebDriverWait(browser,delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[1]/ul/li[1]/table/tbody/tr[2]/td/div/nav/div[1]/ul/li[3]/ul/li[3]/ul/li[1]/ul/li[2]/a')))
        print("Button to book is up")
        button_to_book1.click()
    except TimeoutError:
        print("too much time to load")



    ## Now in sports faciliities booking page

    ####AMEND BELOW PLEASE
    # Currnet Auto Load:       TABLE TENNIS
    #TABLE TENNIS XPATH: /html/body/form/table/tbody/tr[7]/td[1]/a

    try:
        browser.switch_to.window(browser.window_handles[1])
        browser.switch_to_frame(browser.find_element_by_name("contentFrame"))

        button_to_book1 = WebDriverWait(browser, 5)
        button_to_book1 = browser.find_element_by_xpath("/html/body/form/table/tbody/tr[7]/td[1]/a").click()
        print("Sports Facilities Booking page: Booking is up")
    except TimeoutError:
        print("too much time to load")

    #Time slot
    ##Now old version, used to by XPATH, no logic involved
    try:
        Timeslot_button = WebDriverWait(browser,2).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr[14]/td[2]/a')))
        Timeslot_button.click()
        alert = browser.switch_to.alert
        alert.accept()
    except TimeoutError:
        print("too much time in loading")

    #FacitilityBooking, Step1: User type and End time
    try:
        #browser.switch_to_frame(browser.find_element_by_name("contentFrame"))
        UserType_button = WebDriverWait(browser,2).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/table/tbody/tr[4]/td[2]/input[1]'))).click()
        continue_button = WebDriverWait(browser,1).until(EC.presence_of_element_located((By.XPATH,'/html/body/form/table/tbody/tr[9]/td/input[3]'))).click()
    except TimeoutError:
        print("too much time in loading")


    #Facility Booking, Step2: Field: Number + checkbox
    #/html/body/form/table[2]/tbody/tr[4]/td[2]/input
    #/html/body/form/input[2] continue button
    try:
        number_field = WebDriverWait(browser,1).until(EC.presence_of_element_located((By.XPATH,'/html/body/form/table[2]/tbody/tr[4]/td[2]/input')))
        number_field.send_keys("2")
        checkbox = WebDriverWait(browser,1).until(EC.presence_of_element_located((By.XPATH,'/html/body/form/input[1]'))).click()
        continue_button =WebDriverWait(browser,1).until(EC.presence_of_element_located((By.XPATH,'/html/body/form/input[2]'))).click()
    except TimeoutError:
        print("ERRRRRRR")

    import urllib.request
    try:
        img = WebDriverWait(browser,2).until(EC.presence_of_element_located((By.XPATH,'/html/body/form/table/tbody/tr[10]/td[2]/img')))
        #cv2.imshow("temp.py", img)
        #src = img.get_attribute('src')
        #urllib.request.urlretrieve(src, "captcha.png")
        #cap= cv2.imread("captcha.png")
        browser.save_screenshot('tmp.png')
        location = img.location
        print(location)
        x, y = location['x'] + 5, location['y'] + 5
        img = Image.open('tmp.png')
        captcha = img.crop((x, y, x + 200, y + 50))
        captcha.convert("RGB").save('captcha_test.jpg', 'JPEG')

    except TimeoutError:
        print("Error at last step")
    import time
    #for i in range (1, 300):
    #    img = WebDriverWait(browser, 2).until(
    #        EC.presence_of_element_located((By.XPATH, '/html/body/form/table/tbody/tr[10]/td[2]/img')))
    #    src = img.get_attribute('src')
    #    urllib.request.urlretrieve(src, "captcha "+str(i)+".png")
    #    refresh_button = browser.find_element_by_xpath("/html/body/form/table/tbody/tr[10]/td[2]/a").click()
    #    time.sleep(1)

    #image = browser.find_element_by_xpath("/html/body/img")
    #location = image.location
    #print(location)
    #x, y = location['x'] + 5, location['y'] + 5
    #img = Image.open('tmp.png')
    #captcha = img.crop((x, y, x + 200, y + 50))
    #captcha.convert("RGB").save('captcha_test.jpg', 'JPEG')


if __name__=="__main__":
    if len(sys.argv) != 3:
        print("please use the following format in command: {this file name}.py `username` `password`")
        sys.exit(1)
    main(str(sys.argv[1]), str(sys.argv[2]))