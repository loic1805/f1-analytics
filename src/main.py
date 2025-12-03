import matplotlib.pyplot as plt
from telemetry import loadSession, getFastestLap
from plotter import plotSpeedTrace

def main():
    #setup
    year = 2024
    gp = "Japan"
    sessionType = 'Q'
    driver1 = 'VER'
    driver2 = 'PIA'
    #data loading
    session = loadSession(year, gp, sessionType)
    if not session:
        return
    #laps getter
    d1Lap, d1Tel = getFastestLap(session, driver1)
    d2Lap, d2Tel = getFastestLap(session, driver2)
    if d1Tel is None or d2Tel is None:
        print(f"Couldn't extract telemetry for one or both drivers.")
        return
    #now the plotting
    eventName = f"{session.event.EventName} {session.event.year} - {sessionType}"
    plotSpeedTrace(session, d1Tel, driver1, d2Tel, driver2)
    print("Displaying on..")
    plt.show()

if __name__ == "__main__":
    main()