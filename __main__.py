
import getpass, json, os
import requests

import boto3

from dotenv import load_dotenv

from snowfall.auth import AuthService
from snowfall.menu import Menu, MenuOption

AuthSvc = AuthService()

load_dotenv()  # take environment variables from .env.

CONFIG_BUCKET_NAME = os.getenv('CONFIG_BUCKET_NAME')
LOGIN_LAMBDA_URL = os.getenv('LOGIN_LAMBDA_URL')
SIGN_UP_LAMBDA_URL = os.getenv('SIGN_UP_LAMBDA_URL')

def register_action():
    
    print("Please sign up")
    
    username = input('Username: ')
    password = getpass.getpass()
    
    resp = requests.post(SIGN_UP_LAMBDA_URL, json={
        'username': username,
        'password': password
    })
    
    print(resp.text)
    
    
def login_action():
    
    print("Please Login")

    username = input('Username: ')
    password = getpass.getpass()
    
    resp = requests.post(LOGIN_LAMBDA_URL, json={
        'username': username,
        'password': password
    })
    
    resp_json = resp.json()
    
    AuthSvc.authenticate_with_credentials(resp_json['credentials'])
    
    

AUTH_MENU = [
    [1, 'Register', register_action],
    [2, 'Login', login_action]
]

def display_menu(menu_title, menu_options, input_prompt='Select an option: '):
    
    actions = {}
    
    print(menu_title)
    print()
    
    for option in menu_options:
        
        select_key = option[0]
        display_name = option[1]
        action_function = option[2]
        
        actions[str(select_key)] = action_function
        
        print(f"{select_key} - {display_name}")
        
    print()
    
    user_input = input(input_prompt)
    
    if user_input in actions:
        action_function = actions[user_input]
        action_function()
    else:
        print("Please make a valid selection.")
    
# display_menu('Auth Menu', AUTH_MENU)
    
register_option = MenuOption('Register', action_fn=register_action)
login_option = MenuOption('Login', action_fn=login_action)

auth_menu = Menu('Auth Menu')
auth_menu.add_menu_option(register_option)
auth_menu.add_menu_option(login_option)

while AuthSvc.is_authenticated() == False:
    auth_menu.display_menu()
    
## list options: text-quest, text-civ, text-tcg

s3_client = boto3.client('s3')
main_menu_config_json_resp = s3_client.get_object(
    Bucket=CONFIG_BUCKET_NAME,
    Key='mainMenuConfig.json'
)

MAIN_MENU_CONFIG = json.loads(main_menu_config_json_resp['Body'].read())

'''
MAIN_MENU_CONFIG = {
    'title': 'Select Application',
    'apps': [
        {
            'name': 'TextQuest',
            'active': True
        },
        {
            'name': 'TextCiv',
            'active': False
        },
        {
            'name': 'TextTCG',
            'active': False
        }
    ]
}
'''

main_menu = Menu(MAIN_MENU_CONFIG['title'])

for app in MAIN_MENU_CONFIG['apps']:
    
    def make_fn(app):
        def f(*args, **kwargs):
            if app['active']:
                print(f'You are playing {app["name"]}.')
            else:
                print('This application is not yet ready.')
        return f
        
    menu_item_name = app['name']
    if not app['active']:
        menu_item_name += ' [COMING SOON]'
            
    main_menu.add_menu_option(
        MenuOption(menu_item_name, action_fn=make_fn(app))
    )

main_menu.display_menu()