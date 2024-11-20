import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv("data.csv")

state_codes = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}


def generate_map(data: pd.DataFrame) -> go.Figure:
    map_data = data.groupby("State")["Sales"].sum().reset_index()
    map_data["text"] = (
        map_data["State"] + "<br>" + "Sales: $" + map_data["Sales"].astype(str)
    )
    map_data["codes"] = map_data["State"].map(state_codes)

    fig = go.Figure(
        data=go.Choropleth(
            locations=map_data["codes"],
            z=map_data["Sales"].astype(float),
            locationmode="USA-states",
            colorscale="Reds",
            colorbar_title="Sales (USD)",
            hoverinfo="none",
        )
    )

    for i, row in map_data.iterrows():
        fig.add_trace(
            go.Scattergeo(
                locationmode="USA-states",
                locations=[row["codes"]],
                text=f"{row['codes']}",
                hovertext=f"{row['State']}<br>${row['Sales']:,.2f}",
                hoverinfo="text",
                mode="text",
                textfont=dict(size=7),
            )
        )

    fig.update_layout(
        title_text="Sales by State",
        geo_scope="usa",
        showlegend=False,
    )

    return fig


if __name__ == "__main__":
    fig = generate_map(data)
    fig.show()
