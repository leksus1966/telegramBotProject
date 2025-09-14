import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters,
    CallbackQueryHandler
)
from .weather import fetch_weather, fetch_forecast, parse_weather, parse_forecast

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 8443))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CITIES = ["Kyiv", "Lviv", "Khmelnytskyi", "Rivne", "Ternopil"]

HELP_TEXT = (
    "I'm Weather Bot.\n"
    "I have this commands:\n"
    "/start — greeting\n"
    "/help — show this message\n"
    "/weather <city> — current weather\n"
    "/forecast <city> — forecast for 5 intervals (~15hours)\n"
    "You can select a city using the buttons or simply enter it."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(city, callback_data=f"city:{city}")] for city in CITIES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hello! ' + HELP_TEXT, reply_markup=reply_markup)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def weather_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Print the city: /weather Lviv')
        return
    await send_weather_for_city(update, ' '.join(context.args))


async def forecast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Print the city: /forecast Lviv')
        return
    await send_forecast_for_city(update, ' '.join(context.args))


async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_weather_for_city(update, update.message.text.strip())


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("city:"):
        city = data.split(":", 1)[1]
        await send_weather_for_city(update, city, edit=True)


async def send_weather_for_city(update: Update, city: str, edit=False):
    target = update.message if hasattr(update, 'message') and update.message else update.callback_query.message
    msg = await target.reply_text(f'Find weather for : {city}...')
    try:
        res = await fetch_weather(city)
    except Exception:
        logger.exception('Error fetching weather')
        await msg.edit_text('Server error.')
        return

    if 'error' in res:
        await msg.edit_text(f'Error: {res}')
        return

    weather = parse_weather(res)
    text = format_weather_text(weather)
    await msg.edit_text(text, disable_web_page_preview=True)


async def send_forecast_for_city(update: Update, city: str):
    msg = await update.message.reply_text(f'Forecast for: {city}...')
    res = await fetch_forecast(city)
    if 'error' in res:
        await msg.edit_text(f'Error: {res}')
        return
    forecast = parse_forecast(res)
    text = format_forecast_text(city, forecast)
    await msg.edit_text(text, disable_web_page_preview=True)


def format_weather_text(w: dict) -> str:
    icon_url = f"https://openweathermap.org/img/wn/{w.get('icon')}@2x.png"
    lines = [f"Weather in {w.get('city')}, {w.get('country')} ☁️",
             f"Temperature: {w.get('temp')}°C (feels like {w.get('feels_like')}°C)",
             f"Min/Max: {w.get('temp_min')}°C / {w.get('temp_max')}°C",
             f"Humidity: {w.get('humidity')}%  Pressure: {w.get('pressure')} hPa", f"Wind: {w.get('wind_speed')} m/s",
             icon_url]
    return '\n'.join(lines)


def format_forecast_text(city: str, forecast: list) -> str:
    lines = [f"Weather for {city}:"]
    for f in forecast:
        icon_url = f"https://openweathermap.org/img/wn/{f.get('icon')}@2x.png"
        lines.append(f"{f['dt_txt']}: {f['description']} {f['temp']}°C {icon_url}")
    return '\n'.join(lines)


def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError('TELEGRAM_TOKEN is not set')

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_cmd))
    app.add_handler(CommandHandler('weather', weather_cmd))
    app.add_handler(CommandHandler('forecast', forecast_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    app.add_handler(CallbackQueryHandler(button))

    if WEBHOOK_URL:
        logger.info("Starting webhook mode")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TELEGRAM_TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}",
        )
    else:
        logger.info("Starting polling mode")
        app.run_polling()


if __name__ == '__main__':
    main()