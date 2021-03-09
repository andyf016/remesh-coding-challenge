from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

PATH = "/Users/andrewfillenwarth/Desktop/Projects/selenium/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.rottentomatoes.com/")
time.sleep(15)

search = driver.find_element_by_class_name("search-text")
search.send_keys("The Godfather")
view_all = driver.find_element
time.sleep(15)



driver.close()
