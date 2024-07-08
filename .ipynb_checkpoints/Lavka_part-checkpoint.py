from goods import Moscl
from time import sleep

class Lavka:
    url_lavka = 'https://lavka.yandex.ru'
    price = 'div/div/div/div[1]/div[1]/div/div/div/span[4]/span[1]'
    full_price = 'div/div/div/div[1]/div[1]/div/div/div/span[4]/span[2]/span[1]'
    name = 'div/div/div/div[1]/div[1]/div/h3'
    weight = 'div/div/div/div[1]/div[1]/span/span/span/span/span'
    searchstr = "search-input-id"
    check = '/html/body/div/div[3]/div[1]/main/div/div/div/div[1]/div/div/h2'
    class_of_supply_el = 'c8uba0o'
    address_button = "/html/body/div/div[1]/header/div[2]/div[3]/button"
    addressstr = "/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/input"
    first_address = '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/ul/li[1]'
    OK_button = '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button'
    def __init__(self, list, location):
        self.names = list
        self.location = location
    def open_site():
        browser.get(url_lavka)
    def location():
        address = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH,address_button))).click()
        adrsstr = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH,adressstr)))
        adrsstr.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        adrsstr.send_keys(self.location)
        sleep(2)
        adrsstr.send_keys(Keys.SPACE)
        sleep(1)
        wait(browser, 15).until(EC.presence_of_element_located((By.XPATH, first_address))).click()
        but = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH, OK_button)))
        sleep(2)
        but.click()
    def sup(df):
        for k in range(len(Moscl)):
            i = Moscl[k]
            searchbar = wait(browser, 10).until(EC.presence_of_element_located((By.ID, searchstr)))
            searchbar.click()
            searchbar.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
            searchbar.send_keys(i)
            wait(browser, 15).until(EC.text_to_be_present_in_element((By.XPATH, check), i))
            t = browser.find_elements(By.CLASS_NAME, class_of_supply_el)
            bestl(t, i, k, df)
    def bestl(t, nm, k, df):
        nmt = transliterate(nm)
        c = 0
        best = ''
        for lt in t:
            print(lt)
            link = lt.find_element(By.TAG_NAME, 'a').get_attribute('href')
            price = lt.find_element(By.XPATH, price).text
            full_price = lt.find_element(By.XPATH, full_price).text
            name = lt.find_element(By.XPATH, name).text
            weight = lt.find_element(By.XPATH, weight).text
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
        df.iloc[k, 0] = name + ', ' + weight
        df.iloc[k, 3] = price_of_best
        df.iloc[k, 4] = full_price_of_best
        