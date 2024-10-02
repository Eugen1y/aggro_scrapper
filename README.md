# Agro Scraper

Agro Scraper - это инструмент для извлечения информации о продуктах с веб-сайта agroplant.com.ua. Скрипт автоматически проходит по списку ссылок из файла `agro_urls.xlsx` и собирает данные о названии, цене, производителе, таре и наличии. На выходе создает файл `results.csv` c результатами работы 

## Установка

Следуйте этим шагам, чтобы установить и запустить проект:

1. **Клонировать репозиторий**

   ```bash
   git clone https://github.com/your-username/agro_scraper.git
   cd agro_scraper
2. **Установить виртуальное окружение**

   ```bash
   python -m venv venv
   
3. **Активировать виртуальное окружение**

   ```bash
   venv\Scripts\activate

   
4. **Установить зависимости**

   ```bash
   pip install -r requirements.txt

## Запуск скрапера
После установки зависимостей вы можете запустить скрипт, выполнив:
   ```bash
   python aggro_scrapper.py
   ```
