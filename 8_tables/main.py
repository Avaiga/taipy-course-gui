from taipy.gui import Gui, Markdown, notify
import taipy.gui.builder as tgb
import pandas as pd


def food_df_on_edit(state, var_name, payload):
    index = payload["index"]  # row index
    col = payload["col"]  # column name
    value = payload["value"]  # new value cast to the column type
    user_value = payload["user_value"]  # new value as entered by the user

    old_value = state.food_df.loc[index, col]
    new_food_df = state.food_df.copy()
    new_food_df.loc[index, col] = value
    state.food_df = new_food_df
    notify(
        state,
        "I",
        f"Edited value from '{old_value}' to '{value}'. (index '{index}', column '{col}')",
    )


def food_df_on_delete(state, var_name, payload):
    index = payload["index"]  # row index

    state.food_df = state.food_df.drop(index=index)
    notify(state, "E", f"Deleted row at index '{index}'")


def food_df_on_add(state, var_name, payload):
    empty_row = pd.DataFrame(
        [[None for _ in state.food_df.columns]], columns=state.food_df.columns
    )
    state.food_df = pd.concat([empty_row, state.food_df], axis=0, ignore_index=True)

    notify(state, "S", f"Added a new row.")


if __name__ == "__main__":
    food_df = pd.DataFrame(
        {
            "Meal": [
                "Lunch",
                "Dinner",
                "Lunch",
                "Lunch",
                "Breakfast",
                "Breakfast",
                "Lunch",
                "Dinner",
            ],
            "Category": [
                "Food",
                "Food",
                "Drink",
                "Food",
                "Food",
                "Drink",
                "Dessert",
                "Dessert",
            ],
            "Name": [
                "Burger",
                "Pizza",
                "Soda",
                "Salad",
                "Pasta",
                "Water",
                "Ice Cream",
                "Cake",
            ],
            "Calories": [300, 400, 150, 200, 500, 0, 400, 500],
        }
    )

    with tgb.Page() as page:
        tgb.text("# Daily Calorie Tracker", mode="md")
        with tgb.layout("1 1"):
            tgb.table(
                "{food_df}",
                editable=True,
                filter=True,
                on_edit=food_df_on_edit,
                on_delete=food_df_on_delete,
                on_add=food_df_on_add,
                group_by__Category=True,
                apply__Calories=sum,
            )

    Gui(page=page).run(dark_mode=False)
