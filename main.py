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

# PATH must be updated to the location of chromedrive on your machine!
PATH = "/Users/andrewfillenwarth/Desktop/Projects/selenium/chromedriver"
driver = webdriver.Chrome(PATH)

# set the time for the driver to wait for elements to load
driver.implicitly_wait(10)

# declare empty list for results from the search 
search_string = ""
list_of_results = []

# set up an arg parser to take a search string from the command line
# this argument is required
parser = argparse.ArgumentParser(description='Search For a Movie')
parser.add_argument('search_string', type=str, help='search string')
args = parser.parse_args()
search_string = args.search_string


print(f'Searching for movie with string filter {search_string}')

# open chrome and navigate to rotten tomatoes home page
driver.get("https://www.rottentomatoes.com/")

# find the search bar element and send the search string to it
search = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "search-text")))
search.send_keys(search_string)

# this try excep block verifies that there are some initial results by checking for the presence of the 'view all" link
try:
    view_all = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "View All")))
    view_all.click()
except:
    print("no results to show")
    driver.quit()

# after navigating to the results page the driver will click on the movies filter 
show_movies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-page-content"]/div/section[1]/search-result-container/nav/ul/li[3]/span')))
show_movies.click()

# this while loop gathers search results and adds them to a list of final results
while True:
    
    # this where we start to navigate down through the shadow dom level by level
    attached_element_1 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "search-result-container")))
    shadow_root_1 = driver.execute_script("return arguments[0].shadowRoot", attached_element_1)
    
    attached_element_2 = shadow_root_1.find_element_by_css_selector("search-result[type='movie']")
    # at each level we inject this javascript to enable navigation through the shadow dom
    shadow_root_2 = driver.execute_script("return arguments[0].shadowRoot", attached_element_2)

    # this is the desired level it contains the custom tags that have all the movie info and the 'next' button
    parent_list = shadow_root_2.find_element_by_class_name('list')
    media_rows = parent_list.find_elements_by_tag_name('media-row')
    
    # the find_elements_ method returns a list of media-row tags
    for row in media_rows:
        # the media rows contain all the movie info as props
        # this injected javascript will return the props as key: value pairs
        # this line was adapted from stackoverflow.com
        props = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', row)
        # the audience score and critic scores are stored as key: value strings within the main dict 
        # here they are parsed by the json library to access only the score number and nothing else
        tom_score = json.loads(props['tomatometerscore'])
        audience_score = json.loads(props['audiencescore'])

        # the scores are cast to integers and made 0 if they are 'none'
        # this is to help wit hsorting later
        props['audiencescore'] = int(audience_score.get('score', 0))
        props['tomatometerscore'] = int(tom_score.get('score', 0))
        props['releaseyear'] = int(props.get('releaseyear', 0))

        # this if statement filters results that dont match the search string and contain a zero score
        if operator.contains(props['name'].lower(), search_string.lower()) and (props['audiencescore'] * props['tomatometerscore']) != 0:
            list_of_results.append(props)
        # find the next button
        # re intiialize it each time to help prevent a stale element refrence error 
        next_button = shadow_root_2.find_element_by_css_selector('button.btn.paging-btn.paging-btn-right')
    try:
        # click the button if it is there
        next_button.click()
        # the sleep function is also here to help prevent a stale element refrence error 
        time.sleep(5)
    except:
        # break the while loop when there is no longer a next button
        break


        
# sort the list by the criteria required
sorted_list = sorted(list_of_results, key=operator.itemgetter('tomatometerscore', 'audiencescore', 'releaseyear'), reverse = True)

# get the top movie from the list and print it's properties
final_movie = sorted_list[0]
print(f'The best match for movie search string {search_string} is: ')
print('Title: ' + final_movie['name'])
print('Release Year: ' + final_movie['releaseyear'])
print('Critic Score: ' + final_movie['tomatometerscore'])
print('Audience Score ' + final_movie['audiencescore'])
print('URL: ' + final_movie["url"])



driver.quit()