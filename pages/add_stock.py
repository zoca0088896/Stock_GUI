from nicegui import ui
from models.stock_model import model_manger
from setting.dark_mode import DarkMode

# 導入資料庫管理物件
model_manger = model_manger
# 設定全域變數
stock_df = model_manger.get_df()[["代號", "名稱", "市場", "觀察中"]]


def add_stock() -> None:
    with ui.grid(columns=3).classes("grid-flow-col w-full"):
        # 所有股票標格，可加入篩選清單
        stock_table()

        # 顯示目前選擇的股票
        info_list()

        # 添加新股票至清單和提供輸入添加刪減觀察
        new_stock_card()

    # dark mode
    dark_mode = DarkMode()
    dark_mode.show_switch()

    ui.button("返回主頁", on_click=lambda: ui.navigate.to("/"))
    

# 預計放入股票的列表提示
@ui.refreshable
def info_list() -> None:
    global stock_df
    with ui.card():
        ui.label("觀察中：").classes(
            "text-xl bg-blue w-full text-center text-slate-50")
        table = ui.table.from_pandas(stock_df[stock_df["觀察中"] == 1][["代號", "名稱", "市場"]],
                                 pagination={"rowsPerPage": 15, "sortBy": "代號"}).classes('w-full')
        
        table.add_slot('header', r'''
        <q-tr :props="props">
            <q-th auto-width> 從觀察移除 </q-th>
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
            </q-th>
        </q-tr>
        ''')
        table.add_slot('body', r'''
        <q-tr :props="props">
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
        def remove_select(msg):
            global stock_df
            model_manger.update_unselected(msg.args["row"]["代號"])
            stock_df = model_manger.get_df()[["代號", "名稱", "市場", "觀察中"]]
            stock_table.refresh()
            info_list.refresh()
        table.on("remove", lambda msg: remove_select(msg))

# 所有股票表格
@ui.refreshable
def stock_table() -> None:
    global stock_df
    with ui.card():
        ui.label("可選入股票：").classes(
            "text-xl bg-blue w-full text-center text-slate-50")
        table = ui.table.from_pandas(stock_df[stock_df["觀察中"] == 0][["代號", "名稱", "市場"]],
                                    pagination={"rowsPerPage": 15, "sortBy": "代號"}).classes('w-full')
        table.add_slot('header', r'''
            <q-tr :props="props">
                <q-th auto-width> 加入觀察 </q-th>
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
                
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.value }}
                </q-td>
            </q-tr>
        ''')
        def add_select(msg):
            global stock_df
            model_manger.update_selected_by_id(msg.args["row"]["代號"])
            stock_df = model_manger.get_df()[["代號", "名稱", "市場", "觀察中"]]
            stock_table.refresh()
            info_list.refresh()
        table.on("add", lambda msg: add_select(msg))


# 添加新股票組件
# 和用代號添加股票到觀察清單或移除
@ui.refreshable
def new_stock_card() -> None:
    with ui.card():
        def add_new_stock(stock_id, name, stock_type, selected):
            global stock_df
            model_manger.add_stock(stock_id, name, stock_type, selected)
            stock_df = model_manger.get_df()[["代號", "名稱", "市場", "觀察中"]]
            stock_table.refresh()
            info_list.refresh()

        ui.label("添加新上市櫃的股票").classes(
            "text-xl bg-blue w-full text-center text-slate-50")
        input_code = ui.input("輸入股票代號")
        input_name = ui.input("輸入股票名稱")
        input_type = ui.radio({"市": "上市", "櫃": "上櫃"}, value="市")
        input_selected = ui.radio({0: "不列入觀察清單", 1: "列入"}, value=1)
        ui.button("新增股票", on_click=lambda: add_new_stock(stock_id=input_code.value,
                                                         name=input_name.value,
                                                         stock_type=input_type.value,
                                                         selected=input_selected.value))

        # 代號添加
        def add_code(stock_code):
            global stock_df
            model_manger.update_selected_by_id(stock_code)
            stock_df = model_manger.get_df()[["代號", "名稱", "市場", "觀察中"]]
            stock_table.refresh()
            info_list.refresh()

        def unselected(stock_code):
            global stock_df
            model_manger.update_unselected(stock_code)
            stock_df = model_manger.get_df()[["代號", "名稱", "市場", "觀察中"]]
            stock_table.refresh()
            info_list.refresh()

        ui.label("輸入代號添加至觀察名單").classes(
            "text-xl bg-blue w-full text-center text-slate-50")
        selected_code = ui.input("輸入股票代號")
        ui.button("納入觀察", on_click=lambda: add_code(selected_code.value))
        ui.button("從觀察名單去除", on_click=lambda: unselected(selected_code.value))
   