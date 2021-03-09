from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "/Users/andrewfillenwarth/Desktop/Projects/selenium/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.rottentomatoes.com/")

search = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "search-text")))

search.send_keys("The Godfather")
view_all = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "View All")))
view_all.click()
show_movies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-page-content"]/div/section[1]/search-result-container/nav/ul/li[3]/span')))
show_movies.click()



time.sleep(10)

driver.close()



