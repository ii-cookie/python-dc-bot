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



