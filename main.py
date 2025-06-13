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


@client.event
async def on_message(message):

    cmd = event_handle.extract_cmd(message)
    parameters = event_handle.extract_parameters(message)
    #testing parameters
    if cmd == 'say':   
        words = ' '.join(parameters)
        await message.channel.send(words)

    #testing cmd
    if cmd == 'ping':   
        await message.channel.send('pong')

        

client.run(TOKEN)
