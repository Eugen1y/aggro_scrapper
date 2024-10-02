import pandas as pd

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache'
}


def read_urls(filename):
    """
    Читает URL из указанного файла Excel.

    :param filename: str - Путь к файлу Excel, содержащему ссылки.
    :return: list - Список URL, извлеченных из столбца 'Ссылки'.
    """
    df = pd.read_excel(filename)
    urls = df['Ссылки'].tolist()

    return urls


def make_request(url):
    """
    Выполняет HTTP-запрос к указанному URL.

    :param url: str - URL для выполнения запроса.
    :return: requests.Response или False - Объект ответа, если статус код 200,
                                           иначе False.
    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    return False


def find_info(response):
    """
    Извлекает информацию о продукте из HTML-страницы.

    :param response: requests.Response - Объект ответа, полученный из запроса.
    :return: list - Список, содержащий URL, название, производителя, тару,
                    наличие и цену продукта. Если страница не существует,
                    возвращается список с пометкой 'Bad link'.
    """
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup.find('div', {'class': 'row g-2 g-md-3 ds-module ds-category-products'}):
        return [response.url, 'Bad link', '', '', '', '']
    name = soup.find('div', {'class': 'col-12 ds-page-title pb-3'}).text.replace('\n', '')
    virobnik = soup.find('div', {
        'class': 'd-flex justify-content-between align-items-start align-iems-md-center secondary-text fsz-12'}).find(
        'span').text.replace('\n', '').replace('Виробник:', '')
    price = soup.find('div', {'class': 'ds-price-new fsz-24 fw-700 dark-text'}).text
    availability = 'в наявності' if soup.find('button', {'id': 'button-cart'}) else 'немає'
    lst = soup.find_all('div', {'class': 'ds-product-attributes-item d-flex br-2'})
    for i in lst:
        if 'Тара' in i.text:
            tara = i.find_all('span')[-1].text.replace('\n', '')
            break
    else:
        tara = 0

    return [response.url, name, virobnik, tara, availability, price]


def main():
    """
    Основная функция для запуска процесса извлечения данных.

    Считывает URL из файла, выполняет HTTP-запросы и извлекает информацию
    о продуктах, затем сохраняет результаты в CSV файл.
    """
    url_file = 'agro_urls.xlsx'
    urls = read_urls(url_file)

    result_filename = 'results.csv'
    df = pd.DataFrame(columns=['URL', 'Имя', 'Виробник', 'Тара', 'Наявність', 'Ціна'])

    for url in urls:
        req = make_request(url)
        if req:
            data = find_info(req)
            df.loc[len(df)] = data
            df.to_csv(result_filename, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()