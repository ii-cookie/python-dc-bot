import importlib
import discord
from pandas import ExcelFile
import re


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
guild = discord.Guild

#extracting commands and parameters from text

is_url = r'https?://\S+|www\.\S+'
is_mention = r'<@\S+>'

def extract_cmd(message):
    if message.author == client.user:
        return 
    elif message.content.startswith('_'):
        cmd = message.content.split()[0].replace("_","")

        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]
        return cmd

def extract_parameters(message):
    if message.author == client.user:
        return []
    elif message.content.startswith('_'):
        cmd = message.content.split()[0].replace("_","")

        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]
            return parameters

def is_valid_extract(content):
    if not content.isascii():   #take only ascii characters
        return False
    
    if (re.findall(is_url, content)):   #skipping all the links
        return False
    
    if (re.findall(is_mention, content)):
        return 'there is a mention dude no way'
    
    return content


def extract_messages(message, all_messages, limit):
    
    if limit == 0:
        return
    
    user = message.author
    class result:
        extracted_messages = []
        content = []
        count = 0

    
    for msg in all_messages:
        
        content = is_valid_extract(msg.content)
        if not is_valid_extract(content):
            continue
        
        
        if msg.author == user:
            result.extracted_messages.append(message)
            result.count += 1
            result.content.append(content)



        if limit == -1:     #skip the limit checking
            continue

        if result.count > limit:   
            break

    
    result.extracted_messages.reverse()
    #removing the cmd message
    result.extracted_messages.pop()
    result.count -=1

    return result


