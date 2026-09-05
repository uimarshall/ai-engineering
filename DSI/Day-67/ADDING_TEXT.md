## Adding Text to a Matplotlib Chart

This beginner example reads height and weight data, plots male records, highlights one patient, and adds labels that make the chart easier to understand.

The Python file is [308_Adding_Text.py](308_Adding_Text.py). The data file is [weights_and_heights.csv](weights_and_heights.csv).

## What Each Part Does

```python
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.markers import MarkerStyle
```

- `matplotlib.pyplot` provides functions for creating charts.
- `pandas` provides DataFrames, which are tables that can be filtered and summarized.
- `MarkerStyle` creates the typed `x` marker used to highlight the selected patient.

```python
body_data = pd.read_csv("weights_and_heights.csv")
```

Reads the CSV file into a DataFrame named `body_data`. Each row represents one person, and columns such as `Gender`, `Weight`, and `Height` contain measurements.

```python
male = body_data[body_data["Gender"] == "Male"]
female = body_data[body_data["Gender"] == "Female"]
```

These lines filter the full table. The first keeps male records and the second keeps female records. The female subset is prepared for future analysis even though this chart focuses on males.

```python
male_sample = male.sample(200, random_state=42)
```

Chooses 200 male records. `random_state=42` makes the selection repeatable, so the same chart is produced each time the script runs.

```python
patient = male_sample.loc[[705]]
patient_weight = patient["Weight"].iloc[0]
patient_height = patient["Height"].iloc[0]
```

Selects patient 705 and extracts the weight and height as individual values. The double brackets in `.loc[[705]]` intentionally keep `patient` as a one-row DataFrame for plotting. `.iloc[0]` then gets a scalar value for `annotate()`, which requires numbers rather than Pandas Series objects.

```python
median_weight = male_sample["Weight"].median()
median_height = male_sample["Height"].median()
min_weight = male_sample["Weight"].min()
min_height = male_sample["Height"].min()
```

Calculates the typical weight and height using the median. It also finds the smallest values so the median labels can be positioned near the edge of the chart.

```python
plt.style.use("seaborn-v0_8-poster")
```

Applies a presentation-friendly chart style with larger text and clearer visual elements.

```python
plt.scatter(male_sample["Weight"], male_sample["Height"], ...)
```

Creates a scatter plot. Each dot represents one person. Weight is on the x-axis and height is on the y-axis. `alpha` controls transparency, `color` controls dot color, and `s` controls dot size.

The next two `scatter()` calls draw the selected patient twice: first as a large pink circle with a red border, then as a red `x`. Layering markers makes the selected record stand out from the rest of the sample.

```python
plt.title(...)
plt.xlabel(...)
plt.ylabel(...)
```

Adds a title and names both axes. Units are important because they tell the reader what the numbers mean.

```python
plt.axvline(x=median_weight, ...)
plt.axhline(y=median_height, ...)
```

Adds vertical and horizontal dashed reference lines. Together they divide the chart into areas representing below-typical and above-typical measurements.

## Adding Annotations

`plt.annotate()` adds text at a meaningful location on a chart. Its important arguments are:

- `text`: the words displayed.
- `xy`: the data point or coordinate being described.
- `xytext`: where the text should appear.
- `textcoords`: how to interpret `xytext`, such as pixel offsets.
- `bbox`: an optional box around the text.
- `arrowprops`: an optional arrow pointing to the data.

The script annotates both median lines and the selected patient. The f-strings insert calculated values into labels, such as `Median Weight (180 lbs)`.

## Why the Series Error Happened

This causes the error:

```python
xy=(patient["Weight"], patient["Height"])
```

Each expression returns a Pandas `Series`, even though the DataFrame has one row. Matplotlib's annotation coordinates must be individual numbers. The corrected version uses:

```python
xy=(patient_weight, patient_height)
```

The `patient_weight` and `patient_height` variables are scalar values extracted with `.iloc[0]`.

## Business Application

The same chart pattern can support a healthcare analytics team reviewing patient measurements:

1. Load measurements from a CSV export or database.
2. Filter records by a group, such as age range, gender, clinic, or treatment plan.
3. Calculate median values to create understandable benchmarks.
4. Plot all records to reveal clusters, unusual values, or possible data-entry problems.
5. Highlight one patient so a clinician can compare that patient with the group.
6. Add annotations so a report remains understandable without someone explaining the chart verbally.

The pattern also applies outside healthcare. A retailer could plot order value against delivery time and highlight a delayed order. A bank could plot income against loan amount and highlight an application for review. A factory could plot machine temperature against production speed and label a measurement outside the normal operating range.

In a production report, replace `Patient 705` with a safe business identifier, validate units and missing values, and avoid exposing personally identifiable information. Reference lines should represent a business-approved benchmark, not automatically be treated as a diagnosis or decision.

## Running the Example

From the `DSI` project directory, use the project environment:

```powershell
uv run python Day-67/308_Adding_Text.py
```

The project dependencies must include Matplotlib and Pandas. The script expects `weights_and_heights.csv` in the current working directory, so running it from `DSI` is recommended.
