import fastf1
import fastf1.plotting
import os 

cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
fastf1.Cache.enable_cache(cache_dir)
fastf1.plotting.setup_mpl()

def loadSession(year, grandPrix, sessionType = 'Q'):
    """
    Load a session and return the associated object
    
    :param year (int): the racing season (e.g, 2024)
    :param grandPrix (str): the GP name (e.g, 'Bahrain')
    :param sessionType (str): 'FP1', 'FP2', 'FP3', 'Q', 'S', 'R'
    """
    print(f"Loading {year} {grandPrix} ({sessionType})...")
    try:
        session = fastf1.get_session(year, grandPrix, sessionType)
        session.load()
        return session
    except Exception as e:
        print(f"Failed to load session: {e}")
        return None
    
def getFastestLap(session, driverCode):
    """
    Get the fastest lap for a specific driver
    """
    print(f"Extracting fastest lap for {driverCode}...")
    try:
        #first we fetch the driver's laps
        laps = session.laps.pick_drivers(driverCode)
        #safeguard, we check if the driver exists in the session
        if len(laps) == 0:
            print(f"Driver '{driverCode}' didn't participate.")
            return None, None
        #if all good, we get his fastest lap and the related telemetry data
        fastestLap = laps.pick_fastest()
        telemetryData = fastestLap.get_telemetry()
        return fastestLap, telemetryData
    except Exception as e:
        print(f"Error extracting lap for {driverCode}: {e}")
        return None, None
    
def loadSessionLight(year, grandPrix, sessionType):
    """
    Loads a session without telemetry/laps data to quickly get the driver list.
    """
    print(f"⬇Loading Driver List: {year} {grandPrix} ({sessionType})...")
    try:
        session = fastf1.get_session(year, grandPrix, sessionType)
        session.load(telemetry=False, laps=False, weather=False)
        return session
    except Exception as e:
        print(f"Failed to load session header: {e}")
        return None
    
if __name__ == "__main__":
    session = loadSession(2024, 'Bahrain')
    if session:
        lap, tel = getFastestLap(session, 'VER')
        if lap is not None:
            print(f"Success! Versatappen Pole lap : {lap['LapTime']}")
