from pathlib import Path
import os
import json
import re

#---------------------writing extracted msg to txt---------------------------
def writing_extracted_msg(message, result):
    nested_directory_path = Path("private_data/Extracted_messages")

    nested_directory_path.mkdir(parents=True, exist_ok=True)
    print(f"Nested directories '{nested_directory_path}' created successfully.")  
    
    with open('private_data/extracted_messages/' + message.author.name + '_' + message.channel.name + '_' + str(message.channel.id) + '.txt', 'w') as f:
        for content in result.content:
                f.write(content + ' \n')
                
#-----------------------------START of get xxx files()----------------------------
#------------------------get files helper func---------------
def getJSONFILE(path):
    datafile = path
    try:
        if datafile.is_file():    
            with open(datafile) as json_file:
                data = json.load(json_file)
        else:
            data = {}
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}. Initializing with empty data.")
        data = {}
    return data

#-----------------------get data of toggles--------------------
def getTogglesjson():
    path = Path('private_data/toggles.json')
    return getJSONFILE(path)

#----------------------get data of domains----------------------
def getDomainsjson():
    path = Path('private_data/toggles.json')
    return getJSONFILE(path)
    
    
#------------------------------END of get xxx files()-------------------------------


#---------------------a function that saves and deletes from file on toggles--------------------
def save_toggle(key, id, response):

    id = str(id)
    
    datafile = Path('private_data/toggles.json')
    all_toggle_data = getTogglesjson()
        
    status = False
    
    with open(datafile, 'w') as json_file:
        if key in all_toggle_data:
            #case 1: key exist, id exist
            if id in all_toggle_data[key]:
                all_toggle_data[key].remove(id)
                status = response + 'off'
            #case 2: key exist, id dont exist
            else:
                all_toggle_data[key].append(id)
                status = response + "on"
        #case 3: key dont exist -> id also dont exist
        else:
            all_toggle_data[key] = [id]
            status = response + "on"
        json.dump(all_toggle_data, json_file, indent=4)
        return status
    
    
#------------------------------------check toggle-------------------------------------------
def check_toggle_on(type, message):
    

    user_key = type + '_' + 'user'
    server_key = type + '_' + 'server'
    
    all_toggle_data = getTogglesjson()
        
    if not user_key in all_toggle_data:
        user = False
    elif not str(message.author.id) in all_toggle_data[user_key]:
        user = False
    else:
        user = True
    
    if not server_key in all_toggle_data:
        server = False
    elif not str(message.guild.id) in all_toggle_data[server_key]:
        server = False
    else: server = True
    
    return user, server

