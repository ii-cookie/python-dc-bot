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

def is_valid_extract(msg):
    
    if msg.content == '':
        return False    

    content = msg.content
    if not msg.content.isascii():   #take only ascii characters
        return False
    
    if (re.findall(is_url, msg.content)):   #skipping all the links
        return False
    
    return True


def remove_mention(msg):
    is_mention = r'<@[0-9]+>'
    partitions = re.split(is_mention, msg.content)
    mentions = msg.mentions

    print("partitions: ")   #checking why partitions[i] is failing
    print(partitions)

    i = 1
    sentence = partitions[0]
    for mention in mentions:
        sentence += mention.name + partitions[i]
        i += 1

    print("sentence: ")     #checking why partitions[i] is failing
    print(sentence)

    return sentence



def extract_messages(message, all_messages, limit):
    
    if limit == 0:
        return
    
    user = message.author
    class result:
        extracted_messages = []
        content = []
        count = 0

    
    for msg in all_messages:
        
        if msg.author == user:

            if not is_valid_extract(msg):
                continue    

            result.extracted_messages.append(msg)
            result.count += 1
            result.content.append(remove_mention(msg))


        if limit == -1:     #skip the limit checking
            continue

        if result.count > limit:   
            break

    
    result.extracted_messages.reverse()
    #removing the cmd message
    result.extracted_messages.pop()
    result.count -= 1

    return result


