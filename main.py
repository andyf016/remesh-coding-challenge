from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import json
import time

PATH = "/Users/andrewfillenwarth/Desktop/Projects/selenium/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.rottentomatoes.com/")
search_string = "The Godfather"
list_of_results = []
final_result = {}

search = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "search-text")))

search.send_keys(search_string)
view_all = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "View All")))
view_all.click()
show_movies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-page-content"]/div/section[1]/search-result-container/nav/ul/li[3]/span')))
show_movies.click()

attached_element_1 = driver.find_element_by_tag_name("search-result-container")
shadow_root_1 = driver.execute_script("return arguments[0].shadowRoot", attached_element_1)
attached_element_2 = shadow_root_1.find_element_by_css_selector("search-result[type='movie']")
shadow_root_2 = driver.execute_script("return arguments[0].shadowRoot", attached_element_2)
parent_list = shadow_root_2.find_element_by_class_name('list')
media_rows = parent_list.find_elements_by_tag_name('media-row')
for row in media_rows:
    props = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', row)
    tom_score = json.loads(props['tomatometerscore'])
    print(props['name'])
    print(tom_score.get('score'))
    # list_of_results.append(props)


driver.quit()



