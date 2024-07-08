from goods import Moscl
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common import exceptions 
from translit import transliterate
class Lavka():
    url_lavka = 'https://lavka.yandex.ru'
    price = 'div/div/div/div[1]/div[1]/div/div/div/span[4]/span[1]'
    full_price = 'div/div/div/div[1]/div[1]/div/div/div/span[4]/span[2]/span[1]'
    name = 'div/div/div/div[1]/div[1]/div/h3'
    weight = 'div/div/div/div[1]/div[1]/span/span/span/span/span'
    searchstr = "search-input-id"
    check = '/html/body/div/div[3]/div[1]/main/div/div/div/div[1]/div/div/h2'
    class_of_supply_el = 'c8uba0o'
    address_button = "/html/body/div/div[1]/header/div[2]/div[3]/button"
    adrstr = "/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/input"
    first_address = '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/ul/li[1]'
    OK_button = '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button'
    def __init__(self, list, location, browser, df):
        self.names = list
        self.location = location
        self.browser = browser
        self.df = df
    def open_site(self):
        self.browser.get(self.url_lavka)
    def set_location(self):
        # wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,self.address_button))).click()
        # adrsstr = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,self.adrstr)))
        # adrsstr.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        # adrsstr.send_keys(self.location)
        # sleep(2)
        # adrsstr.send_keys(Keys.SPACE)
        # sleep(1)
        # wait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH, self.first_address))).click()
        # but = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, self.OK_button)))
        # sleep(2)
        # but.click()
        address = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div[1]/header/div[2]/div[3]/button"))).click()
        adrsstr = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/input")))
        adrsstr.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        adrsstr.send_keys('Москва, Запорожская улица, 5')
        sleep(2)
        adrsstr.send_keys(Keys.SPACE)
        sleep(1)
        wait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/ul/li[1]'))).click()
        but = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button')))
        sleep(2)
        but.click()
    def bestl(self, t, nm, k):
        nmt = transliterate(nm)
        c = 0
        best = ''
        for lt in t:
            link = lt.find_element(By.TAG_NAME, 'a').get_attribute('href')
            price = lt.find_element(By.XPATH, self.price).text
            full_price = lt.find_element(By.XPATH, self.full_price).text
            name = lt.find_element(By.XPATH, self.name).text
            weight = lt.find_element(By.XPATH, self.weight).text
            if c == 0:
                price_of_best = price 
                full_price_of_best = full_price
                name_of_best = name 
                weight_best = weight
                c += 1
            try:
                nameinlink = link.split(r'/')[-1]
                if nmt.split().issubset(nameinlink.lower()) or nameinlink.split().lower().issubset(nmt):
                    price_of_best = price 
                    full_price_of_best = full_price
                    name_of_best = name 
                    weight_best = weight
                    break
            except:
                break
        print(price_of_best, full_price_of_best)
        self.df.iloc[k, 0] = name_of_best + ', ' + weight_best
        self.df.iloc[k, 3] = price_of_best
        self.df.iloc[k, 4] = full_price_of_best
    def sup(self):
        for k in range(len(Moscl)):
            i = Moscl[k]
            searchbar = wait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, self.searchstr)))
            searchbar.click()
            searchbar.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
            searchbar.send_keys(i)
            wait(self.browser, 15).until(EC.text_to_be_present_in_element((By.XPATH, self.check), i))
            t = self.browser.find_elements(By.CLASS_NAME, self.class_of_supply_el)
            self.bestl(t, i, k)
        