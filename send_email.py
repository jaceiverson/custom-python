import smtplib
from custom_python.make_config import read

from email.mime.text import MIMEText

def send(subject,
         message,
         recipients,
         sender,
         config_file = None):
    
    email_txt = MIMEText('\n'.join(message))
    email_txt['Subject'] = subject
    email_txt['From'] = sender
    email_txt['To'] = '\n'.join(recipients)


    #THIS pwd is from Google app passwords
    #you  need this password from your account
    #read it in through the config file
    if config_file == None:
        config_file = read()

    email = config_file['email']['email']
    pwd = config_file['email']['pwd']

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(email,pwd)
    server.sendmail('testing@terakeet.com',recipients,email_txt.as_string())
    server.close()

if __name__ == '__main__':
    '''
    send('GBQ',['to be done'],['iverson.jace@gmail.com'],sender = 'me jace')
    '''
    pass