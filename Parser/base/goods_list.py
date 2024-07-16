import pandas as pd
import re
t = pd.read_excel(r"C:\Users\nikit\Downloads\Тестовое задание.xlsx", sheet_name = ['Москва', 'Ростов-на-Дону']) # Считываение имен товаров из Excel 
Mos = t['Москва'].iloc[2:,0].to_list() # Сохраняем в список
Moscl = []
def goods(): # Функция,  которой названия товаров очищаются от имен фирм типо Самокат, Лавка, Озон и тд, если фирма производтель, то ее не трогаем.
    for i in Mos:
        str = i.replace('+', ' ')
        str = re.sub(r'\s+',' ', str.replace('Самокат ', ''))
        if str[-2:] == ' г':
            str = (re.search(r'[\S ]+(?=[,]\s\d+\s[г])', str))
            str = str.group(0)
        Moscl.append(str)
    return Moscl
def get_df(): # Функция создающая датафрейм, в котором будет информация о товарах 
    df =  pd.DataFrame(columns = ['Лавка','Озон','Вкус','ЦЛ', 'ЦЛП','ЦО', 'ЦОП','ЦВ', 'ЦВП'], index = Mos)
    return df
    