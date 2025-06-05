from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
import plotly.graph_objects as go
from taipy.designer import Page

from chart import generate_map

data = pd.read_csv("data.csv")
chart_data = (
    data.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

map_data = data.groupby("State")["Sales"].sum().reset_index()

start_date_str = "2015-01-01"
start_date = pd.to_datetime(start_date_str)
end_date_str = "2018-12-31"
end_date = pd.to_datetime(end_date_str)

categories = list(data["Category"].unique())
selected_category = "Furniture"

selected_subcategory = "Bookcases"
subcategories = list(
    data[data["Category"] == selected_category]["Sub-Category"].unique()
)

layout = {"yaxis": {"title": "Revenue (USD)"}, "title": "Sales by State"}

map_fig = generate_map(data)


def change_category(state):
    state.subcategories = list(
        data[data["Category"] == state.selected_category]["Sub-Category"].unique()
    )
    state.selected_subcategory = state.subcategories[0]


def apply_changes(state):
    state.data = data[
        (
            pd.to_datetime(data["Order Date"], format="%d/%m/%Y")
            >= pd.to_datetime(state.start_date_str)
        )
        & (
            pd.to_datetime(data["Order Date"], format="%d/%m/%Y")
            <= pd.to_datetime(state.end_date_str)
        )
    ]
    state.data = state.data[state.data["Category"] == state.selected_category]
    state.data = state.data[state.data["Sub-Category"] == state.selected_subcategory]
    # state.chart_data = (
    #     state.data.groupby("State")["Sales"]
    #     .sum()
    #     .sort_values(ascending=False)
    #     .head(10)
    #     .reset_index()
    # )
    # state.layout = {
    #     "yaxis": {"title": "Revenue (USD)"},
    #     "title": f"Sales by State for {state.selected_category} - {state.selected_subcategory}",
    # }
    state.map_fig = generate_map(state.data)


def on_change(state, var, val): ...


page = Page("new_charts.xprjson")

Gui(page=page).run(title="Sales", design=True, port=2542)
