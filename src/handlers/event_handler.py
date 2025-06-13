import importlib
import discord
from pandas import ExcelFile



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
guild = discord.Guild

#extracting commands and parameters from text



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
        return 
    elif message.content.startswith('_'):
        cmd = message.content.split()[0].replace("_","")

        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]
            return parameters




def extract_messages(message, all_messages, limit):

    if limit == 0:
        return
    

    user = message.author
    class result:
        extracted_messages = []
        count = -1              #does one extra to ignore the cmd line
        def __init__(self, extracted_messages, count):
            self.extracted_messages = extracted_messages
            self.count = count
    
    for msg in all_messages:
        
        if msg.author == user:
            result.extracted_messages.append(msg)
            result.count += 1

        if limit == -1:     #skip the limit checking
            continue

        if result.count > limit:   
            break

    
    result.extracted_messages.reverse()
    #removing the cmd message
    result.extracted_messages.pop()
    result.count -=1

    return result


