import matplotlib.pyplot as plt
import fastf1.plotting
import seaborn as sns

#let's apply the basic f1 styling
fastf1.plotting.setup_mpl()

def plotSpeedTrace(session, driver1Tel, driver1Code, driver2Tel, driver2Code):
    """
    Plots a comparison of speed traces for two drivers
    
    :param session (object): the fastF1 session object
    :param driver1Tel (dataframe): driver 1's telemetry data
    :param driver1Code (str): driver 1's code (e.g 'VER')
    :param driver2Tel (dataframe): driver 2's telemetry data
    :param driver2Code (str): driver 2's code (e.g 'LEC')
    """
    eventName = f"{session.event.EventName} {session.event.year}"
    print(f"Generating chart: {driver1Code} vs {driver2Code}..")
    #first we create the main figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title(f"{eventName} : Speed comparison", fontsize=16)

    #then we plot each driver
    #driver 1
    color1 = fastf1.plotting.get_driver_color(driver1Code, session=session)
    ax.plot(driver1Tel["Distance"], driver1Tel["Speed"], color=color1, label=driver1Code,linewidth=2)
    #driver 2, we'll use dashed line for contrast
    color2 = fastf1.plotting.get_driver_color(driver2Code, session=session)
    ax.plot(driver2Tel["Distance"], driver2Tel["Speed"], color=color2, linestyle="--", label=driver2Code,linewidth=2)

    #now onto the labels and the grid
    ax.set_xlabel("Distance (m)", fontsize=12)
    ax.set_ylabel("Speed (km/h)", fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
    plt.tight_layout()

    return fig