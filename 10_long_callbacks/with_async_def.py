import taipy.gui.builder as tgb
from taipy.gui import Gui, State, notify


async def approximate_pi(state: State):
    try:
        k, s = 3.0, 1.0
        pi_list = []
        num_iterations = int(state.num_iterations)

        for i in range(num_iterations):
            s = s - ((1 / k) * (-1) ** i)
            k += 2

            # Log approximation at intervals
            if (i + 1) % (int(num_iterations / 100) + 1) == 0:
                pi_list.append(4 * s)

            # Update progress
            if (i + 1) % (int(num_iterations / 50) + 1) == 0:
                state.progress = (i + 1) / num_iterations * 100

        state.pi_list = pi_list
        state.progress = 100
        notify(state, "success", "Approximation completed")
    except Exception as e:
        notify(state, "error", "An error occurred during approximation")
        print(e)


# Initial state variables
num_iterations = 20000000
pi_list = []
progress = 0
layout = {
    "xaxis": {"title": "Iteration (Percentage of Total Iterations)"},
    "yaxis": {"title": "Pi Approximation"},
}

with tgb.Page() as page:
    tgb.text("# Approximating **Pi** using the Leibniz formula", mode="md")
    tgb.number("{num_iterations}", label="Number of iterations")
    tgb.button("Approximate Pi", on_action=approximate_pi)

    tgb.progress(
        "{progress}",
        show_value=True,
        title=lambda progress: "Running..." if progress < 100 else "Finished",
        title_anchor="right",
        render=lambda progress: progress not in [0, 100],
    )
    with tgb.part(render=lambda pi_list: pi_list != []):
        tgb.text("## Evolution of approximation", mode="md")
        tgb.chart("{pi_list}", layout="{layout}")

Gui(page).run(dark_mode=False, server_config={"socketio": {"ping_interval": 1}})
