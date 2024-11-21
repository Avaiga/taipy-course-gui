from taipy.gui import Gui, Icon, navigate
import taipy.gui.builder as tgb
import pandas as pd

from chart import generate_map

import os
from taipy.gui import notify
import taipy.gui.builder as tgb
from taipy.auth import hash_taipy_password, AnyOf, Credentials, Authenticator
import taipy.enterprise.gui as tp_enterprise


os.environ["TAIPY_AUTH_HASH"] = "taipy"

username = "login"

credentials = Credentials(user_name=username, roles=[])

passwords = {
    "Florian": hash_taipy_password("mp153ap63"),
    "Alexandre": hash_taipy_password("m4a1m995"),
}

roles = {
    "Florian": ["admin", "TAIPY_ADMIN"],
    "Alexandre": ["TAIPY_READER"],
}

authenticator = Authenticator(protocol="taipy", roles=roles, passwords=passwords)

is_admin = AnyOf("admin", True, False)


def on_login(state, id, login_args):
    state.username, password = login_args["args"][:2]
    try:
        state.credentials = tp_enterprise.login(state, state.username, password)
        notify(state, "success", f"Logged in as {state.username}...")
        navigate(state, "page1", force=True)
    except Exception as e:
        notify(state, "error", f"Login failed: {e}")
        print(f"Login exception: {e}")
        navigate(state, "login", force=True)


def go_to_login(state):
    navigate(state, "login", force=True)


data = pd.read_csv("data.csv")
chart_data = (
    data.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

map_data = data.groupby("State")["Sales"].sum().reset_index()

start_date = "2015-01-01"
start_date = pd.to_datetime(start_date)
end_date = "2018-12-31"
end_date = pd.to_datetime(end_date)

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
            >= pd.to_datetime(state.start_date)
        )
        & (
            pd.to_datetime(data["Order Date"], format="%d/%m/%Y")
            <= pd.to_datetime(state.end_date)
        )
    ]
    state.data = state.data[state.data["Category"] == state.selected_category]
    state.data = state.data[state.data["Sub-Category"] == state.selected_subcategory]
    state.chart_data = (
        state.data.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    state.layout = {
        "yaxis": {"title": "Revenue (USD)"},
        "title": f"Sales by State for {state.selected_category} - {state.selected_subcategory}",
    }
    state.map_fig = generate_map(state.data)


with tgb.Page() as page_1:
    with tgb.part(class_name="container"):
        tgb.text("# Sales by **State**", mode="md")
        with tgb.expandable(title="Filters", expanded=False):
            with tgb.part(class_name="card"):
                with tgb.layout(columns="1 2 1"):
                    with tgb.part():
                        tgb.text("Filter **From**", mode="md")
                        tgb.date("{start_date}")
                        tgb.text("To")
                        tgb.date("{end_date}")
                    with tgb.part():
                        tgb.text("Filter Product **Category**", mode="md")
                        tgb.selector(
                            value="{selected_category}",
                            lov=categories,
                            on_change=change_category,
                            dropdown=True,
                        )
                        tgb.text("Filter Product **Subcategory**", mode="md")
                        tgb.selector(
                            value="{selected_subcategory}",
                            lov="{subcategories}",
                            dropdown=True,
                        )
                    with tgb.part(class_name="text-center"):
                        tgb.button(
                            "Apply",
                            class_name="plain apply_button",
                            on_action=apply_changes,
                        )
        tgb.html("br")
        with tgb.layout(columns="2 3"):
            tgb.chart(
                data="{chart_data}",
                x="State",
                y="Sales",
                type="bar",
                layout="{layout}",
            )
            tgb.chart(figure="{map_fig}")
        tgb.html("br")
        with tgb.part(render="{is_admin.get_traits(credentials)}"):
            tgb.table(data="{data}")


def menu_option_selected(state, action, info):
    page = info["args"][0]
    navigate(state, to=page)


with tgb.Page() as root_page:
    tgb.menu(
        label="Menu",
        lov=[
            ("page1", Icon("images/map.png", "Sales")),
            ("page2", Icon("images/person.png", "Account")),
        ],
        on_action=menu_option_selected,
    )

with tgb.Page() as login_page:
    tgb.login("Welcome to Taipy!")

with tgb.Page() as page_2:
    tgb.text("# Account **Management**", mode="md")
    tgb.button(
        "Logout", class_name="plain login-button", width="50px", on_action=go_to_login
    )

pages = {
    "/": root_page,
    "page1": page_1,
    "page2": page_2,
    "login": login_page,
}


Gui(pages=pages).run(title="Sales", dark_mode=False, debug=True)
