from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from base.translit import transliterate
from selenium.common import exceptions 

class Ozon:
    searchstr = '/html/body/div[1]/div/div[1]/header/div[1]/div/div[2]/div/div/form/div/div[2]/input' # Посковая строка на сайте, по value этого элемента проверяется также обновление карточек
    price = 'div[1]/div[1]/div/span[1]'# Xpath к цене от объекта карточки (class_of_supply_el)
    full_price = 'div[1]/div[1]/div/span[2]' # Xpath к полной цене, без скидки
    name = 'div[1]/a/div/span'# Xpath к цене
    selector_of_supply_el = '#paginatorContent > div > div > div > div' # Selector карточки товара
    url_ozon = 'https://www.ozon.ru/category/supermarket-25000/?__rr=1&miniapp=supermarket' # Ссылка на сайт
    button_address = '/html/body/div[1]/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/button' # Кнопка открывающая окно ввода адреса
    address_string = '/html/body/div[8]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/form/div/div/fieldset/div[1]/div/div/div/label/div[1]/div/textarea' #Строка для ввода адреса
    cross_address_string = '/html/body/div[4]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/form/div/div/fieldset/div[1]/div/div/div/label/div[1]/div/div/div/button/span' # Кнопка очистки, строки для ввода адреса
    first_submit_button = '/html/body/div[5]/div/div/div/div'# Выподающее меню выбора адреса 
    second_submit_button = '/html/body/div[4]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div[2]/button'# Кнопка сохранения адреса
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
            save_but = wait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, self.second_submit_button))).click()
            sleep(0.1)
            save_but.click()
        except:
            print('Проблема установки адреса, впишите его в ручную, проверьте, что адрес введен на Ozon fresh и введите в консоль какой либо символ')
            input()
    def sup(self):
        """Находит карточки всех доступных товаров, по данному запросу"""
        for k in range(len(self.names)):
            i = self.names[k]
            searchbar = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, self.searchstr)))
            searchbar.click()
            if k != 0:
                searchbar.click()
                sleep(0.1)
                searchbar.clear()
                sleep(0.1)
            searchbar.send_keys(i)
            searchbar.send_keys(Keys.ENTER)
            wait(self.browser, 15).until(EC.text_to_be_present_in_element_value((By.XPATH, self.searchstr), i))
            try:
                t = self.browser.find_elements(By.CSS_SELECTOR, self.selector_of_supply_el)
            except:
                try:
                    t = self.browser.find_elements(By.CSS_SELECTOR, self.selector_of_supply_el)
                except: 
                    print("Ошибка поиска товаров")
                    break
            c = 0
            nmt = transliterate(i)
            if len(t) != 0:
                for lt in t:
                    link = lt.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    price = lt.find_element(By.XPATH, self.price).text
                    full_price = lt.find_element(By.XPATH, self.full_price).text
                    name = lt.find_element(By.XPATH, self.name).text
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
                self.df.iloc[k, 1] = name_of_best
                self.df.iloc[k, 5] = price_of_best
                self.df.iloc[k, 6] = full_price_of_best
            else:
                self.df.iloc[k, 1] = '-'
                self.df.iloc[k, 5] = '-'
                self.df.iloc[k, 6] = '-'