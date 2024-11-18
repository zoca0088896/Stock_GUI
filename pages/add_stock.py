from nicegui import ui
from models.stock_model import StockModel

model_manger = StockModel("sqlite:///models/stocks.db")
stock_df = model_manger.get_df()


@ui.refreshable
def add_stock():
    select_stock, set_select = ui.state([])

    with ui.row():
        label = ui.label("select_stock")
        table = ui.table.from_pandas(stock_df,
                             pagination={"rowsPerPage": 15, "sortBy": "id"})
        table.add_slot('header', r'''
            <q-tr :props="props">
                <q-th auto-width />
                <q-th v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.label }}
                </q-th>
            </q-tr>
        ''')
        table.add_slot('body', r'''
            <q-tr :props="props">
                <q-td auto-width>
                    <q-btn size="sm" color="accent" round dense
                        @click="$parent.$emit('action', props)"
                        :icon="props.expand ? 'remove' : 'add'" />
                </q-td>
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.value }}
                </q-td>
            </q-tr>
            
        ''')
        table.on("action", lambda msg: print(msg.args["row"]))


    ui.button("返回主頁", on_click=lambda: ui.navigate.to("/"))
