from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common import exceptions 
from base.translit import transliterate
class Lavka():
    url_lavka = 'https://lavka.yandex.ru' # Ссылка на сайт
    price = 'div/div/div/div[1]/div[1]/div/div/div/span[4]/span[1]' #относительный Xpath до цен, от элемента карточки товара
    full_price = 'div/div/div/div[1]/div[1]/div/div/div/span[4]/span[2]/span[1]' # Относительный Xpath до полной цены, без скидки
    name = 'div/div/div/div[1]/div[1]/div/h3' # Относительнй Xpath до имени товара
    weight = 'div/div/div/div[1]/div[1]/span/span/span/span/span' # Относительный Xpath до веса товара
    searchstr = "search-input-id" # Класс обекта строки поиска на сайте 
    check = '/html/body/div/div[3]/div[1]/main/div/div/div/div[1]/div/div/h2' # "Элемент сайта, который дублирует запрос в строке, по нему можно проверить обновил ли сайт карточки"
    class_of_supply_el = 'c8uba0o' # Класс карточки элемента
    address_button = "/html/body/div/div[1]/header/div[2]/div[3]/button" #Кнопка смены адреса
    adrstr = "/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/input" # Строка ввода адреса
    first_address = '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/ul/li[1]' # Нажатие на первый элемент выпадающего списка адресов
    OK_button = '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button' # Кнопка подтверждения адреса
    def __init__(self, list, location, browser, df):
        self.names = list # Имена товаров, чистые, Moscl в main файле
        self.location = location # Местоположение введенное пользователем 
        self.browser = browser 
        self.df = df
    def open_site(self):
        """Открывает сайт магазина"""
        self.browser.get(self.url_lavka)
    def set_location(self):
        """Устанавливает адрес пользователя"""
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
        try:
            address = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,self.address_button))).click() # Нажимаем на кнопку, чтобы открылось окно смены адреса 
            adrsstr = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,self.adrstr))) # Сохраняем объект строки для ввода адресак
            adrsstr.send_keys(Keys.CONTROL + 'a' + Keys.DELETE) # Удаляем то, что Яндекс автоматически вставляет
            adrsstr.send_keys('Москва, Запорожская улица, 5') #Вписываем нужное
            sleep(2)
            adrsstr.send_keys(Keys.SPACE) #Ставим пробел, чтобы появился правильный выпадающий список
            sleep(1)
            wait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH,self.first_address))).click() # Кликаем на первый элемент выпадающего списка адресов
            but = wait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, self.OK_button))) #Сохраняем элемент кнопки потверждающей введенный адрес
            sleep(2)
            but.click() # Завершаем установку адреса, кликая на кнопку ОК
        except:
            print('Проблема установки адреса, впишите его в ручную, проверьте, что адрес введен на Ozon fresh и введите в консоль какой либо символ')
            input()
    def sup(self):
        """Находит карточки всех доступных товаров, по данному запросу"""
        for k in range(len(self.names)): # Запускаем цикл, для того, чтобы сделать запросы по всем элементам списка
            i = self.names[k] # Сохраняем название товара в прееменную
            #TO-DO Посмотреть имеет ли смысл каждый раз создавать новый объект поисковой строки или можно до цикла один раз создать
            searchbar = wait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, self.searchstr))) # Создается объект поисковой строки
            searchbar.click()
            searchbar.send_keys(Keys.CONTROL + 'a' + Keys.DELETE) # Удаляется информация из него
            searchbar.send_keys(i) # Вводится запрос
            wait(self.browser, 15).until(EC.text_to_be_present_in_element((By.XPATH, self.check), i)) # Ждем пока изменится элемент, который отображает наш запрос на сайте
            t = self.browser.find_elements(By.CLASS_NAME, self.class_of_supply_el)  # Находим карточки элементов
            c = 0 
            nmt = transliterate(i) #Создаем название товара в виде транслита, для сравнения с транслитом из ссылок на товары
            for lt in t: # Цикл в котором проходимся по всей выдаче
                link = lt.find_element(By.TAG_NAME, 'a').get_attribute('href') # Вытаскиваем ссылку на товар
                price = lt.find_element(By.XPATH, self.price).text # Цену 
                #TO-DO Найти товар без скидки, чтобы посмотреть как меняется карточка
                full_price = lt.find_element(By.XPATH, self.full_price).text # Цену без скидки
                name = lt.find_element(By.XPATH, self.name).text #Имя товара
                weight = lt.find_element(By.XPATH, self.weight).text # Вес
                if c == 0: # Проверяется первый ли это товар и если первый, сохраняется как наиболее подходящий
                    price_of_best = price 
                    full_price_of_best = full_price
                    name_of_best = name 
                    weight_best = weight
                    c += 1
                try:
                    nameinlink = link.split(r'/')[-1] # Из ссылки убираем все ненужное и оставляем только название товара 
                    if nmt.split().issubset(nameinlink.lower()) or nameinlink.split().lower().issubset(nmt): #Сравниваем ссылку и запрос в виде транслита
                        price_of_best = price 
                        full_price_of_best = full_price
                        name_of_best = name 
                        weight_best = weight
                        break
                except:
                    break
            # Записываем наиболее подходящий товар в датафрейм
            print(self.df)
            self.df.iloc[k, 0] = name_of_best + ', ' + weight_best 
            self.df.iloc[k, 3] = price_of_best
            self.df.iloc[k, 4] = full_price_of_best