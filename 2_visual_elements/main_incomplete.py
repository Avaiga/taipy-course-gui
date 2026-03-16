from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd

data = pd.read_csv("data.csv")
chart_data = data.groupby("State")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()

categories = list(data["Category"].unique())
selected_category = "Furniture"

layout = {"yaxis": {"title": "Revenue (USD)"}, "title": "Sales by State"}


def change_category(state):
    # TODO: Update the chart data based on the selected category
    ...


with tgb.Page() as page:
    # TODO: A selector to select the category
    # TODO: A chart to visualize the data: x="State", y="Sales", type="bar", layout=layout
    # TODO: A table
    ...

Gui(page=page).run(title="Sales", dark_mode=False)
