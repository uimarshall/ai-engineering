# Overview of Streamlit

## What is Streamlit?

Streamlit is a Python framework for quickly turning data scripts into interactive, shareable web apps. It lets you build an app using Python without needing front-end development experience.

The basic pattern is to import Streamlit (commonly as `st`) and call its functions to display content in the app:

```python
import streamlit as st
import pandas as pd

st.title("My data app")

data = pd.read_csv("data.csv")
st.dataframe(data)
```

Streamlit also provides interactive widgets such as sliders, file uploaders, radio buttons, selection boxes, and date inputs. Widgets can let users provide inputs or filter the data and results shown in the app.

## What can you build?

Streamlit apps can include text, tables, charts, maps, code, and interactive forms. The [Streamlit Gallery](https://streamlit.io/gallery) is a useful source of inspiration: you can explore working apps and, when available, inspect their source code for implementation ideas.

One example from the tutorial is **Eagle Vision**, a bird-classification app. It lets users upload an image or choose a sample, then displays the model’s predicted bird class and confidence alongside similar images. The example demonstrates how a Python machine-learning model can power an interactive app; its reported accuracy and predictions describe that project, not a general guarantee.

## Find the documentation

The [Streamlit documentation](https://docs.streamlit.io) is a reference for building and deploying apps. Its API reference lists the available elements and widgets. For example, the **Number input** documentation describes its parameters and shows both the code and the resulting widget.

Use the docs when you need to check a widget’s options or see how to implement a particular app feature.

## Running and sharing apps

You can run an app locally while developing it, then deploy it so other people can access it online. Streamlit Community Cloud is one option for sharing and hosting Streamlit apps.

Apps can also depend on model files and Python packages. A `requirements.txt` file can declare the packages the app needs, including specific versions, so the deployment environment can install them.

In this course, we will build a simpler Streamlit app around a machine-learning pipeline. The goal is to learn the foundations and then use the gallery and documentation to extend the app with more features.
