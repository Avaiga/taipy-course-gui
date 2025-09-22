import datetime as dt
import time
from threading import Thread

import taipy.gui.builder as tgb
from taipy.gui import Gui


def update_time(gui: Gui):
    while True:
        gui.broadcast_callback(
            callback=lambda state: state.assign("current_time", dt.datetime.now().strftime("%H:%M:%S"))
        )
        time.sleep(1)


current_time = "HH:MM:SS"

with tgb.Page() as page:
    tgb.text("Current time: {current_time}")

gui = Gui(page=page)

t = Thread(target=update_time, args=(gui,), daemon=True)
t.start()

gui.run(title="Real-time data updates", server_config={"socketio": {"ping_interval": 1}})
