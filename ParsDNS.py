from bs4 import BeautifulSoup
import requests
import xlrd, xlwt

wb = xlwt.Workbook()
ws = wb.add_sheet('sheet0', cell_overwrite_ok=True)

Checking = True
count = 1   # Минимально-возможная страница
i = 0   #Для работы со столбцами
ii = 0  #Для работы со строками

name = str(input("Введите названия для файла без расширения: "))

while Checking:

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                            ' Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'}

    url_content = requests.get(r'https://technopoint.ru/catalog/17a8a01d16404e77/smartfony/?p={}&order=1&groupBy=avails&f[pqc]=o8r3o&stock=2'.format(count),     #Где ?p={} {0}
                               headers = headers)

    url_soup = BeautifulSoup(url_content.text,'html.parser')


    if not url_soup.find_all("div","catalog-item"):
        print("Запись окончена. На страницах больше нет данных. файл .xls сохранен в рабочем каталоге.")
        Checking = False
        break


    count_items = 0

    for check in url_soup.find_all("div","catalog-item"):
        ii=0
        price_content = requests.get('https://technopoint.ru/{}'.format(check.find('a','ui-link').get('href')),
                               headers = headers)
        price_soup = BeautifulSoup(price_content.text,'html.parser')
        price_forstring = price_soup.find('span','current-price-value').text.split()[0]+price_soup.find('span','current-price-value').text.split()[1]

        item_list = [
            int(price_soup.find('div','price-item-code').find('span').text),     #Код продукта
            check.find('div', 'product-info__title-link').text,     #Информация о продукте
            check.find('span', 'product-info__title-description').text,     #Характеристики продукта
            price_forstring     #Цена в руб
        ]
        for item in item_list:
            ws.write(i,ii,item)
            ii+=1
        i+=1
        print(item_list)
        wb.save('{}.xls'.format(name))
        print('Сохранено\n')

    else:
        count+=1
