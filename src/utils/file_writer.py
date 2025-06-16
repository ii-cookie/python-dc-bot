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
def save_toggle(filename, id, response):

    id = str(id)
    all_save_data = []
    file = Path('private_data/' + filename + '.txt')
    if file.is_file():
        with open('private_data/' + filename + '.txt', 'r') as f:
            all_save_data = [line.rstrip() for line in f]
            print(all_save_data)
            print(id)

    with open('private_data/' + filename + '.txt', 'w') as f:
        if id in all_save_data:
            for data in all_save_data:
                if data != id:
                    f.write(data)
            return response + 'off'
        else:
            for data in all_save_data:
                f.write(data)
            f.write(id + '\n')
            return response + "on"