
def default_action_fn(*args, **kwargs):
    print("This action is not yet implemented.")

class MenuOption:
    
    def __init__(self, label, action_fn=None, **kwargs):
        
        self.label = label
        self.key = '0'
        
        if action_fn is None:
            self.action_fn = default_action_fn
        else:
            self.action_fn = action_fn
            
    def set_input_key(self, key):
        self.key = key
            
    def action(self, *args, **kwargs):
        return self.action_fn()
        
class Menu:
    
    def __init__(self, menu_name, input_prompt="Select an option: "):
        
        self.menu_name = menu_name
        self.input_prompt = input_prompt
        self.menu_option_map = {}
        self.menu_options = []
        
    def add_menu_option(self, menu_option):
        
        self.menu_options.append(menu_option)
        
        input_key = str(len(self.menu_options))
        self.menu_option_map[input_key] = menu_option
        menu_option.set_input_key(input_key)
        
    def display_menu(self):
        
        print(self.menu_name)
        print()
        
        for menu_option in self.menu_options:
            
            print(f"{menu_option.key} - {menu_option.label}")
        
        print()
        
        user_input = input(self.input_prompt)
        
        if user_input in self.menu_option_map:
            menu_option = self.menu_option_map[user_input]
            menu_option.action()
        else:
            print("Invalid selection.")