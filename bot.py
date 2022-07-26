import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from PIL import Image
import requests

#navigate env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

#grab bots user id
BOT_ID = client.api_call("auth.test")['user_id']


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    usr_text = event.get('text')

    if BOT_ID != user_id:
        #did user ask for a shiba?
        if usr_text == 'can i have a shiba':
            #get shiba image from shibe api
            response = requests.get("http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true")
            response = response.json()[0]
            #store shiba image
            img_data = requests.get(response).content
            with open('shiba.jpg', 'wb') as handler:
                handler.write(img_data)
            #send shiba image to slack channel
            response = client.files_upload(file='shiba.jpg',channels=channel_id)


#start bot
if __name__ == "__main__":
    app.run(debug=True)
