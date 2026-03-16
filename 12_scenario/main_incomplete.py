import datetime as dt

import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from taipy import Config, Frequency, Scope


def clean_data(initial_dataset: pd.DataFrame):
    print("     Cleaning data")
    initial_dataset["Date"] = pd.to_datetime(initial_dataset["Date"])
    cleaned_dataset = initial_dataset[["Date", "Value"]]
    return cleaned_dataset


def predict(cleaned_dataset: pd.DataFrame, day: dt.datetime):
    print("     Predicting")
    train_dataset = cleaned_dataset[cleaned_dataset["Date"] < pd.Timestamp(day)]
    predictions = train_dataset["Value"][-30:].reset_index(drop=True)
    date_range = pd.date_range(start=pd.Timestamp(day), periods=30, freq="D")
    smooth_predictions = predictions.rolling(window=3).mean()
    smooth_predictions = smooth_predictions.round(2)
    return pd.DataFrame({"Date": date_range, "Prediction": predictions, "Smooth Prediction": smooth_predictions})


def evaluate(predictions, cleaned_dataset, day):
    print("     Evaluating")
    expected = cleaned_dataset.loc[cleaned_dataset["Date"] >= pd.Timestamp(day), "Value"][:30].reset_index(drop=True)
    mse = ((predictions["Prediction"] - expected) ** 2).mean()
    return int(mse)


# Input Data Nodes
initial_dataset_cfg = Config.configure_data_node(
    id="initial_dataset",
    storage_type="csv",
    path="12_scenario/dataset.csv",
    scope=Scope.GLOBAL,
)


# TODO: Replace the ... with the correct configuration for the data nodes
# We assume the current day is the 26th of July 2021. This is our default data
# This day can be changed to simulate multiple executions of scenarios on different days
day_cfg = ...
# Remaining Data Nodes
cleaned_dataset_cfg = ...
predictions_cfg = ...
evaluation_cfg = ...


# TODO: Replace the ... with the correct configuration for the tasks
# Task config objects
clean_data_task_cfg = ...
predict_task_cfg = ...
evaluate_task_cfg = ...


# Configure our scenario config.
scenario_cfg = Config.configure_scenario(
    id="scenario",
    task_configs=[clean_data_task_cfg, predict_task_cfg, evaluate_task_cfg],
    frequency=Frequency.MONTHLY,
)

Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)


def update_date(state):
    state.scenario.day.write(state.selected_date)
    state.scenario = state.scenario


selected_date = dt.datetime(2021, 7, 26)

scenario = None
df_metrics = None
data_node = None

with tgb.Page() as root_page:
    tgb.navbar()

with tgb.Page() as scenario_page:
    with tgb.layout("1 3 4"):
        with tgb.part():
            tgb.scenario_selector("{scenario}")
        with tgb.part():
            tgb.text("## Select Prediction Start Date:", mode="md")
            tgb.date("{selected_date}", on_change=update_date)
        with tgb.part():
            tgb.text("## Scenario", mode="md")
            tgb.scenario("{scenario}", show_properties=False, show_sequences=False)
    tgb.job_selector(show_submitted_label=False)
    tgb.scenario_dag("{scenario}")

with tgb.Page() as data_page:
    with tgb.layout("1 5"):
        tgb.data_node_selector("{data_node}")
        tgb.data_node("{data_node}", scenario="{scenario}")

pages = {
    "/": "<|navbar|> <|toggle|theme|> <br/>",
    "Scenario": scenario_page,
    "Data": data_page,
}


if __name__ == "__main__":
    tp.Orchestrator().run()
    tp.Gui(pages=pages).run(title="Backend Demo", dark_mode=False)
