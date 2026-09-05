# -*- coding: utf-8 -*-  # Declares the text encoding used by this Python file.

# This script demonstrates how to add labels and annotations to a Matplotlib chart.

import matplotlib.pyplot as plt  # Imports Matplotlib's plotting functions.
import pandas as pd  # Imports Pandas for reading and working with table-shaped data.
from matplotlib.markers import (
    MarkerStyle,  # Imports the typed marker used for the patient highlight.
)

body_data = pd.read_csv(
    "weights_and_heights.csv"
)  # Loads the CSV file into a Pandas DataFrame.

male = body_data[body_data["Gender"] == "Male"]  # Keeps only rows where Gender is Male.
female = body_data[
    body_data["Gender"] == "Female"
]  # Keeps only rows where Gender is Female.

male_sample = male.sample(
    200, random_state=42
)  # Selects 200 repeatable random male records.
patient = male_sample.loc[
    [705]
]  # Selects patient 705 while keeping the result as a one-row DataFrame.
patient_weight = patient["Weight"].iloc[
    0
]  # Extracts the patient's weight as one scalar value.
patient_height = patient["Height"].iloc[
    0
]  # Extracts the patient's height as one scalar value.

median_weight = male_sample["Weight"].median()  # Calculates the sample's middle weight.
median_height = male_sample["Height"].median()  # Calculates the sample's middle height.
min_weight = male_sample[
    "Weight"
].min()  # Finds the smallest weight used for annotation placement.
min_height = male_sample[
    "Height"
].min()  # Finds the smallest height used for annotation placement.

plt.style.use(
    "seaborn-v0_8-poster"
)  # Applies a readable style designed for larger charts.
plt.scatter(  # Draws one point for every sampled male.
    male_sample["Weight"],  # Uses weight values for the horizontal axis.
    male_sample["Height"],  # Uses height values for the vertical axis.
    alpha=0.5,  # Makes the sample points partly transparent.
    color="royalblue",  # Colors the sample points blue.
    s=700,  # Sets the sample point size.
)
plt.scatter(  # Draws a large pink circle around the selected patient.
    patient["Weight"],  # Uses the patient's weight as the circle's x-coordinate.
    patient["Height"],  # Uses the patient's height as the circle's y-coordinate.
    alpha=1.0,  # Makes the patient highlight fully opaque.
    color="pink",  # Fills the patient highlight with pink.
    s=700,  # Sets the patient highlight size.
    edgecolors="red",  # Adds a red outline around the patient highlight.
    linewidth=2,  # Sets the outline thickness.
)

plt.scatter(  # Draws a red x on top of the selected patient.
    patient["Weight"],  # Uses the patient's weight for the x-coordinate.
    patient["Height"],  # Uses the patient's height for the y-coordinate.
    marker=MarkerStyle("x"),  # Uses a typed x marker to emphasize the patient.
    alpha=1.0,  # Makes the x fully visible.
    color="red",  # Colors the x red.
    s=250,  # Sets the x marker size.
    linewidth=5,  # Sets the x marker thickness.
)

plt.title("Weights vs.  Height for Males")  # Adds a descriptive chart title.
plt.xlabel("Weight (lbs)")  # Names the horizontal axis and its unit.
plt.ylabel("Height (in)")  # Names the vertical axis and its unit.
plt.axvline(
    x=median_weight, color="black", linestyle="--"
)  # Draws a dashed line at the median weight.
plt.axhline(
    y=median_height, color="black", linestyle="--"
)  # Draws a dashed line at the median height.

plt.annotate(  # Adds a label for the median weight line.
    text=f"Median Weight ({round(median_weight)} lbs)",  # Builds the label text with the calculated value.
    xy=(median_weight, min_height),  # Sets the data coordinate where the label points.
    xytext=(10, -10),  # Moves the label by 10 pixels right and 10 pixels down.
    textcoords="offset pixels",  # Makes xytext use pixel offsets instead of data coordinates.
    fontsize=16,  # Sets the label font size.
)

plt.annotate(  # Adds a label for the median height line.
    text=f"Median Height ({round(median_height)} in)",  # Builds the label text with the calculated value.
    xy=(min_weight, median_height),  # Sets the data coordinate where the label points.
    xytext=(-10, 10),  # Moves the label by 10 pixels left and 10 pixels up.
    textcoords="offset pixels",  # Makes xytext use pixel offsets instead of data coordinates.
    fontsize=16,  # Sets the label font size.
)

plt.annotate(  # Adds a label and arrow pointing to the selected patient.
    text="Patient 705",  # Sets the text shown beside the patient marker.
    xy=(
        patient_weight,
        patient_height,
    ),  # Uses scalar coordinates required by annotate().
    xytext=(140, 74),  # Places the label at the specified chart position.
    fontsize=25,  # Makes the patient label easy to read.
    bbox=dict(
        boxstyle="round", fc="salmon", ec="red"
    ),  # Draws a rounded label box with red edges.
    arrowprops=dict(  # Configures the arrow connecting the label to the patient.
        arrowstyle="wedge, tail_width=1.",  # Gives the arrow a wide wedge shape.
        fc="salmon",  # Fills the arrow with salmon color.
        ec="red",  # Gives the arrow a red edge.
        patchA=None,  # Removes the default patch at the arrow's starting point.
        connectionstyle="arc3,rad=-0.1",  # Bends the arrow slightly.
    ),
)

plt.tight_layout()  # Adjusts spacing so chart elements do not overlap.
plt.show()  # Displays the completed chart.
