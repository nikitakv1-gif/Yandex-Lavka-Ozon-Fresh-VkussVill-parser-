from goods import Moscl
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common import exceptions 
from translit import transliterate

class Ozon():
    searchstr = '/html/body/div[1]/div/div[1]/header/div[1]/div/div[2]/div/div/form/div/div[2]/input' # Посковая строка на сайте
    price = '/div[1]/div[1]/div/span[1]' # Xpath к цене от объекта карточки (class_of_supply_el)
    full_price = 'div[1]/div[1]/div/span[2]/text()' # Xpath к полной цене, без скидки
    name = 'div[1]/a/div/span' # Xpath к цене
    class_of_supply_el = 'j8j_23' # Класс карточки элемента
    url_ozon = 'https://www.ozon.ru/category/supermarket-25000/?__rr=1&miniapp=supermarket' # Ссылка на сайт
    button_address = '/html/body/div[1]/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/button' # Кнопка открывающая окно ввода адреса
    address_string = '/html/body/div[4]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/form/div/div/fieldset/div[1]/div/div/div/label/div[1]/div/textarea' #Строка для ввода адреса
    cross_address_string = '/html/body/div[4]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/form/div/div/fieldset/div[1]/div/div/div/label/div[1]/div/div/div/button/span' # Кнопка очистки, строки для ввода адреса
    first_submit_button = '/html/body/div[5]/div/div/div/div' # Выподающее меню выбора адреса 
    second_submit_button = '/html/body/div[4]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[2]/button' # Кнопка сохранения адреса
    def __init__(self, list, location, browser, df):
        self.names = list
        self.location = location
        self.browser = browser
        self.df = df
    def open_site(self):
        """Открывает сайт магазина"""
        self.browser.get(self.url_ozon)
    def set_location(self):
        """В случае если в брауезере на сайте не выставлен адрес произойдет его установка"""
        # to-do Проверка локации на сайте, если она совпадает с введенной хотя бы отчасти, то не трогаем и скипаем,
        # иначе все что снизу + при первом заходе на сайт, выставление геолокации для обычного озона
        try:
            x_but = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, self.button_address)))
            sleep(0.1)
            x_but.click()
            adrstro = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, self.address_string)))
            wait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH, self.cross_address_string))).click()
            adrstro.send_keys(self.location)
            sleep(0.5)
            adrstro.send_keys(Keys.ENTER)
            sleep(1)
            wait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH, self.first_submit_button))).click()
            sleep(2)
            #wait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[2]/button'))).click()
            save_but = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, self.second_submit_button)))
            sleep(0.1)
            save_but.click()
        except:
            pass
    def bestl(self, t, nm, k):
        # to-do Написать функцию, которая заменит чать с try except и будет лучше определять наиболее подходящий товар
        """Проходит по всем товарам и определяет самый лучший"""
        nmt = transliterate(nm)
        c = 0
        best = ''
        for lt in t:
            link = lt.find_element(By.TAG_NAME, 'a').get_attribute('href')
            price = lt.find_element(By.XPATH, price).text
            full_price = lt.find_element(By.XPATH, full_price).text
            name = lt.find_element(By.XPATH, name).text
            if c == 0:
                price_of_best = price 
                full_price_of_best = full_price
                name_of_best = name 
                c += 1
            try:
                nameinlink = link.split(r'/')[-1]
                if nmt.split().issubset(nameinlink.lower()) or nameinlink.split().lower().issubset(nmt):
                    price_of_best = price 
                    full_price_of_best = full_price
                    name_of_best = name 
                    break
            except:
                break
        self.df.iloc[k, 0] = name
        self.df.iloc[k, 3] = price_of_best
        self.df.iloc[k, 4] = full_price_of_best
    
    def sup(self):
        """Находит карточки всех доступных товаров, по данному запросу"""
        for k in range(len(Moscl)):
            i = Moscl[k]
            searchbar = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, self.searchstr)))
            searchbar.click()
            searchbar.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
            searchbar.send_keys(i)
            searchbar.send_keys(Keys.ENTER)
            wait(self.browser, 15).until(EC.text_to_be_present_in_element_value((By.XPATH, self.searchstr), i))
            t = self.browser.find_elements(By.CLASS_NAME, self.class_of_supply_el)
            self.bestl(t, i, k)