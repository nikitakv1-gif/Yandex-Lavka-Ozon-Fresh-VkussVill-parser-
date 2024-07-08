import pandas as pd
import re

t = pd.read_excel(r"C:\Users\nikit\Downloads\Тестовое задание.xlsx", sheet_name = ['Москва', 'Ростов-на-Дону'])
Mos = t['Москва'].iloc[2:,0].to_list()
Mos
Moscl = []
for i in Mos:
    str = i.replace('+', ' ')
    str = re.sub(r'\s+',' ', str.replace('Самокат ', ''))
    if str[-2:] == ' г':
        str = (re.search(r'[\S ]+(?=[,]\s\d+\s[г])', str))
        str = str.group(0)
    Moscl.append(str)
def get_df():
    df =  pd.DataFrame(columns = ['Лавка','Озон','Вкус','ЦЛ', 'ЦЛП','ЦО', 'ЦОП','ЦВ', 'ЦВП'], index = Mos)
    return df
    