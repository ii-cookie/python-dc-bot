from pathlib import Path

#---------------------writing extracted msg to txt---------------------------
def writing_extracted_msg(message, result):
    nested_directory_path = Path("private_data/Extracted_messages")

    nested_directory_path.mkdir(parents=True, exist_ok=True)
    print(f"Nested directories '{nested_directory_path}' created successfully.")  
    
    with open('private_data/extracted_messages/' + message.author.name + '_' + message.channel.name + '_' + str(message.channel.id) + '.txt', 'w') as f:
        for content in result.content:
                f.write(content + ' \n')

