import matplotlib.pyplot as plt
import fastf1.plotting
import seaborn as sns

#let's apply the basic f1 styling
fastf1.plotting.setup_mpl()

def plotSpeedTrace(driver1Tel, driver1Code, driver2Tel, driver2Code, grandPrixName):
    """
    Plots a comparison of speed traces for two drivers
    
    :param driver1Tel (dataframe): driver 1's telemetry data
    :param driver1Code (str): driver 1's code (e.g 'VER')
    :param driver2Tel (dataframe): driver 2's telemetry data
    :param driver2Code (str): driver 2's code (e.g 'LEC')
    :param grandPrixName (str): the chart's title
    """