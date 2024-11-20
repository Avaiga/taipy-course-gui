from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd

data = pd.read_csv("data.csv")
chart_data = (
    data.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

categories = list(data["Category"].unique())
selected_category = "Furniture"

layout = {"yaxis": {"title": "Revenue (USD)"}, "title": "Sales by State"}


def change_category(state):
    state.data = data[data["Category"] == state.selected_category]
    state.chart_data = (
        state.data.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    state.layout = {
        "yaxis": {"title": "Revenue (USD)"},
        "title": f"Sales by State for {state.selected_category}",
    }


with tgb.Page() as page:
    tgb.selector(value="{selected_category}", lov=categories, on_change=change_category)
    tgb.chart(
        data="{chart_data}",
        x="State",
        y="Sales",
        type="bar",
        layout="{layout}",
    )
    tgb.html("br")
    tgb.table(data="{data}")

Gui(page=page).run(title="Sales", dark_mode=False)
