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

username_field = driver.find_element_by_id('okta-signin-username')  # the username field
username_field.send_keys(username)
password_field = driver.find_element_by_id('okta-signin-password')  # the password field
password_field.send_keys(password)
sign_in_button = driver.find_element_by_id('okta-signin-submit')  # the login button
sign_in_button.click()


# wait for a sec, otherwise a stale element reference come up
time.sleep(3)

push_button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div/form[1]/div[2]/input')
# the send push button
push_button.click()
input('Press a key once the push has been received')

