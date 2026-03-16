"""This example demonstrates three approaches to handling user interactions and events.

From the most general to the most specific:

1. Global callbacks
2. Local callbacks
3. Expression evaluation in curly braces

It is often best to start from the most specific and generalize as needed.
"""

from taipy.gui import Gui
import taipy.gui.builder as tgb
from math import cos, exp

number = 10


def compute_data(decay: int) -> list:
    return [cos(i / 6) * exp(-i * decay / 600) for i in range(100)]


def on_change(state, var_name: str, var_value):
    # Approach 1: Global callbacks
    # The global callback is triggered on a state variable change
    # NOTE: If the state variable change was caused by a user action (e.g., moving a slider), if a local callback exists
    # for that visual element, the local callback is executed INSTEAD of the global callback
    if var_name == "number":
        print("Global callback triggered with number =", var_value)
        state.data = compute_data(state.number)


def slider_moved(state):
    # Approach 2: Local callbacks
    # The local callback must be bound to a specific visual element (e.g., a slider)
    print("Local callback triggered with number =", state.number)
    state.data = compute_data(state.number)


with tgb.Page() as page:
    tgb.text("# Taipy Getting Started", mode="md")

    # Global on_change callback is (implicitly) called in this case
    tgb.slider("{number}", label="Global on_change callback")

    # Local slider_moved callback is called in this case
    tgb.slider("{number}", on_change=slider_moved, label="Local slider_moved callback")

    # Read-only number display via expression evaluation
    tgb.number("{number * 2}", active=False)

    # Approach 3: Using functions directly in curly braces
    # Expression is evaluated each time a state variable that is used in it (`number`, in this case) is updated
    tgb.chart("{compute_data(number)}")

    # Approach 3b: Using lambda functions
    # Variation of Approach 3 where a lambda function is used to call the function with the state variable (`number`) as argument
    tgb.chart(lambda number: compute_data(number))


data = compute_data(number)  # This is not needed for Approach 3

gui = Gui(page=page)
# gui.on_change = on_change  # I can optionally explicitly register the on_change function
gui.run()
