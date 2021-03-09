from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PATH = "/Users/andrewfillenwarth/Desktop/Projects/selenium/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.rottentomatoes.com/")


try:
    search = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "search-text"))
    )
except:
    print("error on page")
    driver.quit()

# search = driver.find_element_by_class_name("search-text")
search.send_keys("The Godfather")
view_all = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "View All"))
    )
# view_all = driver.find_element_by_link_text("View All")
view_all.click()



driver.close()
