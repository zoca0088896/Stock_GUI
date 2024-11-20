from nicegui import ui
from models.stock_model import model_manger

# 導入資料庫管理物件(pages被導入main，從根目錄往下)
model_manger = model_manger
# 設定全域變數
stock_df = model_manger.get_df()
selected_stocks = []


def add_stock():
    global selected_stocks
    with ui.grid(columns=4).classes("grid-flow-col"):
        # 所有股票標格，可加入篩選清單
        stock_table()

        # 顯示目前選擇的股票
        info_list(selected_stocks)

        # 以代號添加到自選清單
        code_card()

        # 添加新股票至清單
        new_stock_card()

        # 將篩選股票列入已選擇

    ui.button("返回主頁", on_click=lambda: ui.navigate.to("/"))


# 預計放入股票的列表提示
@ui.refreshable
def info_list(stock_list: list):
    with ui.card():
        label = ui.label(f"預計選入股票：{stock_list}").classes("text-2xl")

        def change_data():
            global stock_df, selected_stocks
            model_manger.update_selected(selected_stocks)
            stock_df = model_manger.get_df()
            stock_table.refresh()
            selected_stocks.clear()
            info_list.refresh()
        ui.button("批量加入觀察清單", on_click=change_data)


# 所有股票表格
@ui.refreshable
def stock_table():
    global stock_df
    table = ui.table.from_pandas(stock_df,
                                 pagination={"rowsPerPage": 10, "sortBy": "id"})
    table.add_slot('header', r'''
        <q-tr :props="props">
            <q-th auto-width> 加入預選 </q-th>
            <q-th auto-width> 從預選移除 </q-th>
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
            </q-th>
        </q-tr>
    ''')
    table.add_slot('body', r'''
        <q-tr :props="props">
            <q-td auto-width>
                <q-btn size="sm" color="accent" round dense
                    @click="$parent.$emit('add', props)"
                    icon="add" />
            </q-td>
            <q-td auto-width>
                <q-btn size="sm" color="accent" round dense
                    @click="$parent.$emit('remove', props)"
                    icon="remove" />
            </q-td>
            <q-td v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.value }}
            </q-td>
        </q-tr>
    ''')

    def add_select(msg):
        global selected_stocks
        if msg.args["row"]["stock_id"] not in selected_stocks:
            selected_stocks.append(msg.args["row"]["stock_id"])
        info_list.refresh()

    def remove_select(msg):
        global selected_stocks
        if msg.args["row"]["stock_id"] in selected_stocks:
            selected_stocks.remove(msg.args["row"]["stock_id"])
        info_list.refresh()

    table.on("add", lambda msg: add_select(msg))
    table.on("remove", lambda msg: remove_select(msg))


# 用代號添加股票到預選清單組件和輸入代號清除觀察名單
@ui.refreshable
def code_card():
    with ui.card():
        def add_code(stock_code):
            global selected_stocks
            if stock_code not in selected_stocks:
                selected_stocks.append(stock_code)
            info_list.refresh()

        def unselected(stock_code):
            global stock_df
            model_manger.update_unselected(stock_code)
            stock_df = model_manger.get_df()
            stock_table.refresh()

        ui.label("輸入代號添加至觀察名單").classes("text-xl bg-blue w-full text-center text-slate-50")
        selected_code = ui.input("輸入股票代號")
        ui.button("納入預選", on_click=lambda: add_code(selected_code.value))
        ui.button("從觀察名單去除", on_click=lambda: unselected(selected_code.value))



# 添加新股票組件
@ui.refreshable
def new_stock_card():
    with ui.card():
        def add_new_stock(stock_id, name, stock_type, selected):
            global stock_df
            model_manger.add_stock(stock_id, name, stock_type, selected)
            stock_df = model_manger.get_df()
            stock_table.refresh()

        ui.label("添加新上市櫃的股票").classes("text-xl bg-blue w-full text-center text-slate-50")
        input_code = ui.input("輸入股票代號")
        input_name = ui.input("輸入股票名稱")
        input_type = ui.radio({"上市": "上市", "上櫃": "上櫃"}, value="上市")
        input_selected = ui.radio({0: "不列入觀察清單", 1: "列入"}, value=1)
        ui.button("新增股票", on_click=lambda: add_new_stock(stock_id=input_code.value,
                                                             name=input_name.value,
                                                             stock_type=input_type.value,
                                                             selected=input_selected.value))

