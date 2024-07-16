from shops.Lavka_part import Lavka 
from shops.Ozon_part import Ozon 
from Parser.shops.goods_list import Moscl, get_df
import pandas as pd
import undetected_chromedriver as webdriver

browser = webdriver.Chrome()
df = get_df()
print(df)
location = 'Москва, Запорожская улица, 5'
# lavka = Lavka(Moscl, location, browser, df)
# lavka.open_site()
# lavka.set_location()
# lavka.sup()

ozon = Ozon(Moscl, location, browser, df)
ozon.open_site()
ozon.set_location()
ozon.sup()