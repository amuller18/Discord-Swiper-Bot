from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

class ripper():
    def __init__(self, driver, api_key, backup_code):
        self.driver = driver
        self.output_api_key = api_key
        self.backup_code = backup_code
        self.last_outputted_message = ''

    def login(self, username, password):
        self.driver.get('https://discord.com/app')
        time.sleep(2)
        if self.driver.current_url == 'https://discord.com/login':
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="uid_17"]'))
                )
            finally:
                time.sleep(0.5)
                self.driver.find_element(By.ID, 'uid_17').send_keys(username)
                time.sleep(1)
                self.driver.find_element(By.ID, 'uid_19').send_keys(password)
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]').click()
                #do captcha
                time.sleep(20)
                self.twofa()
    
    def twofa(self):
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/section/div[2]/div/div/form/div[2]/div[1]/div/input'))
            )
            self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/section/div[2]/div/div/form/div[3]/button[1]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/section/div[2]/div/div/div[2]/div[2]').click()
            element.click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/section/div[2]/div/div/form/div[2]/div[1]/div/input').click()
            input = self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/section/div[2]/div/div/div[2]/div[2]').click()
            input.send_keys(self.backup_code)
            time.sleep(1)
            try:
                self.driver.find_element(By.CLASS_NAME, 'inputDefault__80165 input_d266e7').click()
            except:
                print('Incorrect backup code')
        finally:
            print('passed 2fa')
        
    def go_to_channel(self, server_name, channel_name, c):
        
        server_sidebar = self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/nav/ul/div[2]/div[3]')
        server_list = server_sidebar.find_elements(By.CLASS_NAME, 'listItem_fa7b36')
        time.sleep(2)
        for server in server_list:
            if str(server.find_element(By.CLASS_NAME, 'target__47b05').get_attribute("data-dnd-name")[
                   6:]) == server_name:
                print('Found server', server_name)
                server.find_element(By.CLASS_NAME, 'wrapper_d281dd').click()
            else:
                print('Not found server')
                time.sleep(0.3)
        time.sleep(2)
        channel_sidebar = self.driver.find_element(By.XPATH, '//*[@id="channels"]/ul')
        channel_list = channel_sidebar.find_elements(By.CLASS_NAME, 'containerDefault__3187b')
        for channel in channel_list:
            if channel.get_attribute('data-dnd-name') is not None:
                if str(channel.get_attribute('data-dnd-name')[c:]) == channel_name:
                    channel.click()

    def start_ripping(self):
        print('riping')
        time.sleep(1)
        messages = self.driver.find_element(By.CLASS_NAME, 'scrollerInner__059a5').find_elements(By.TAG_NAME, 'li')
        up_to_date = False
        while up_to_date == False:
            count = 0
            message = messages[-1-(count)].find_elements(By.CSS_SELECTOR, 'span')
            most_recent_message = [text for text in message if "Today at " not in text.text and text.text != '']
            if most_recent_message == self.last_outputted_message:
                up_to_date = False
            else:
                recontructed_text = ''
                for text in most_recent_message:
                    recontructed_text += str(text.text)
                print(recontructed_text)
                self.post_output(recontructed_text)
        print('finish')
        time.sleep(500)
    
    def post_output(self, messages):
        requests.post(self.output_api_key, {'content' : messages})
