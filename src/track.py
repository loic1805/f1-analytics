import plotly.graph_objects as go
import numpy as np

def plotTrackMap(session, driver, tel):
    """
    Plots the track map with speed heatmap for a specific driver.
    """
    eventName = f"{session.event.EventName} {session.event.year}"
    #create the scatter plot
    #to enable the colors gradient for the heatmap, we'll use markers instead of lines
    fig = go.Figure(data=go.Scatter(
        x=tel['X'], 
        y=tel['Y'], 
        mode='markers', 
        marker=dict(
            size=4,
            color=tel['Speed'],
            colorscale='Viridis',
            colorbar=dict(title='Speed (km/h)'),
            showscale=True
        ),
        text=tel['Speed'],
        hovertemplate=f"{driver} <br>Speed: %{{text:.0f}} km/h<br>X: %{{x:.0f}}<br>Y: %{{y:.0f}}<extra></extra>"
    ))
    #let's add the corner numbers
    try:
        circuit_info = session.get_circuit_info()
        if circuit_info is not None:
            for index, row in circuit_info.corners.iterrows():
                fig.add_annotation(
                    x=row['X'],
                    y=row['Y'],
                    text=str(row['Number']) + row['Letter'],
                    showarrow=True,
                    arrowhead=1,
                    arrowcolor="white",
                    font=dict(color="white", size=10),
                    bgcolor="black",
                    opacity=0.7
                )
    except Exception as e:
        print(f"Could not load corner info: {e}")
    fig.update_layout(
        template="plotly_dark",
        title=dict(text=f"{eventName} - {driver} Speed Map", font=dict(size=20)),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, visible=False, scaleanchor="x", scaleratio=1),
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig