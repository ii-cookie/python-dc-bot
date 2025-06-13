import cmd
import discord
import pandas as pd
from dotenv import load_dotenv, dotenv_values
import os
import src.handlers.event_handler as event_handle

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
guild = discord.Guild

#basic checking if bot online
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#basic ping pong checking
@client.event
async def on_message(message):


    if message.author == client.user:
        return
    elif message.content.startswith('_'):
        cmd = message.content.split()[0].replace("_","")

        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]

            #testing parameters
            if cmd == 'say':   
                words = ' '.join(parameters)
                await message.channel.send(words)

        #testing cmd
        if cmd == 'ping':   
            await message.channel.send('pong')

        

client.run(TOKEN)
