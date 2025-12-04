import pandas as pd
import numpy as np

def computeDeltaTime(driver1Tel, driver2Tel):
    """
    Computes the time difference between two drivers over the course of a lap.
    Returns a dataframe with 'Distance' and 'Delta'.
    
    Positive delta means Driver 1 is faster (Driver 2 took more time to reach the same point).
    Negative delta means Driver 2 is faster.
    :param driver1Tel (dataframe): Driver 1's telemetry data
    :param driver2Tel (dataframe): Driver 2's telemetry data
    """
    #let's create a common distance axis (0 to the end of the lap)
    #then we take the shorter total distance to avoid extrapolation errors
    maxDist = min(driver1Tel['Distance'].max(), driver2Tel['Distance'].max())
    #then we create distinct points every 1 meter
    sectionDist = np.linspace(0, maxDist, num=max(2, int(maxDist)))

    #in order for this to work correctly, we need to convert Time to seconds
    #also we need strictly increasing time
    d1TimeSeconds = driver1Tel['Time'].dt.total_seconds()
    d2TimeSeconds = driver2Tel['Time'].dt.total_seconds()

    #now we interpolate time
    #basically 'at distance x, what was the time for driver 1?'
    d1Interp = np.interp(sectionDist, driver1Tel['Distance'], d1TimeSeconds)
    d2Interp = np.interp(sectionDist, driver2Tel['Distance'], d2TimeSeconds)

    #now we can compute the delta (d2 time - d1 time)
    #if d2 takes 100s and d1 takes 99s, delta will be +1.0s
    deltaSeconds = d2Interp - d1Interp

    return pd.DataFrame({
        'Distance': sectionDist,
        'Delta': deltaSeconds
    })