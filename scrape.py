from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time


def is_exists(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


def scrape(search_command):

    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        executable_path='/Users/Akshay Saxena/Downloads/chromedriver', chrome_options=option)

    driver.get("https://experiments.github.com/semantic-code-search")
    time.sleep(5)

    first_click = driver.find_element_by_xpath('(//ul//li)[1]')
    first_click.click()
    time.sleep(5)
    print("here")

    search = driver.find_element_by_xpath("//input[contains(@name, 'query')]")
    search.send_keys(search_command)
    search.send_keys(Keys.ENTER)
    time.sleep(3)
    res = []

    for i in range(2, 12, 2):
        j = 1
        res_in = []

        driver.find_element_by_xpath(
            "(//code)[" + str(i) + "]")
        print("reached here")
        text = driver.find_element_by_xpath(
            "(//code)[" + str(i) + "]").text

        print(text)
        res_in.append(text)
        res.append(res_in)

    print(res)
    return res


scrape("run time")
