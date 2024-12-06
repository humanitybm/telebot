import telebot
import requests

API_KEY = "175ef938d8ecbc93ab5b2318392f5d95"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

from pybit.unified_trading import WebSocket
from threading import Thread
import time

# Глобальный словарь для хранения текущих данных о тикерах
crypto_data = {}

# Функция для обработки сообщений WebSocket
def handle_ticker_message(message):
    try:
        # Проверяем, есть ли ключ 'data' в сообщении
        if "data" in message:
            data = message["data"]  # Извлекаем данные
            if "symbol" in data and "lastPrice" in data:
                symbol = data["symbol"]
                crypto_data[symbol] = {
                    "last_price": data["lastPrice"],
                    "high_price_24h": data.get("highPrice24h", "N/A"),
                    "low_price_24h": data.get("lowPrice24h", "N/A"),
                    "volume_24h": data.get("volume24h", "N/A"),
                }
            else:
                print("Message missing expected keys in 'data':", data)
        else:
            print("Message missing 'data' key:", message)
    except Exception as e:
        print(f"Error in WebSocket message handling: {e}")

# Инициализация WebSocket
def start_websocket():
    ws = WebSocket(
        testnet=True,
        channel_type="spot",
    )
    symbols = ["BTCUSDT", "ETHUSDT", "TONUSDT"]  # Список отслеживаемых символов
    for symbol in symbols:
        ws.ticker_stream(
            symbol=symbol,
            callback=handle_ticker_message,
        )

# Запускаем WebSocket в отдельном потоке
ws_thread = Thread(target=start_websocket, daemon=True)
ws_thread.start()

# Обновлённая функция для получения тикера
def get_crypto_ticker_ws(symbol):
    try:
        # Проверяем наличие данных в словаре
        ticker = crypto_data.get(symbol)
        if not ticker:
            return f"❌ No data available for {symbol}. Please wait for updates. (Updates usually take a few seconds)"
        
        # Форматируем и возвращаем данные
        return (
            f"📊 {symbol} Ticker Info (Real-Time):\n"
            f"💰 Last Price: {ticker['last_price']} USDT\n"
            f"📈 24h High: {ticker['high_price_24h']} USDT\n"
            f"📉 24h Low: {ticker['low_price_24h']} USDT\n"
            f"🔄 24h Volume: {ticker['volume_24h']}"
        )
    except Exception as e:
        return f"⚠ Exception occurred: {e}"


def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "en"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        print("Response Status Code:", response.status_code)
        print("Response Data:", data)

        if response.status_code == 200:
            weather_description = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_info = (
                f"🌤 Weather in {city}:\n"
                f"🌡 Temperature: {temp}°C\n"
                f"🤔 Feels like: {feels_like}°C\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌬 Wind speed: {wind_speed} m/s\n"
                f"📋 Description: {weather_description}"
            )
            return weather_info
        else:
            return f"❌ Error: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"⚠ An error occurred: {e}"




bot = telebot.TeleBot("7740359408:AAGCt0y5y0T4Fzrk7xRe9t6LlNwkh_7V_0E")

@bot.message_handler(commands=['start'])
def start(message):
    keyboard_start = telebot.types.InlineKeyboardMarkup()
    btn1s = telebot.types.InlineKeyboardButton(text="Weather", callback_data='weather')
    btn2s = telebot.types.InlineKeyboardButton(text="Exchange Rates", callback_data='er')
    keyboard_start.add(btn1s, btn2s)

    bot.send_message(
        message.chat.id,
        text="Hello, I am a bot, made by @pythonengineer. Enjoy communication with me! Tap on the commands below.",
        reply_markup=keyboard_start,
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        keyboard_start = telebot.types.InlineKeyboardMarkup()
        btn1s = telebot.types.InlineKeyboardButton(text="Weather", callback_data='weather')
        btn2s = telebot.types.InlineKeyboardButton(text="Exchange Rates", callback_data='er')
        keyboard_start.add(btn1s, btn2s)

        keyboard_er = telebot.types.InlineKeyboardMarkup()
        btn1er = telebot.types.InlineKeyboardButton(text="BTC/USDT", callback_data='BTC')
        btn2er = telebot.types.InlineKeyboardButton(text="ETH/USDT", callback_data='ETH')
        btn3er = telebot.types.InlineKeyboardButton(text="TON/USDT", callback_data='TON')
        keyboard_er.add(btn1er, btn2er, btn3er)

        keyboard_backer = telebot.types.InlineKeyboardMarkup()
        btn1b = telebot.types.InlineKeyboardButton(text="Back", callback_data='returner')
        btn2b = telebot.types.InlineKeyboardButton(text="Main", callback_data='start')
        keyboard_backer.add(btn1b, btn2b)

        keyboard_backw = telebot.types.InlineKeyboardMarkup()
        btn1b = telebot.types.InlineKeyboardButton(text="Back", callback_data='returnw')
        btn2b = telebot.types.InlineKeyboardButton(text="Main", callback_data='start')
        keyboard_backw.add(btn1b, btn2b)

        keyboard_weather = telebot.types.InlineKeyboardMarkup()
        btn1w = telebot.types.InlineKeyboardButton(text="New York", callback_data='nyc')
        btn2w = telebot.types.InlineKeyboardButton(text="Moscow", callback_data='mow')
        btn3w = telebot.types.InlineKeyboardButton(text="Warsaw", callback_data='waw')
        keyboard_weather.add(btn1w, btn2w, btn3w)

        # Логика обработки кнопок
        if call.data == 'start':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Hello, I am a bot, made by @pythonengineer. Enjoy communication with me! Tap on the commands below.",
                reply_markup=keyboard_start,
            )
        elif call.data == 'weather':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Choose city:",
                reply_markup=keyboard_weather,
            )
        elif call.data == 'er':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Choose currency:",
                reply_markup=keyboard_er,
            )
        elif call.data == "nyc":
            weather_info = get_weather('New york')
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=weather_info,
                reply_markup=keyboard_backw
			)
        elif call.data == "mow":
            weather_info = get_weather('Moscow')
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=weather_info,
                reply_markup=keyboard_backw
			)
        elif call.data == "waw":
            weather_info = get_weather('Warsaw')
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=weather_info,
                reply_markup=keyboard_backw
			)
        if call.data == 'BTC':
            crypto_info = get_crypto_ticker_ws("BTCUSDT")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=crypto_info,
                reply_markup=keyboard_backer,
            )
        elif call.data == 'ETH':
            crypto_info = get_crypto_ticker_ws("ETHUSDT")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=crypto_info,
                reply_markup=keyboard_backer,
            )
        elif call.data == 'TON':
            crypto_info = get_crypto_ticker_ws("TONUSDT")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=crypto_info,
                reply_markup=keyboard_backer,
            )
        elif call.data == 'returner':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Choose between the following currencies:",
                reply_markup=keyboard_er,
            )
        elif call.data == 'returnw':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Choose city:",
                reply_markup=keyboard_weather,
            )
    except Exception as e:
        print(f"Exception has been thrown: {e}")

bot.infinity_polling()
