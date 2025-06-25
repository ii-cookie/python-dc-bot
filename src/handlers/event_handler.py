import importlib
import discord
from pandas import ExcelFile
import re


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
guild = discord.Guild


#----------------------------------detect command / parameters-------------------------------------

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
        
#------------------------------------extracting messages-------------------------------------


#------------------helper func-------------------
is_url = r'https?://\S+|www\.\S+'
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
    if not (re.search(is_mention, msg.content)):
        return msg.content
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

#-----------------actual extract---------------------

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
    result.content.reverse()
    return result


#----------------------------identifying toggle type--------------------------
def identify_toggle_type(message,parameters):
    
    
    if len(parameters) == 0:
        return False, False, 'Please enter a social media name, eg _toggle twitter'
    
    
    if parameters[0] == 'twitter' or 'x':           #cmd = _toggle twitter 
        filename = 'twitter'
        
    elif parameters[0] == 'instagram' or 'ig':      #cmd = _toggle twitter 
        filename = 'instagram'
    else:
        return False, False, 'This social media is currently not supported'
        
        
    if len(parameters) == 2:
        
        if parameters[1] == 'server':               #cmd = _toggle ???? server
            id = message.guild.id
            response = filename + ' link conversion for your server has been toggled '
            filename += '_server'                   #filename = ????_server
            
    else:                                           #cmd = _toggle ???? 
        id = message.author.id
        response = filename + ' link conversion for you has been toggled '
        filename += '_user'                         #filename = ????_user
        
    return filename, id, response


#------------------------------link convert-------------------------------
class domain:
    def __init__(self, old, new):
        self.old = old
        self.new = new

twitter = domain('x.com', 'vxtwitter.com')
domains = [twitter]

def content_link_replace(content):
    if (re.search(is_url, content)):
        content_without_links = re.split(is_url, content)
        all_links = re.findall(is_url, content)
        new_links = []

        changes = False     #keep track if theres any link converted, if yes then need send, else do nth
        for link in all_links:
            for domain in domains:
                pattern = rf"https?://{re.escape(domain.old)}\S+"   #check all patterns
                if re.search(pattern, link):        #if detected, then convert the link
                    new_link = link_convert(link, domain.old, domain.new)
                    changes = True
                    new_links.append(new_link)
                    break       #no need to check other domains cuz alr found
            
        
        #if nothing need change, then return false
        if not changes:
            return False
        
        sentence = content_without_links[0]
        i = 1
        for link in new_links:
            sentence += str(link) + content_without_links[i]
            i += 1
        return sentence
    return False

def link_convert(link, old_domain, new_domain):
    partitions = re.split('/', link)

    converted = ''

    for part in partitions:
        if part == partitions[2] and old_domain:
            converted += '//' + new_domain + '/'
            continue
        converted += part
    
    return converted
