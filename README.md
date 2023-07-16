# Google Calendar Bot
Это Telegram бот, который получает данные из Google календарей посредством API. Может выдать информацию о ближайших событиях по запросу и отправляет уведомления о днях рождения.

Запущенный на сервере бот: https://t.me/mrhyde_calendar_bot

### Используемые технологии:
```
Python 3.11.4
python-telegram-bot 20.3
APScheduler 3.10.1
google-api-python-client 2.91.0
google-auth-httplib2 0.1.0
google-auth-oauthlib 1.0.0
```

### Как адаптировать код под своего бота:
- Создайте и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt 
	 ``` pip install -r requirements.txt ```
- Создайте файл .env в корне проекта
- Создайте бота с помощью [BotFather](https://t.me/BotFather) 
- Запишите токен вашего бота в файл .env в переменную TG_BOT_TOKEN
- Узнайте свой id у [userinfobot](https://t.me/userinfobot) отправив команду ```/start```
- Запишите этот id в файл .env в переменную TG_CHAT_ID
- Настройте API Google календаря согласно [инструкции](https://developers.google.com/calendar/api/quickstart/python?hl=en). В качестве метода авторизации используйте OAuth 2.0. Файл должен называться credentials.json и располагаться в папке creds.
- Измените значение переменной BIRTHDAYS_ID в файле google_calendar.py на id вашего календаря (его можно найти в настройках Google календаря)
- Запустите файл tg_bot.py
