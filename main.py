from nicegui import app, ui
from pages.home import main_menu
from pages.add_stock import add_stock
from pages.group import show_group


user = {"is_login": True}


@ui.page(path="/", title="選股程式-主頁")
def home_page() -> None:
    if not user["is_login"]:
        # login helper fn
        def get_auth() -> None:
            password = result.value
            # default password: 0000
            if password == "0000":
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


@ui.page(path="/group/{group_type}/{upper_bound}/{lower_bound}")
def group_page(group_type: str, upper_bound: float, lower_bound: float) -> None:
    show_group(group_type, upper_bound, lower_bound)


ui.run()
