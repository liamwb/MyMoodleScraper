"""
A program to download the weeks content for each of my units, and store them in the appropriate locations on my laptop
By Liam Wood-Baker, 2020
"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome('C:/Users/Liam/Drivers/chromedriver.exe')
password, username = [line.strip('\n') for line in open('DETAILS.txt')]


driver.get("https://lms.monash.edu/my/")  # the login screen

driver.find_element_by_id('okta-signin-username').send_keys(username)  # typing in my username
driver.find_element_by_id('okta-signin-password').send_keys(password)  # typing in my password
driver.find_element_by_id('okta-signin-submit').click()  # click the login button


# wait for a sec, otherwise a stale element reference come up
time.sleep(3)

driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div/form[1]/div[2]/input').click()
# click the send push button (it doesn't have an id for some reason

input('Press enter once the push has been received')

