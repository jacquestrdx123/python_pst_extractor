import pypff
import sys
import pprint
import os
import re
import json


def get_sub_folders(folder, folder_id, message_id):
    number_of_items = folder.get_number_of_sub_messages()
    for y in range(number_of_items):
        sub_message = folder.get_sub_message(y);
        sender_name = sub_message.get_sender_name()
        headers = sub_message.get_transport_headers()
        subject = sub_message.get_subject()
        created_at = sub_message.get_creation_time()
        delivered_at = sub_message.get_delivery_time()
        attachment_count = sub_message.get_number_of_attachments()
        body = sub_message.get_html_body()
        if body:
            body_length = len(str(body))
            body = body.replace("\n", "<br>").replace("\r", "<br>")
        else:
            body = sub_message.get_plain_text_body()
            body_length = len(str(body))
            body = body.replace("\n", "<br>").replace("\r", "<br>")
        if body_length <= 0:
            body = sub_message.get_plain_text_body()
            body = body.replace("\n", "<br>").replace("\r", "<br>")


        folder_name = folder.get_name()
        message_id += 1
        sender_regex = r"From: \"(.+?)\" <(.+?)>"
        receiver_regex = r"To: \"(.+?)\" <(.+?)>"
        header_length = 0
        if headers:
            header_length = len(str(headers))
        if header_length > 0:
            sender_match = re.search(sender_regex, headers)
            receiver_match = re.search(receiver_regex, headers)
        else:
            sender_match = False
            receiver_match = False
        if sender_match:
            sender_name = sender_match.group(1)
            sender_email = sender_match.group(2)
        else:
            sender_name = "Unknown"
            sender_email = "Unknown"
        if receiver_match:
            receiver_name = receiver_match.group(1)
            receiver_email = receiver_match.group(2)
        else:
            receiver_name = "Unknown"
            receiver_email = "Unknown"
        attachments = []
        if attachment_count > 0:
            for z in range(attachment_count):
                attachment = sub_message.get_attachment(z)
                attachment_name = attachment.get_name()
                attachment_data = attachment.read_buffer(attachment.get_size())
                directory = '/home/jacques/python_pst_extractor/testing/' + sys.argv[1]
                if not os.path.exists(directory):
                    os.makedirs(directory)
                directory = '/home/jacques/python_pst_extractor/testing/' + sys.argv[1] + '/' + str(message_id)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                destination_path = str(directory) + '/' + str(attachment_name)
                with open(destination_path, 'wb') as file:
                    file.write(attachment_data)
                attachment_data_arr = {
                    "file_name": str(attachment_name),
                    "file_path": str(directory),
                    "message_id": str(message_id)
                }
                attachments.append(attachment_data_arr)
        message_data = {
            "pst_name": str(sys.argv[1]),
            "folder_id": str(folder_id),
            "message_id": str(message_id),
            "body": str(body),
            "folder_name": str(folder_name),
            "sender_name": str(sender_name),
            "sender_email": str(sender_email),
            "receiver_name": str(receiver_name),
            "receiver_email": str(receiver_email),
            "headers": str(headers),
            "subject": str(subject),
            "creation_date": str(created_at),
            "delivery_date": str(delivered_at),
            "attachment_count": str(attachment_count),
            "attachment_data": attachments
        }

        data.append(message_data)

    sub_folder_count = folder.get_number_of_sub_folders()
    for x in range(sub_folder_count):
        folder_id += 1
        sub_folder = folder.get_sub_folder(x);
        get_sub_folders(sub_folder, folder_id, message_id)


pst_file_path = str(sys.argv[1])
data = []
message_id = 0
folder_id = 0
try:
    # Open the PST file
    pst_file = pypff.file()
    pst_file.open(pst_file_path)

    # Access the root folder
    root_folder = pst_file.get_root_folder()
    file_size = pst_file.get_size()
    # print("File Size: " + str(file_size))
    root_folder_name = root_folder.get_name();
    # print("File Name: " + str(root_folder_name))

    get_sub_folders(root_folder, folder_id, message_id)

    pst_file.close()

    json_data = json.dumps(data)

    print(json_data)

except pypff.Error as e:
    print("Error:", str(e))


