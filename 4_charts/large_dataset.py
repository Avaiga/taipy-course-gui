import numpy as np
import pandas as pd
import taipy.gui.builder as tgb
from taipy.gui import Gui
from taipy.gui.data.decimator import MinMaxDecimator, LTTB, RDP, ScatterDecimator

# Generate a random dataset
#   Compute the 'X' data
#     Generate 50000 x values (a sequence of integers)
x_values = np.linspace(1, 100, 50000)

#   Compute the 'Y' data
#     Define the combined log-sine function
y_values = np.log(x_values) * np.sin(x_values / 5)
#   Introduce some noise
#     Create a mask with a True value with a 1 % probability
noise_mask = np.random.rand(*y_values.shape) < 0.01
#     The noise values
noise_values = np.random.uniform(-0.5, 0.5, size=np.sum(noise_mask))
#     Add the noise to the 'Y' values
y_values_noise = np.copy(y_values)  # Copy original array
y_values_noise[noise_mask] += noise_values
# Create the DataFrame
data = pd.DataFrame({"X": x_values, "Y": y_values_noise})

# Create a decimator to reduce the number of points displayed
decimator = MinMaxDecimator(200)

with tgb.Page() as page:
    tgb.text("# Large dataset - Decimator", mode="md")
    tgb.chart(data="{data}", x="X", y="Y", mode="markers", decimator=decimator)

Gui(page=page).run(title="Large dataset - Decimator")
