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
        domains = fw.getDomainsjson()

        if not parameters:
            response = ''
            for domain in domains:
                user, server = fw.check_toggle_on(domain, message)
                user = str(user)
                server = str(server)
                response += domain + ': \n\tuser side: ' + user + '\tserver side: ' + server + '\n'
                
            
            type, id, response = [False, False, response]
        else:
            domain_notfound = True
            for domain in fw.getDomainsjson():
                if parameters[0] == domain:
                    type = domain
                    domain_notfound = False
            if domain_notfound and len(parameters) <= 2:
                type, id, response = [False, False, 'This social media is currently not supported, would you like to create a new conversion? \n\tuse _toggle create <keyword> <doman.old> <domain.new>. \n\texample: to convert https://x.com/ to https://vxtwitter.com/ \n\t\t<keyword> = twitter, \n\t\t<domain.old> = x.com, \n\t\t<domain.new> = vxtwitter.com']
                
            if len(parameters) == 1:
                id = message.author.id
                response = type + ' link conversion for you has been toggled '
                type += '_user'                         #type = ????_user

            if len(parameters) == 2:
                
                if parameters[1] == 'server':               #cmd = _toggle ???? server
                    id = message.guild.id
                    response = type + ' link conversion for your server has been toggled '
                    type += '_server'                   #type = ????_server
                else: 
                    await message.channel.send('r u sure u want to convert future ' + type + ' links to "' + parameters[1] + '"? [y/n]')
                    try:
                        msg = await client.wait_for("message", timeout = 10.0)
                    except asyncio.TimeoutError:
                        await message.channel.send('bro u didnt reply')
                    else:     
                        if msg.content == 'y':
                            fw.add_domain_preference(type, msg.author.id, parameters[1])
                            await message.channel.send('ok done')
                        else:
                            await message.channel.send('kk')
                    type, id = [type, False]
                    
            if len(parameters) == 4:
                if parameters[0] == 'create':
                    keyword = parameters[1]
                    old_domain = parameters[2]
                    new_domain = parameters[3]
                
            else:                                           #cmd = _toggle ???? 
                id = message.author.id
                response = type + ' link conversion for you has been toggled '
                type += '_user'                         #type = ????_user

        # type, id, response = event_handle.identify_toggle_type(message, parameters)       #function usage for identify toggle type
        
        #-----------------------------save the toggles------------------------------
        if type and id:
            response = fw.save_toggle(type, id, response)

        await message.channel.send(response)


#----------------------------------END of detecting and running commands------------------------------


#----------------------------------------auto response to messages------------------------------------
    
    #------------basic testing response------------
    if message.content == "ping":
        await message.channel.send("https://www.instagram.com/reel/DKIjia6I8_q/?igsh=eTFzNm5mMzhwa3Zn")
    
    #-----------------------------------auto detecting links and conversion-------------------------------

    response = event_handle.content_link_replace(message)
    
    if response:    
        await message.channel.send(response)




client.run(TOKEN)
