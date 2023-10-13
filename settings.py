import os
from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

incorrect_auth_key = {'key': '1000000000000000000000'}
incorrect_email = 'hhfxhf@mail.ru'
incorrect_password = 'dxfjftdfgyrfd'

