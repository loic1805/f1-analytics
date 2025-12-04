import matplotlib.pyplot as plt
from telemetry import loadSession, getFastestLap
from plotter import plotAnalysis
from analysis import computeDeltaTime

def main():
    #setup
    year = 2024
    gp = "Japan"
    sessionType = 'Q'
    driver1 = 'PIA'
    driver2 = 'VER'
    if driver1 == driver2:
        print('Please select two different drivers')
        return
    #data loading
    session = loadSession(year, gp, sessionType)
    if not session:
        return
    #get laps
    d1Lap, d1Tel = getFastestLap(session, driver1)
    d2Lap, d2Tel = getFastestLap(session, driver2)
    if d1Tel is None or d2Tel is None:
        print(f"Couldn't extract telemetry for one or both drivers.")
        return
    #computing the delta
    deltaData = computeDeltaTime(d1Tel, d2Tel)
    #now the plotting
    plotAnalysis(session, d1Tel, driver1, d2Tel, driver2, deltaData)
    print("Comparison report generated !")
    plt.show()

if __name__ == "__main__":
    main()