# Welcome to Telegram Bot Weather Application

This is a simple weather application built with Python. It shows the current weather
and forecast for cities. I use python-telegram-bot and OpenWeather API.


## Pre-Requisites:

1. Install the latest version of [Python](https://www.python.org/downloads/)
   - I used the Python 3.13

2. Sign up for a free account at [openweathermap](https://openweathermap.org/), 
3. Log in to [home page](https://home.openweathermap.org/api_keys), and generate your new API key.

3. After generating your API key, copy it into the "OPENWEATHER_API_KEY" variable within the .env file using this format:
```bash
OPENWEATHER_API_KEY = 'your-api-key'
```
4. Create your new bot in the Telegram. Use chat with @BotFather.
- send `/newbot`, create the new bot name and get an API token.
5. After generating of the API token, copy it into the "TELEGRAM_TOKEN" variable within the .env file using this format:
```bash
TELEGRAM_TOKEN = 'your-api-token'
```

## How to run this project?

**Clone this project**
```
$  git clone https://github.com/leksus1966/telegramBotProject.git 
```
or
```
$  git clone git@github.com:leksus1966/telegramBotProject.git
```

**Enter the project directory**
```
$  cd telegramBotProject
```

**Activate Virtual Environment.**

For Windows
```
$  source venv/scripts/activate
```

For Linux and Mac
```
$  source .venv/bin/activate
```

**Install packages**
```
$ python3 -m pip install -r requirements.txt
```

**Now Run the App**
```
$ python -m app.bot
```

**How to start this application in the container**
 - Install Docker Desktop
 - Start Docker
```bash
docker build -t telegram-weather-bot .
docker run --env-file .env telegram-weather-bot
```

**How to start with docker-compose**
```bash
docker-compose up -d --build
```

Check logs from container
```bash
docker-compose logs -f
```

Stop the container
```bash
docker-compose stop
```

**How to start this application on Heroku**
```bash
heroku create
heroku config:set TELEGRAM_TOKEN=... OPENWEATHER_API_KEY=... WEBHOOK_URL=https://<app>.herokuapp.com
git push heroku main
```
## Features

- /weather `<city>` — current weather
- /forecast `<city>` — forecast for 5 intervals (~15h)
- Inline buttons with a choice of popular cities
- Weather icons
- Webhook mode for deployment on Heroku

## Connect with me

- Github [https://github.com/leksus1966]
- Linkedin [https://www.linkedin.com/in/oleksii-sokalo-97589393/]
