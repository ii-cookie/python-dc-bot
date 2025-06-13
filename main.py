import cmd
import discord
import pandas as pd
from dotenv import load_dotenv, dotenv_values
import os
import asyncio
import src.handlers.event_handler as event_handle
import src.utils.extracted_messages_filewriter as emf

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
    if message.author.bot:
        return

    cmd = event_handle.extract_cmd(message)
    parameters = event_handle.extract_parameters(message)
    #testing parameters
    if cmd == 'say':   
        words = ' '.join(parameters)
        await message.channel.send(words)

    #testing cmd
    if cmd == 'ping':   
        await message.channel.send('pong')

    
    if cmd == 'extract':
        if parameters[0]:
            limit = parameters[0]
            limit = int(limit)
        else:
            
            await message.channel.send('r u sure to extract all your messages in this channel? (y/n)')
            try:
                msg = await client.wait_for("message", timeout=5.0)
            except asyncio.TimeoutError:
                await message.channel.send('bro u didnt reply')
            else:
                if msg.content == 'y':
                    limit = -1
                else:
                    limit = 0

    
        # target = parameters[1]
        all_messages = [message async for message in message.channel.history()]
        result = event_handle.extract_messages(message, all_messages, limit)
        await message.channel.send('ok i extracted like ' + str(result.count) + ' of ur messages in this channel')
        emf.writing(message, result)


        
        


        

client.run(TOKEN)
