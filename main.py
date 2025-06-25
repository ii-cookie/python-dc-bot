import cmd
import discord
import pandas as pd
from dotenv import load_dotenv, dotenv_values
import os
import asyncio
import re
import src.handlers.event_handler as event_handle
import src.utils.file_writer as fw

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
guild = discord.Guild



#-----------------------------------basic checking if bot online----------------------------------
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    
#-------------------------------START of detecting and running commands--------------------------    

    #------------------------------extract commands-------------------------------
    cmd = event_handle.extract_cmd(message)
    parameters = event_handle.extract_parameters(message)



    #------------------------------testing parameters-----------------------------
    if cmd == 'say':   
        words = ' '.join(parameters)
        await message.channel.send(words)


    #--------------------------------testing cmd----------------------------------
    if cmd == 'ping':   
        await message.channel.send('pong')



    #----------------------------extract messages to txt------------------------------
    if cmd == 'extract':
        if parameters:
            limit = parameters[0]
            limit = int(limit)
        else:
            await message.channel.send('r u sure to extract all your messages in this channel? (y/n)')
            try:
                msg = await client.wait_for("message", timeout = 10.0)
            except asyncio.TimeoutError:
                await message.channel.send('bro u didnt reply')
            else:
                if msg.content == 'y':
                    limit = -1
                else:
                    limit = 0
        all_messages = [message async for message in message.channel.history(limit = None, oldest_first = False)]
        result = event_handle.extract_messages(message, all_messages, limit)
        await message.channel.send('ok i extracted like ' + str(result.count) + ' of ur messages in this channel')
        fw.writing_extracted_msg(message, result)



    #------------------------------------test cmd----------------------------------------
    if cmd == 'test':
        all_messages = [msg async for msg in message.channel.history(limit = 5, oldest_first=False)]
        
        for msg in all_messages:
            if msg == '':
                continue
            is_mention = r'<@[0-9]+>'
            partitions = re.split(is_mention, msg.content)
            mentions = msg.mentions

            i = 1
            sentence = partitions[0]
            for mention in mentions:
                sentence += mention.name + partitions[i]
                i += 1

            await message.channel.send(sentence)
        
    #-------------------------------------------------------------------------------------------------
    #-------------------------------------------toggles-----------------------------------------------
    #-------------------------------------------------------------------------------------------------
    if cmd == 'toggle':
        
        #---------------------------checking toggle type---------------------------

        filename, id, response = event_handle.identify_toggle_type(message, parameters)

        #-----------------------------save the toggles------------------------------
        response = fw.save_toggle(filename, id, response)
        id = ''
        filename = ''   #not sure if i need to clear this but just in case

        await message.channel.send(response)


#----------------------------------END of detecting and running commands------------------------------


#----------------------------------------auto response to messages------------------------------------
    
    #------------basic testing response------------
    if message.content == "ping":
        await message.channel.send("pong")
    
    #-----------------------------------auto detecting links and conversion-------------------------------

    response = event_handle.content_link_replace(message.content)
    
    if response:    
        await message.channel.send(response)





client.run(TOKEN)
