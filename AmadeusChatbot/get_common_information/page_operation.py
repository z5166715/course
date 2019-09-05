from selenium import webdriver
import time
import bs4


# driver = webdriver.Chrome()
# prefix = url = 'https://www.handbook.unsw.edu.au/ArchitectureAndBuilding/browse?interest_value=68b44253db96df002e4c126b3a961980'
# driver.get(url)


def get_full_page(driver):
    while True:
        try:
            driver.find_element_by_xpath('//button[@class="a-browse-more-controls-btn"][@data-type="Program"]').click()
            time.sleep(1)
        except:
            break
    while True:
        try:
            driver.find_element_by_xpath('//button[@class="a-browse-more-controls-btn"][@data-type="Specialisation"]').click()
            time.sleep(1)
        except:
            break
    while True:
        try:
            driver.find_element_by_xpath('//button[@class="a-browse-more-controls-btn"][@data-type="Double Degree"]').click()
            time.sleep(1)
        except:
            break
    while True:
        try:
            driver.find_element_by_xpath('//button[@class="a-browse-more-controls-btn"][@data-type="Course"]').click()
            time.sleep(1)
        except:
            break
    return driver



# for degree in ["Undergraduate","Postgraduate","Research"]:
# driver.find_element_by_xpath('//button[@aria-controls="Undergraduate"]').click()
# driver = get_full_page(driver)