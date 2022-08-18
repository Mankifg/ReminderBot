# Reminder bot
Reminder bot is a discord bot hosted on Heroku created for keeping trak of tasks.
There are two diffrent types of tasks. There is a so called reminder which can be set for specific hour that day or implemented as countdown.
There is also a daily schedule siplayed for current day every morning, it also includes weather report. 
It allows to preset schedule for every day in advance via JSON file or for the current day using chat.
The bot will automaticly remind you half an hour in advance about tasks on schedule.

# .ENV structure
```
TOKEN=[Discord bot token]
WEATHER=[OpenWeatherMap Key]
RAPIDKEY=[Rapid api key]
DISCORD_CHANNEL=[Discord channel token]
```

1. Discord bot token - [Discord Dev Portal](https://discord.com/developers/applications)
2. OpenWeatherMap Key - [Here](https://home.openweathermap.org/users/sign_up)
3. Rapid api key - By creating account [Here](https://rapidapi.com/auth/sign-up?referral=/weatherbit/api/weather) and subscribing to [Here](https://rapidapi.com/weatherbit/api/weather)

# Commands
List of command can be accessed from typing **m!help**. It will show every command:


![Images](/assets/images/help.png)

# Invite bot to server?
Sure, just click [Here](https://discord.com/api/oauth2/authorize?client_id=1008650079390945300&permissions=224256&scope=bot)

# Deployment
Environment variables must be set in settings of your dyno.

Be sure to turn on the dyno, otherwise it's not going to work.

Timezone must be set to your location using an environment variable. Example:
```
TZ=Europe/Ljubljana
```

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# Contributing
If you find any issue or have suggestion, fell free to submit a **PR**.

