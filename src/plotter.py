import matplotlib.pyplot as plt
import fastf1.plotting

#dark mode
plt.style.use('dark_background')

#let's apply the basic f1 styling
fastf1.plotting.setup_mpl()

def plotAnalysis(session, driver1Tel, driver1Code, driver2Tel, driver2Code, deltaData):
    """
    Plots a dual analysis for two drivers: (1) a comparison of their speed traces, and (2) a delta time (gap) analysis.
    
    The first subplot compares the speed traces of both drivers over distance.
    The second subplot shows the delta time (gap) between the two drivers as a function of distance.
    
    :param session (object): the fastF1 session object
    :param driver1Tel (dataframe): driver 1's telemetry data
    :param driver1Code (str): driver 1's code (e.g 'VER')
    :param driver2Tel (dataframe): driver 2's telemetry data
    :param driver2Code (str): driver 2's code (e.g 'LEC')
    :param deltaData (dataframe): calculated time gap with 'Distance' and 'Delta' columns
    """
    eventName = f"{session.event.EventName} {session.event.year}"
    print(f"Generating chart: {driver1Code} vs {driver2Code}..")
    #first we create the main figure (two subplots : 2 rows 1 column, sharing the x axis)
    fig, ax = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

    #PLOT 1 : Speed trace
    ax[0].set_title(f"{eventName}: Speed Comparison", fontsize=16, color='white')
    #let's plot each driver
    #driver 1
    color1 = fastf1.plotting.get_driver_color(driver1Code, session=session)
    ax[0].plot(driver1Tel["Distance"], driver1Tel["Speed"], color=color1, label=driver1Code,linewidth=2)

    #driver 2, we'll use dashed line for contrast
    color2 = fastf1.plotting.get_driver_color(driver2Code, session=session)
    ax[0].plot(driver2Tel["Distance"], driver2Tel["Speed"], color=color2, linestyle="--", label=driver2Code, linewidth=2)

    #now the grid and the labels
    ax[0].set_ylabel("Speed (km/h)", fontsize=12)
    ax[0].legend(fontsize=12)
    ax[0].grid(color="gray", linestyle=":", linewidth=0.5, alpha=0.5)

    #PLOT 2 : Time comparison
    ax[1].plot(deltaData['Distance'], deltaData['Delta'], color='white', linewidth=1)
    #we'll add a horizontal line at 0 exactly
    ax[1].axhline(0, color='gray', linestyle='--', linewidth=1)

    #and finally the grid and the labels
    ax[1].set_ylabel(f"Gap (s)\n({driver1Code} Faster)", fontsize=10)
    ax[1].set_xlabel("Distance (m)", fontsize=12)
    ax[1].grid(color="gray", linestyle=":", linewidth=0.5, alpha=0.5)

    plt.tight_layout()

    return fig