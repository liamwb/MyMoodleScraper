"""
A program to download the weeks content for each of my units, and store them in the appropriate locations on my laptop
By Liam Wood-Baker, 2020
"""
import time
import os
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.prompt_for_download": False,  # To auto download files
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
})
driver = webdriver.Chrome('C:/Users/Liam/Drivers/chromedriver.exe', options=options)
password, username = [line.strip('\n') for line in open('DETAILS.txt')]


def backToDashboard():
    """A function to take us back to the dashboard, so we can move onto the next uni"""
    driver.back()
    closeCopyrightWarning()


def login(driver):
    driver.get("https://lms.monash.edu/my/")  # the login screen
    driver.find_element_by_id('okta-signin-username').send_keys(username)  # typing in my username
    driver.find_element_by_id('okta-signin-password').send_keys(password)  # typing in my password
    driver.find_element_by_id('okta-signin-submit').click()  # click the login button

    # wait for a sec, otherwise a stale element reference come up
    time.sleep(3)

    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div/form[1]/div[2]/input').click()
    # click the send push button (it doesn't have an id for some reason)

    input('Press enter once the push has been received')


def closeCopyrightWarning():
    # close the copyright warning
    driver.find_element_by_xpath('/html/body/footer/div/div[1]/div[3]/img').click()


login(driver)
closeCopyrightWarning()

week_number = str(input('Week number? '))


def goToUnit(unit):
    """Navigates to the unit page for a given unit, to be called inside that unit's scrape function"""
    soup = BeautifulSoup(driver.page_source, 'lxml')
    homepage_buttons = soup.findAll('span', class_='multiline')
    for button in homepage_buttons:
        if unit in button.string:
            driver.get(button.parent['href'])


def doDirectory(week):
    """creating the directory to save files to, if it already doesn't exist. To be called in a unit's scrape function"""
    directory = 'C:/Users/Liam/Uni/ATS2005/Week ' + week_number
    print('downloads will go to ' + directory)
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def createTempDriver(options, directory):
    """Creates a new driver variable which will download files to directory"""
    # Once we have the links we want, and we need to download them to the appropriate directory. To do this, we have to
    # make a new driver, with the default download directory changed (can't change the download directory without
    # restarting the driver.
    temp_options = options
    temp_options.add_experimental_option('prefs', {
        "download.default_directory": directory.replace('/', '\\'),  # apparently selenium broke forward slashes
        "download.prompt_for_download": False,  # To auto download files
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })
    return webdriver.Chrome('C:/Users/Liam/Drivers/chromedriver.exe', options=temp_options)


def scrapeMAT1830():
    """Downloads the two tutorial sheets"""
    directory = doDirectory(week_number)
    goToUnit('MAT1830')

    soup = BeautifulSoup(driver.page_source, 'lxml')  # lxml is an HTML parser
    soup.find(string='Tutorial sheet ' + str(int(week_number) - 1))
    instancenames = soup.findAll('span', class_='instancename')  # the name of the file (ie 'Tutorial sheet 2) is stored
    # in these tags, but the links are in these tags' parents

    # finding the tutorial sheets
    for tag in instancenames:  # week n contains tutorial sheet n-1
        if 'Tutorial sheet ' + str(int(week_number) - 1) in tag:  # the tutorial sheet we want
            tutorial_sheet_link = tag.parent['href']
            print('found tutorial sheet')
        if 'Tutorial sheet ' + str(int(week_number) - 1) + ' solutions' in tag:  # the solutions
            solutions_link = tag.parent['href']
            print('found tutorial sheet solutions')

    temp_driver = createTempDriver(options, directory)
    login(temp_driver)  # now we're logged in in the new window (which has the correct download directory)

    temp_driver.execute_script("window.open('');")
    temp_driver.switch_to.window(temp_driver.window_handles[1])
    temp_driver.get(tutorial_sheet_link)  # get the tutorial sheet in a new tab
    temp_driver.get(solutions_link)  # then the solutions
    temp_driver.close()  # then close the window


def scrapeATS2005():
    """Downloads the week's lecture"""
    directory = doDirectory(week_number)
    goToUnit('ATS2005')

    # getting to the right week
    soup = BeautifulSoup(driver.page_source, 'lxml')
    dropdowns = soup.findAll('div', class_='arts-banner-dropdown-content')
    for menu in dropdowns:
        for option in menu.children:
            if 'Week ' + week_number in option.string:
                driver.get(option['href'])

    # finding the lecture
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for resource in soup.findAll('span', class_='resourcelinkdetails'):
        if 'Video file' in resource.string:
            video_link = resource.parent.find('a', class_='')['href']

    driver.get(video_link)  # get to the page that has the video embedded in it
    soup = BeautifulSoup(driver.page_source, 'lxml')
    final_link = soup.find('video').find('source')['src']  # the link is in the source tag, inside the video tag
    driver.get(final_link)

    # this doesn't work
    # urllib.request.urlretrieve(final_link, 'videoname.mp4')

    # this isn't needed if the above doesn't work
    # # open a window with the correct download directory
    # temp_driver = createTempDriver(options, directory)
    # login(temp_driver)
    #
    # # open a new tab for the video
    # temp_driver.execute_script("window.open('');")
    # temp_driver.switch_to.window(temp_driver.window_handles[1])
    #
    # # get to the page which is actually the video
    # temp_driver.get(final_link)

# scrapeMAT1830()
# driver.back()
# closeCopyrightWarning()
# time.sleep(3)
scrapeATS2005()
