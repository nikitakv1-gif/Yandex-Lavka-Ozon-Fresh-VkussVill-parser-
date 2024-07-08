import undetected_chromedriver as webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common import exceptions 

from Lavka_part.Lavka import open_site, location, sup, bestl
from goods import moscl, get_df

df = det_df()
browser = webdriver.Chrome()

open_site()
location()
sup()
df


