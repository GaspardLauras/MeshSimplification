import plotly.graph_objects as go

fig = go.Figure(
    data=[
        go.Mesh3d(
            x=[0, 0, 1, 1, 0, 0, 1, 1],
            y=[0, 1, 1, 0, 0, 1, 1, 0],
            z=[0, 0, 0, 0, 1, 1, 1, 1],
            color='lightpink', 
            opacity=0.50
        )
    ]
)
fig.show()



fig2 = go.Figure(data=[
    go.Mesh3d(
            x=[0, 0, 1, 1, 0, 0, 1, 1],
            y=[0, 1, 1, 0, 0, 1, 1, 0],
            z=[0, 0, 0, 0, 1, 1, 1, 1],
        colorbar_title='z',
        colorscale=[[0, 'gold'],
                    [0.5, 'mediumturquoise'],
                    [1, 'magenta']],
        # Intensity of each vertex, which will be interpolated and color-coded
        intensity=[0, 0.33, 0.66, 1],
        # i, j and k give the vertices of triangles
        # here we represent the 4 triangles of the tetrahedron surface
        i=[0, 1, 2, 3],
        j=[0, 1, 2, 3],
        k=[0, 1, 2, 3],
        name='y',
        showscale=True
    )
])
fig2.show()