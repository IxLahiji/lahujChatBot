import discord
import discord.utils
import asyncio
import os.path
import re
import markovify
import random
import datetime
from chatBot.settings import JSONSettings


prog_path = os.path.dirname(os.path.abspath(__file__))

default_settings = {"Discord token": "",
                    "Source channel": "",
                    "Target channel": "",
                    "Response frequency (%)": "25"
                    }

#Load information
settings = JSONSettings(prog_path, default_settings)

#Create new discord client
client = discord.Client()

last_recieved = datetime.datetime.now()

def remove_emojii(text):
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  #emoticons
            u"\U0001F300-\U0001F5FF"  #symbols & pictographs
            u"\U0001F680-\U0001F6FF"  #transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  #flags (iOS)
            u"\U00002702-\U000027B0"  #dingbats
            u"\U000024C2-\U0001F251"  #enclosed characters
            u"\U0001F681-\U0001F6C5"  #additional transport
            u"\U0001F30D-\U0001F567"  #additional symbols
            u"\U0001F600-\U0001F636"  #additional emoticons
            "]+", flags=re.UNICODE)

        return emoji_pattern.sub(r'', text)


def response_roll():
    x = random.randint(0,100)
    return (x <= int(settings.get_setting('Response frequency (%)')))
        
        
def safe_print(text):
    print (remove_emojii(text))
        

def find_channel(target_channel_name):
    channel = discord.utils.get(client.get_all_channels(), name=target_channel_name)
    return channel


async def retrieve_source_text():
    target_channel = find_channel(settings.get_setting('Source channel'))
    text = ""
    async for message in client.logs_from(target_channel, limit=5000):
            text += message.content + "\n"
    return text


async def generate_sentence ():
    source_text = await retrieve_source_text()
    text_model = markovify.NewlineText(source_text)
    
    new_sentence = None
    while not new_sentence:
        new_sentence = text_model.make_sentence()
    
    return new_sentence


    
@client.event
async def on_message(message):
    global last_recieved
    target_channel_name = settings.get_setting('Target channel')
    if (response_roll()):
        if ((message.channel.name == target_channel_name) and (message.author.id != client.user.id)):
            last_recieved = datetime.datetime.now()
            start_last_recieved = last_recieved
            
            sentence = await generate_sentence()
            if (start_last_recieved == last_recieved):
                await client.send_message(find_channel(target_channel_name), sentence)
            #safe_print (await generate_sentence())


@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name + '[' + client.user.id + '].')

    
    

print("Logging in to bot...")

#Run client (connect and login) ~ Blocking (must be last) ~ This is an unabstracted version of client.run() to give more control
try:
    if (not settings.get_setting('Discord token')):
        print ("Please enter a discord bot token in 'settings.JSON' before running")
        time.sleep(3)
        sys.exit()
    else:
        client.loop.run_until_complete(client.start(settings.get_setting('Discord token')))
    
except KeyboardInterrupt:
    #Set exit flag to allow wakeup() to close properly
    exit_flag = True

    client.loop.run_until_complete(client.logout())
    pending = asyncio.Task.all_tasks()
    gathered = asyncio.gather(*pending)
    try:
        gathered.cancel()
        client.loop.run_until_complete(gathered)
        gathered.exception()
    except:
        pass
finally:
    client.loop.close()
