from nicegui import ui
import json


class DarkMode:
    def __init__(self) -> None:
        self.dark_boolean = None
        self.load()

    def set_dark_mode(self, dark_mode: bool) -> None:
        ...

    def load(self) -> bool:
        with open('user.json', 'r') as f:
            user = json.load(f)
        self.dark_boolean = user[0]["dark"]

    def save(self) -> None:
        with open('user.json', 'r') as f:
            user = json.load(f)
        user[0]["dark"] = self.dark_boolean
        with open('user.json', 'w') as f:
            json.dump(user, f, indent=4)
        self.load()

    def show_switch(self):
        dark = ui.dark_mode(self.dark_boolean)

        def handle_switch():
            self.dark_boolean = not self.dark_boolean
            self.save()

        ui.switch('◐').bind_value(dark).classes(
            "fixed right-1 bottom-5")
        dark.on_value_change(handle_switch)
