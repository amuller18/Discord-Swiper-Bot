from selenium import webdriver
from swiper import ripper
from datetime import datetime
import time

username = '4014104212'
password = 'poopy123'
backup_code = '88888888'
input_server_name = 'Dokyo'
input_channel_name = 'general'
output_api_key = 'https://discord.com/api/webhooks/1218388508444594196/WBullps25ZmhDFjZ7QnUbW_loimTmsjq7K2QmGqCdmlHEGZ_tzv0KpU-_C2J5C9WhRzS'
c = 3 #channel name prefix character count
run = True

driver = webdriver.Chrome()
s = ripper(driver, output_api_key, backup_code)
s.login(username, password)
s.go_to_channel(input_server_name, input_channel_name, c)
s.start_ripping()
while run == True:
    current_time = datetime.now()
    current_minutes = current_time.minute
    if current_minutes % 5 == 0:
        print(f'Started at {current_time}')
        s.login(username,password)
        s.go_to_channel(input_server_name, input_channel_name, c)
        s.start_ripping()
        time.sleep(500)
    else:
        print(f'didnt start at {current_time}')
        time.sleep(10)