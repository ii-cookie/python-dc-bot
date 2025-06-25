from pathlib import Path
import os
import json

#---------------------writing extracted msg to txt---------------------------
def writing_extracted_msg(message, result):
    nested_directory_path = Path("private_data/Extracted_messages")

    nested_directory_path.mkdir(parents=True, exist_ok=True)
    print(f"Nested directories '{nested_directory_path}' created successfully.")  
    
    with open('private_data/extracted_messages/' + message.author.name + '_' + message.channel.name + '_' + str(message.channel.id) + '.txt', 'w') as f:
        for content in result.content:
                f.write(content + ' \n')


#---------------------a function that saves and deletes from file on toggles--------------------
def save_toggle(filename, id, response):

    id = str(id)
    
    """Converting to using json instead of txt"""
    datafile = Path('private_data/toggles.json')
    
    try:
        if datafile.is_file():    
            with open(datafile) as json_file:
                all_toggle_data = json.load(json_file)
        else:
            all_toggle_data = {}
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}. Initializing with empty data.")
        all_toggle_data = {}
        
    status = False
    
    with open(datafile, 'w') as json_file:
        if filename in all_toggle_data:
            #case 1: key exist, id exist
            if id in all_toggle_data[filename]:
                all_toggle_data[filename].remove(id)
                status = response + 'off'
            #case 2: key exist, id dont exist
            else:
                all_toggle_data[filename].append(id)
                status = response + "on"
        #case 3: key dont exist -> id also dont exist
        else:
            all_toggle_data[filename] = [id]
            status = response + "on"
        json.dump(all_toggle_data, json_file, indent=4)
        return status