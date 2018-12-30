import gmail
import pandas as pd

def send_gmail(message):
    email_info = pd.read_csv('email.csv', index_col=0)
    username = email_info.loc['username','value']
    password = email_info.loc['password','value']
    destination_email = email_info.loc['send_to','value']
    gm = gmail.GMail(username, password)
    gm.connect()
    msg = gmail.Message('Craigslist Email Notification',to=destination_email,text=message)
    gm.send(msg)

