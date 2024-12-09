from nicegui import ui
import json


class UserSetting:
    def __init__(self) -> None:
        with open("user.json", "r") as f:
            self.user_setting = json.load(f)
            # open and close strategy range state
            self.upper_bound_a, self.set_upper_a = ui.state(
                self.user_setting[1]["group_a"]["upper"])
            self.lower_bound_a, self.set_lower_a = ui.state(
                self.user_setting[1]["group_a"]["lower"])
            self.group_strategy_a, self.set_group_strategy_a = ui.state(
                self.user_setting[1]["group_a"]["strategy"])

            self.upper_bound_b, self.set_upper_b = ui.state(
                self.user_setting[1]["group_b"]["upper"])
            self.lower_bound_b, self.set_lower_b = ui.state(
                self.user_setting[1]["group_b"]["lower"])
            self.group_strategy_b, self.set_group_strategy_b = ui.state(
                self.user_setting[1]["group_b"]["strategy"])

            self.upper_bound_c, self.set_upper_c = ui.state(
                self.user_setting[1]["group_c"]["upper"])
            self.lower_bound_c, self.set_lower_c = ui.state(
                self.user_setting[1]["group_c"]["lower"])
            self.group_strategy_c, self.set_group_strategy_c = ui.state(
                self.user_setting[1]["group_c"]["strategy"])

    def set_new_bound_a(self, new_upper, new_lower, new_group_strategy) -> None:
        self.set_upper_a(new_upper)
        self.set_lower_a(new_lower)
        self.set_group_strategy_a(new_group_strategy)
        with open("user.json", "r") as f:
            self.user_setting = json.load(f)
        with open("user.json", "w") as f:
            self.user_setting[1]["group_a"]["upper"] = new_upper
            self.user_setting[1]["group_a"]["lower"] = new_lower
            self.user_setting[1]["group_a"]["strategy"] = new_group_strategy
            json.dump(self.user_setting, f, indent=4)

    def set_new_bound_b(self, new_upper, new_lower, new_group_strategy) -> None:
        self.set_upper_b(new_upper)
        self.set_lower_b(new_lower)
        self.set_group_strategy_b(new_group_strategy)
        with open("user.json", "r") as f:
            self.user_setting = json.load(f)
        with open("user.json", "w") as f:
            self.user_setting[1]["group_b"]["upper"] = new_upper
            self.user_setting[1]["group_b"]["lower"] = new_lower
            self.user_setting[1]["group_b"]["strategy"] = new_group_strategy
            json.dump(self.user_setting, f, indent=4)

    def set_new_bound_c(self, new_upper, new_lower, new_group_strategy) -> None:
        self.set_upper_c(new_upper)
        self.set_lower_c(new_lower)
        self.set_group_strategy_c(new_group_strategy)
        with open("user.json", "r") as f:
            self.user_setting = json.load(f)
        with open("user.json", "w") as f:
            self.user_setting[1]["group_c"]["upper"] = new_upper
            self.user_setting[1]["group_c"]["lower"] = new_lower
            self.user_setting[1]["group_c"]["strategy"] = new_group_strategy
            json.dump(self.user_setting, f, indent=4)
