import imaplib
import os
import email
import quopri
import re
import json
# from datetime import datetime, timedelta, date
from settings import get_credentials


# def need_to_sync():
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     fullpath = os.path.join(basedir, __file__)

#     last_modified = datetime.fromtimestamp(os.stat(fullpath).st_mtime).date()
#     time_to_sync = timedelta(days=1)
#     today = date.today()

#     result = last_modified - today
#     if result >= time_to_sync:
#         return True
#     else:
#         return False


def get_messages():
    user, password, imap_url = get_credentials()

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, password)
        mail.select('Inbox')
    except imaplib.socket.gaierror: 
        print("No internet connection")
        return False
    except (AttributeError, TypeError, OSError, imaplib.IMAP4.error):
        print('[Error occured] Invalid credentals')
        return False

    typ, data = mail.search(None, "from", "learn@python.ru")
    mail_ids = data[0]
    id_list = mail_ids.split()

    msg_body = []
    msg_received_list = []
    for num in id_list:
        status, data = mail.fetch(num, '(RFC822)')
        mail_object = data[0][1]
        msg = email.message_from_bytes(mail_object)
        subject = quopri.decodestring(msg["Subject"]).decode('utf-8', errors="ignore").replace('=?utf-8?Q?', '').replace('?', '')
        msg_received_list.append({
            "subject": subject,
            "received": msg["Date"]
        })
        decoded_string = quopri.decodestring(mail_object)
        msg_body.append(decoded_string.decode('utf-8', errors="ignore"))
    
    return msg_body, msg_received_list

def write_messages():
    bodies = get_messages()[0]
    received_list = get_messages()[1]

    with open("meta_msg.json", "w+") as f:
        f.write(json.dumps(received_list, indent=2, ensure_ascii=False))

    with open("datafile.txt", "w+") as f:
        for string in bodies:
            f.write(string)


if __name__ == "__main__":
    write_messages()