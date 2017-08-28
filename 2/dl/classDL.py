from bs4 import BeautifulSoup as bs
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://uaccess.schedule.arizona.edu/psp/uazsaprd2/UA_SCHEDULE/HRMS/h/?tab=DEFAULT'

driver = webdriver.PhantomJS('/Users/jack/bin/phantomjs-2.1.1-macosx/bin/phantomjs')
driver.set_window_size(1920,1080)
driver.get(url)

try:
    element = WebDriverWait(driver, 10)\
                .until( EC.element_to_be_clickable( (By.ID, 'UA_CLAS_SRCH_WK_SSR_PB_SRCH')) )
finally:
    #first radio button
    driver.find_element_by_id('UA_CLAS_SRCH_WK_UA_CLSRCH_OPT$3$').click()
    sleep(10)
    #search
    driver.find_element_by_id('UA_CLAS_SRCH_WK_SSR_PB_SRCH').click()



try:
    element = WebDriverWait(driver, 60)\
                .until( EC.presence_of_element_located( (By.ID, 'SSR_CLSRCH_WRK_SSR_OPEN_ONLY$chk$0')) )
finally:
    driver.save_screenshot('a.png')
    #uncheck open class only

    source = driver.page_source
    print source

    driver.find_element_by_id('SSR_CLSRCH_WRK_SSR_OPEN_ONLY$chk$0').value = 'N'
    
    #subjects
    subjects = driver.find_element_by_id('SSR_CLSRCH_WRK_SUBJECT_SRCH$1')
    for s in subjects:
        print s.text
    
    #search
    'CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH'

    source = driver.page_source
    #b = bs(driver.page_source, 'lxml')
    #print b.findAll('input', {'type':'radio'})

#driver.close()


