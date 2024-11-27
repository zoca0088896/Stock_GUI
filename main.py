from nicegui import ui
from pages.home import main_menu
from pages.add_stock import add_stock
from pages.group import show_group

# temporary user data
user = {"is_login": True, "password": "0000", "group_refresh": 30.0}


@ui.page(path="/", title="選股程式-主頁")
def home_page() -> None:
    if not user["is_login"]:
        # login helper fn
        def get_auth() -> None:
            password = result.value
            if password == user["password"]:
                user["is_login"] = True
                ui.navigate.to("/")
            else:
                login_fail_info.set_text("登入失敗，請確認密碼")

        # login page
        with ui.label("").classes("absolute top-1/4 inset-x-1/3 w-1/3 rounded"):
            with ui.grid().classes("bg-sky-100 shadow-sm p-10"):
                login_label = ui.label("選股網").classes("text-center text-2xl")
                result = ui.input(label="請輸入密碼",
                                  password=True)
                ui.button(text="登入",
                          on_click=get_auth)
                login_fail_info = ui.label("")

    else:
        # home page menu
        main_menu()


@ui.page(path="/add", title="選股程式-新增股票")
def add_page() -> None:
    add_stock()


@ui.page(path="/group/{group_type}/{upper_bound}/{lower_bound}/{strategy_num}", title="分組查看")
def group_page(group_type: str, upper_bound: float, lower_bound: float, strategy_num: float) -> None:
    show_group(group_type, upper_bound, lower_bound, strategy_num)
    # according user setting to refresh.
    # default is 30s
    ui.timer(user["group_refresh"], lambda: show_group.refresh(
        group_type, upper_bound, lower_bound, strategy_num))


ui.run()
