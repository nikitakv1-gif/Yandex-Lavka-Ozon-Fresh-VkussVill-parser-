from shops.Lavka_part import Lavka 
from shops.Ozon_part import Ozon 
from base.goods_list import goods, get_df
from base.browser_create import get_browser
import pandas as pd

def collect():
    browser = get_browser() #запускается объект браузера, в котором потом будут происходить все действия
    df = get_df() #создается датафрейм, в котором будут храниться все наименования и цены товаров
    Moscl = goods() # Названия товаров очищенные от названий компаний продавцов, самокат, озон, лавка и тд. Надеюсь самокаты продавать они не станут, иначе придется переписывать функцию.
    location = 'Москва, Запорожская улица, 5' # Вместо строки будет функция ввода адреса, но пока строка
    lavka = Lavka(Moscl, location, browser, df) # создаем объект класса Лавка
    lavka.open_site() #Открываем сайт
    lavka.set_location() # Устанавливаем локацию #TO_DO добавить проверку, того что предыдущая локация действительно удалилась
    lavka.sup() # Собираем лучшее совпадение для каждого товара
    file_name = 'test.xlsx' 
    df.to_excel(file_name) # Сохранение датафрейма в Excel
# ozon = Ozon(Moscl, location, browser, df)
# ozon.open_site()
# ozon.set_location()
# ozon.sup()

if __name__ == "__main__":
    collect()
    