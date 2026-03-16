import os
from typing import Optional

import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from chart import generate_map
from taipy import Config
from taipy.auth import AnyOf, Credentials
from taipy.auth.exceptions import AuthenticatorError, InvalidCredentials
from taipy.gui import Gui, Icon, navigate, notify

os.environ["TAIPY_AUTH_HASH"] = "taipy"


passwords = {
    "Florian": tp.auth.hash_taipy_password("mp153ap63"),
    "Alexandre": tp.auth.hash_taipy_password("m4a1m995"),
}

roles = {
    "Florian": ["admin", "TAIPY_ADMIN"],
    "Alexandre": ["TAIPY_READER"],
}

Config.configure_authentication(protocol="taipy", roles=roles, passwords=passwords)

credentials: Optional[Credentials] = None
is_admin = AnyOf("admin", True, False)


def handle_logout(state):
    tp.enterprise.gui.logout(state)
    state.credentials = None
    notify(state, "error", "You have logged out.")
    navigate(state, "/", force=True)


def on_login(state, id, payload):
    username, password = payload["args"][:2]
    if username is None:  # The user canceled the login request
        return navigate(state, "/", force=True)
    state.credentials = tp.enterprise.gui.login(state, username, password)
    # Failed authentication would raise an AuthenticatorError exception, handled by main.on_exception
    notify(state, "success", f"You are now logged in as {state.credentials.user_name}.")
    navigate(state, "/", force=True)


def on_exception(state, function_name: str, exception):
    print(f"Exception in {function_name}: {exception}")
    if isinstance(exception, InvalidCredentials) or isinstance(exception, AuthenticatorError):
        handle_logout(state)


def button_loginout(state):
    """Handle login/logout button click."""

    if state.credentials is None:
        return navigate(state, "login", force=True)
    handle_logout(state)


data = pd.read_csv("data.csv")
chart_data = data.groupby("State")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()

map_data = data.groupby("State")["Sales"].sum().reset_index()

start_date = "2015-01-01"
start_date = pd.to_datetime(start_date)
end_date = "2018-12-31"
end_date = pd.to_datetime(end_date)

categories = list(data["Category"].unique())
selected_category = "Furniture"

selected_subcategory = "Bookcases"
subcategories = list(data[data["Category"] == selected_category]["Sub-Category"].unique())

layout = {"yaxis": {"title": "Revenue (USD)"}, "title": "Sales by State"}

map_fig = generate_map(data)


def change_category(state):
    state.subcategories = list(data[data["Category"] == state.selected_category]["Sub-Category"].unique())
    state.selected_subcategory = state.subcategories[0]


def apply_changes(state):
    state.data = data[
        (pd.to_datetime(data["Order Date"], format="%d/%m/%Y") >= pd.to_datetime(state.start_date))
        & (pd.to_datetime(data["Order Date"], format="%d/%m/%Y") <= pd.to_datetime(state.end_date))
    ]
    state.data = state.data[state.data["Category"] == state.selected_category]
    state.data = state.data[state.data["Sub-Category"] == state.selected_subcategory]
    state.chart_data = state.data.groupby("State")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
    state.layout = {
        "yaxis": {"title": "Revenue (USD)"},
        "title": f"Sales by State for {state.selected_category} - {state.selected_subcategory}",
    }
    state.map_fig = generate_map(state.data)


with tgb.Page() as sales_page:
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
                        # TODO: Make the button inactive if the user is not an admin
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
        with tgb.part(render=lambda credentials: credentials and is_admin.get_traits(credentials)):
            tgb.table(data="{data}")


def menu_option_selected(state, action, info):
    page = info["args"][0]
    navigate(state, to=page)


with tgb.Page() as root_page:
    tgb.menu(
        label="Menu",
        lov=[
            ("sales", Icon("images/map.png", "Sales")),
            ("account", Icon("images/person.png", "Account")),
        ],
        on_action=menu_option_selected,
    )

with tgb.Page() as login_page:
    tgb.login("Welcome to Taipy!")

with tgb.Page() as account_page:
    tgb.text("# Account **Management**", mode="md")
    tgb.button(
        lambda credentials: "Login" if credentials is None else "Logout",
        class_name="plain login-button",
        width="50px",
        on_action=button_loginout,
    )

pages = {
    "/": root_page,
    "sales": sales_page,
    "account": account_page,
    "login": login_page,
}


Gui(pages=pages).run(title="Sales", dark_mode=False)
