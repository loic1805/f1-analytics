import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plotAnalysis(session, driversData, deltas, refDriver):
    """
    Plots an interactive 5-panel dashboard with Corner Annotations.
    """
    eventName = f"{session.event.EventName} {session.event.year}"
    #the circuits info
    circuit_info = session.get_circuit_info()
    fig = make_subplots(
        rows=5, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.02,
        row_heights=[0.15, 0.40, 0.15, 0.15, 0.15],
        subplot_titles=("Gap to Reference", "Speed", "Throttle", "Brake", "Gear")
    )
    #now adding the driver's trace
    for driver, data in driversData.items():
        tel = data['tel']
        color = data['color']
        width = 3 if driver == refDriver else 1.5
        #1st row - the delta
        if driver in deltas:
            fig.add_trace(go.Scatter(x=deltas[driver]['Distance'], y=deltas[driver]['Delta'], 
                                   mode='lines', name=f"Gap ({driver})", line=dict(color=color, width=1.5),
                                   legendgroup=driver, showlegend=False,
                                   hovertemplate=f"{driver} Gap: %{{y:.3f}}s<extra></extra>"), row=1, col=1)

        #row 2 - speed
        fig.add_trace(go.Scatter(x=tel['Distance'], y=tel['Speed'], 
                               mode='lines', name=driver, line=dict(color=color, width=width),
                               legendgroup=driver,
                               hovertemplate=f"{driver} Speed: %{{y:.1f}} km/h<extra></extra>"), row=2, col=1)

        #row 3 - the throttles
        fig.add_trace(go.Scatter(x=tel['Distance'], y=tel['Throttle'], 
                               mode='lines', name=f"Throttle ({driver})", line=dict(color=color, width=1.5),
                               legendgroup=driver, showlegend=False,
                               hovertemplate=f"{driver} Throttle: %{{y:.0f}}%<extra></extra>"), row=3, col=1)

        #row 4 - brake
        fig.add_trace(go.Scatter(x=tel['Distance'], y=tel['Brake'], 
                               mode='lines', name=f"Brake ({driver})", line=dict(color=color, width=1.5),
                               legendgroup=driver, showlegend=False,
                               hovertemplate=f"{driver} Brake: %{{y:.0f}}<extra></extra>"), row=4, col=1)

        #tow 5 - Gear
        fig.add_trace(go.Scatter(x=tel['Distance'], y=tel['nGear'], 
                               mode='lines', name=f"Gear ({driver})", line=dict(color=color, width=1.5),
                               legendgroup=driver, showlegend=False,
                               hovertemplate=f"{driver} Gear: %{{y:.0f}}<extra></extra>"), row=5, col=1)
    #corner animations
    if circuit_info is not None:
        for index, row in circuit_info.corners.iterrows():
            #a vertical line for the corner
            fig.add_vline(x=row['Distance'], line_width=1, line_dash="dash", line_color="gray", opacity=0.5)
            #we'll place the corner number label at the top of the Speed chart (Row 2)
            fig.add_annotation(
                x=row['Distance'], y=350,
                text=f"{row['Number']}{row['Letter']}",
                showarrow=False,
                row=2, col=1,
                font=dict(size=10, color="gray"),
                yshift=10
            )
    fig.update_layout(
        template="plotly_dark",
        height=1000,
        title=dict(text=f"{eventName}: Telemetry Deep Dive", font=dict(size=20)),
        hovermode="x unified",
        legend=dict(traceorder="normal", orientation="h", y=1.02, x=0.5, xanchor="center")
    )
    
    # onto the labels
    fig.update_yaxes(title_text="Gap (s)", row=1, col=1)
    fig.update_yaxes(title_text="Speed (km/h)", row=2, col=1)
    fig.update_yaxes(title_text="Throttle (%)", row=3, col=1, range=[-5, 105])
    fig.update_yaxes(title_text="Brake level", row=4, col=1, tickvals=[0, 1])
    fig.update_yaxes(title_text="Gear", row=5, col=1)
    fig.update_xaxes(title_text="Distance (m)", row=5, col=1)

    return fig