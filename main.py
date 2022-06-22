# Imports.
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import keyboard

class Driver():

    def __init__(self):
        self.in_chat = False
        self.users = {}
        self.i = 1

    # Open chrome
    def open_chrome(self):
        # Open Chrome
        main_directory = os.path.join(os.sys.path[0])
        subprocess.Popen([
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + main_directory + "/chrome_profile",], shell=True,)
        print('chrome openned with sucess.')

    # Connect to selenium
    def connect_chrome(self):
        # Connect selenium to chrome
        self.options = Options()
        self.options.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(
                executable_path="chromedriver.exe", options=self.options)
        print('connected with sucess.')

    # In chat, check if have new messages.
    def check_new_msgs(self):
        c = 0
        new_msgs = 0
        self.users = {}
        self.elements = self.driver.find_elements_by_class_name('_ab8w')
        try:
            for element in self.elements:
                if element.get_attribute('aria-label') == 'Não lida':
                    new_msgs += 1
                    self.users[self.elements[c-4].text] = element
                c += 1
        except Exception:
            return print('execute error in check_new_msgs()')
        if new_msgs > 0:
            print(new_msgs, 'user(s) message(s).')
            return True
        else:
            dots = '.' * self.i
            os.system('cls')
            print(f'no new messages{dots}')
            self.i += 1
            if self.i == 4:
                self.i = 0            
                return False
    
    # Get chat with user selenium element.
    def get_chat(self, user):
        if self.users:
            chat = self.users.get(user)
            chat.click()
            print(f'in [{user}] chat.')
            self.in_chat = True
            return

        else:
            return print('are u checked new messages?')
    
    # See the last message of the chat.
    def get_last_msg(self):
        if self.in_chat:
            self.elements = self.driver.find_elements_by_class_name('_aade')
            last_msg = self.elements[-1]
            return last_msg.text
        else:
            return print('are u in chat?')

    # Find and get the correctly answer for a user question.
    # Change the answers and questions here.
    def get_answer(self, msg): 
        
        if msg == '1':
            return 'Answer for question 1'
        
        elif msg == '2':
            return 'Answer for question 2'
        
        elif msg == '3':
            return 'Answer for question 3'
        
        elif msg == '4':
            return 'Answer for question 4'

        else:
            return 'Hi! What is your question?\n1 - question 1?\n2 - question 2?\n3 - question 3?\n4- question 4'

    # Send a message when into chat
    def send_msg(self, msg):
        if self.in_chat:
            self.elements = self.driver.find_elements_by_tag_name('textarea')
            for element in self.elements:
                if 'Mensagem...' in f"{element.get_attribute('placeholder')}":
                    element.send_keys(msg)
                    self.elements = self.driver.find_elements_by_tag_name('button')
                    for element in self.elements:
                        if element.text == 'Enviar':
                            element.click()
                            print('message sent with sucess.')
                            return True
        else:
            return print('are u in chat?')
    
    # A loop with all of it, automatic bot 24/7.
    def auto_answer(self):
        print('starting auto answer...\n hold Q to exit.')
        sleep(1)
        while keyboard.is_pressed('Q') == False:
            check_msgs = self.check_new_msgs()
            if check_msgs:
                for user in self.users:
                    try:
                        self.get_chat(user)
                        sleep(0.5)
                        msg = self.get_last_msg()
                        answer = self.get_answer(msg)
                        self.send_msg(answer)
                        sleep(0.5)
                    except Exception:
                        print('execute error in auto_answer()')
                        break
                self.driver.back()
                self.in_chat = False
                self.i = 0
                print('============== refreshing ==============')
                sleep(2)
            sleep(1)

bot = Driver()

