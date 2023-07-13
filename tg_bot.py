import datetime
import os

from dotenv import load_dotenv
from pytz import timezone
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from google_calendar import BIRTHDAYS_ID, HOLIDAYS_ID, GoogleCalendar

load_dotenv()

calendar = GoogleCalendar()


async def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = [
        [KeyboardButton('Следующие 10 дней рождения')],
        [KeyboardButton('Следующие 10 праздников')],
    ]
    await context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Я - Google Calendar Bot',
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
    )


async def next_ten_birthdays(update, context):
    if update.message.chat.id != int(os.getenv('TG_CHAT_ID')):
        await update.message.reply_text('У вас недостаточно прав!')
    else:
        await update.message.reply_text(calendar.get_events_list(BIRTHDAYS_ID))


async def next_ten_holydays(update, context):
    await update.message.reply_text(
        calendar.get_events_list(HOLIDAYS_ID),
    )


async def message_handler(update, context):
    if 'Следующие 10 дней рождения' in update.message.text:
        await next_ten_birthdays(update, context)
        return
    if 'Следующие 10 праздников' in update.message.text:
        await next_ten_holydays(update, context)
        return
    await update.message.reply_text('Неизвестная команда')


async def today_events(time):
    bot = Bot(token=os.getenv('TG_BOT_TOKEN'))
    response = calendar.get_today_events()
    if response:
        await bot.send_message(
            chat_id=int(os.getenv('TG_CHAT_ID')),
            text=response,
        )


def main():
    app = Application.builder().token(os.getenv('TG_BOT_TOKEN')).build()
    app.add_handler(CommandHandler('start', wake_up))
    app.add_handler(CommandHandler('next_ten_birthdays', next_ten_birthdays))
    app.add_handler(CommandHandler('next_ten_holydays', next_ten_holydays))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.job_queue.run_daily(
        today_events,
        time=datetime.time(hour=8, tzinfo=timezone('Europe/Moscow')),
    )
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()
