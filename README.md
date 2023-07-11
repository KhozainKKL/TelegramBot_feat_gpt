
Telegram-бот по поиску информации (web-запросов) знаменитых личностей.
-   
Миллиарды веб-страниц, изображений и новостей с помощью одного вызова API. Посетить по адресу: https://usearch.com

Данный проект состоит из:
-
1. База данных SQLite с ORM <font color=red><cite>peewee</cite></font>
   - <font color=gren><small>database/common_model/models.py</small></font> - описана модель БД 
   - <font color=gren><small>database/utilites/CRUD.py</small></font> - описаны функции работы с БД (запись, вывод)
   - <font color=gren><small>database/core.py</small></font> - скомпановано подключение и создание БД (Для создания таблицы БД необходимо запустить <font color=red><small>crud</small></font>)
   

2. Взаимодействие со сторонными API сайта осуществляется через <font color=red><cite>requests</cite></font>
   - <font color=gren><small>site_API/utilites/site_api.py</small></font> - реализованы функции осуществляющие API-запросы к стороннему сайту
   - <font color=gren><small>site_API/core.py</small></font> - скомпанована работа по обращению к сторонноему сайту через API-запрос
   

3. telegram-bot реалиозован через <font color=red><cite>telebot</cite></font>
   - <font color=gren><small>telegram_API/utilites/heandler_bot.py</small></font> - сохранены текстовые шаблоны для вывода сообщений пользователю
   - <font color=gren><small>telegram_API/utilites/telegram_api.py</small></font> - основной файл работы telegram-бота
   - <font color=gren><small>telegram_API/core.py</small></font> - "вызов" telegram-бота из main.py (необходим для запуска)
   - <font color=gren><small>translator/translator.py</small></font> - переводчик текстовых сообщений
4. <font color=gren><small>main.py</small></font> - основной файл для запуск скрипта.

Для функционала telegram-бота используется:
-
<font color=gren>КНОПКИ:</font>

      1. "Поиск новостей 🔍" - Поиск информации о любой знаменитой личности
      2. "Поиск фото 🔍" - Поиск фотоматериалов о любой знаменитой личности

<font color=gren>КОМАНДЫ:</font>

      /start - приветственное окно 
      /help - окно помощи и навигации по telegram-боту
      /low - установить минимальные значения запроса (минимальное количество искомой инф.(1), дата посика: текущая)
      /high - установить маскимальные значения запроса (максимальное количество искомой инф.(10), дата посика: 2023-01-01)
      /custom - установить вручную параметры поиска
      /history - вывод истории запросов (имя - метод - запрос)








       If you don't have tesseract executable in your PATH, include the following:
      pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
      # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'













Источники:
-
Необходим предустановленный tesseract --- https://github.com/UB-Mannheim/tesseract/wiki
