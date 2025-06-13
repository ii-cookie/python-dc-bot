#bro i have no idea how to auto make folder so i give up, put the empty folders in urself
        # currentPath = os.getcwd()
        # nameofFolder = "extracted_messages"

        # if not os.path.exists(currentPath + '/private_data' + nameofFolder):
        #     os.makedirs('/private_data' + nameofFolder)




def writing(message, result):
    with open('private_data/extracted_messages/' + message.author.name + '_' + message.channel.name + '_' + str(message.channel.id) + '.txt', 'w') as f:
        # for content in result.content:
        #         f.write(content + ' \n')
        for msg in result.extracted_messages:
                f.write(msg.content + ' \n')
