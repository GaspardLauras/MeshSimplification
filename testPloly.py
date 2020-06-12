import plotly.graph_objects as go
import plotly.express as px
import numpy as np

df = px.data.iris()
print(type(df))
fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                    color='petal_length', symbol='species')
fig.show()