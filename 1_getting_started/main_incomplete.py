from taipy.gui import Gui
import taipy.gui.builder as tgb
from math import cos, exp

value = 10


def compute_data(decay: int) -> list:
    return [cos(i / 6) * exp(-i * decay / 600) for i in range(100)]


def on_change(state, var, val): ...


def slider_moved(state): ...


with tgb.Page() as page:
    ...

data = compute_data(value)

Gui(page=page).run()
