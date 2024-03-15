# surpyance
Simple surveillance system with notifications

## Functions
Basically start a telegram bot in idle, when you want to start verify that someone turn the lights on, send `\start`,
the script will start a control loop when anyone turn the lights on, start to register from the webcam and every 15 seconds,
the bot, will send the video to the chat!

## How to use
- Install the required packages from the `requirements.txt`
- export an environement variable named `BOT_TOKEN` equals to the API string of Telegram
- start the bot with `python surpyance.py`
- send a `\send` message in the chat to start control the camera!
- wait (or possibly not!) some video in the bot chat
