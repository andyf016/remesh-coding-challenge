from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
import operator
import json
import time
import argparse

PATH = "/Users/andrewfillenwarth/Desktop/Projects/selenium/chromedriver"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(10)
driver.get("https://www.rottentomatoes.com/")
search_string = ""
list_of_results = []

parser = argparse.ArgumentParser(description='Create Configuration')
parser.add_argument('search_string', type=str, help='search string')
args = parser.parse_args()
search_string = args.search_string

print(search_string)



search = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "search-text")))

search.send_keys(search_string)
try:
    view_all = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "View All")))
    view_all.click()
except:
    
    print("no results to show")
    driver.quit()
show_movies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-page-content"]/div/section[1]/search-result-container/nav/ul/li[3]/span')))
show_movies.click()

while True:
    attached_element_1 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "search-result-container")))
    shadow_root_1 = driver.execute_script("return arguments[0].shadowRoot", attached_element_1)

    attached_element_2 = shadow_root_1.find_element_by_css_selector("search-result[type='movie']")
    shadow_root_2 = driver.execute_script("return arguments[0].shadowRoot", attached_element_2)

    parent_list = shadow_root_2.find_element_by_class_name('list')
    media_rows = parent_list.find_elements_by_tag_name('media-row')
    for row in media_rows:
        props = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', row)
        tom_score = json.loads(props['tomatometerscore'])
        audience_score = json.loads(props['audiencescore'])
        props['audiencescore'] = int(audience_score.get('score', 0))
        props['tomatometerscore'] = int(tom_score.get('score', 0))
        #print(props['tomatometerscore'])
        props['releaseyear'] = int(props.get('releaseyear', 0))
        if operator.contains(props['name'].lower(), search_string.lower()) and (props['audiencescore'] * props['tomatometerscore']) != 0:
            list_of_results.append(props)
        next_button = shadow_root_2.find_element_by_css_selector('button.btn.paging-btn.paging-btn-right')
    try:
        next_button.click()
        time.sleep(5)
    except:
        break


        

sorted_list = sorted(list_of_results, key=operator.itemgetter('tomatometerscore', 'audiencescore', 'releaseyear'), reverse = True)
print(sorted_list[0])








driver.quit()


# <button class="btn paging-btn paging-btn-right" data-qa="paging-btn-next">
#                Next
#            </button>
