from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

driver = None

def initialize_browser():
    global driver
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path='/Users/curtis/Downloads/chromedriver', chrome_options=option)
    driver.implicitly_wait(5)

    driver.get("https://experiments.github.com/semantic-code-search")
    time.sleep(5)

    first_click = driver.find_element_by_xpath('(//ul//li)[1]')
    first_click.click()

def is_exists(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


def scrape(search_command):
    global driver
    #print("1")
    search = driver.find_elements_by_xpath("//input[contains(@name, 'query')]")
    search = search[-1]
    #print("2")
    search.click()
    search.send_keys(search_command)
    #print("3")
    search.send_keys(Keys.ENTER)
    #print("4")

    time.sleep(3)
    res = set()

    for i in range(2, 12, 2):
        driver.find_element_by_xpath(
            "(//code)[" + str(i) + "]")
        print("reached here")
        text = driver.find_element_by_xpath(
            "(//code)[" + str(i) + "]").text

        print(text)
        res.add(text)
    res = list(res)
    #print(res)
    return res
