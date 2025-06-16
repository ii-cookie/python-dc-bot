from pathlib import Path

#---------------------writing extracted msg to txt---------------------------
def writing_extracted_msg(message, result):
    nested_directory_path = Path("private_data/Extracted_messages")

    nested_directory_path.mkdir(parents=True, exist_ok=True)
    print(f"Nested directories '{nested_directory_path}' created successfully.")  
    
    with open('private_data/extracted_messages/' + message.author.name + '_' + message.channel.name + '_' + str(message.channel.id) + '.txt', 'w') as f:
        for content in result.content:
                f.write(content + ' \n')


#---------------------a function that saves and deletes from file on toggles--------------------
def save_toggle(id, filename):
    directory_path = Path("private_data")
    # Create the directory
    try:
        directory_path.mkdir()
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    id = str(id)

    with open('private_data/' + filename + '.txt', 'w+') as f:
        all_save_data = f.readlines()
        if id in all_save_data:
            for data in all_save_data:
                if data.strip("\n") != id:
                    f.write(data)
            return filename + " is now toggled off"
        else:
            for data in all_save_data:
                f.write(data)
            f.write(id + '\n')
            return filename + " is now toggled on"