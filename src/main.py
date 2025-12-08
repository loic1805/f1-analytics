import matplotlib.pyplot as plt
import argparse
import sys
import fastf1
from telemetry import loadSession, getFastestLap
from plotter import plotAnalysis
from analysis import computeDeltaTime

def interactiveInput():
    """
    Guides the user through selecting Year, GP, Session, and Drivers.
    """
    print("\n🏎️  F1 TELEMETRY ANALYSIS WIZARD 🏎️")
    print("-----------------------------------")
    
    # 1. Select Year
    while True:
        try:
            year = int(input("1️⃣  Enter Season Year (e.g. 2021): "))
            if 2018 <= year <= 2025: # FastF1 supports from 2018 well
                break
            print("⚠️  Please enter a year between 2018 and current.")
        except ValueError:
            print("⚠️  Invalid number.")

    # 2. Select Grand Prix (Fetch Schedule)
    print(f"\n📅 Fetching {year} Schedule...")
    schedule = fastf1.get_event_schedule(year, include_testing=False)
    
    # Filter out future races (optional, but keeps list clean)
    # displaying only RoundNumber and EventName
    print("\nAvailable Races:")
    for i, row in schedule.iterrows():
        print(f"   {row['RoundNumber']}. {row['EventName']}")
    
    while True:
        try:
            roundNum = int(input("\n2️⃣  Select Race Round (Number): "))
            # Get the specific event row
            event = schedule[schedule['RoundNumber'] == roundNum]
            if not event.empty:
                gpName = event.iloc[0]['EventName']
                break
            print("⚠️  Invalid round number.")
        except ValueError:
            print("⚠️  Invalid input.")

    # 3. Select Session
    print(f"\n📍 Selected: {gpName}")
    print("   [Q] Qualifying (Recommended)")
    print("   [R] Race")
    print("   [FP1/FP2/FP3] Practice")
    print("   [S] Sprint")
    
    sessionType = input("\n3️⃣  Select Session Code [Default: Q]: ").upper()
    if not sessionType:
        sessionType = 'Q'

    # 4. Select Drivers (Fetch Entry List)
    print(f"\n👥 Loading Driver List for {gpName}...")
    
    # We do a 'light' load just to get the drivers (no telemetry yet)
    try:
        session = fastf1.get_session(year, gpName, sessionType)
        session.load(telemetry=False, laps=False, weather=False)
        
        # Show drivers sorted by team
        print("\n   Code  |  Driver             |  Team")
        print("   ------+---------------------+------------------")
        # get driver list from session results
        results = session.results
        for driver in session.drivers:
            # Look up driver info in the results table
            info = results.loc[driver]
            print(f"   {info['Abbreviation']:<5} |  {info['FullName']:<19} | {info['TeamName']}")
            
    except Exception as e:
        print(f"⚠️  Could not load driver list: {e}")
        print("   (You'll have to type the codes manually)")

    print("\nWho are we comparing?")
    d1 = input("4️⃣  Driver 1 Code (e.g. VER): ").upper()
    d2 = input("5️⃣  Driver 2 Code (e.g. LEC): ").upper()
    
    return year, gpName, sessionType, d1, d2

def parse_args():
    """
    Parse command line arguments for 'Fast Mode'.
    """
    parser = argparse.ArgumentParser(description="F1 Telemetry Analysis Tool")
    parser.add_argument("--year", type=int, help="Year of the race")
    parser.add_argument("--race", type=str, help="Name of the Grand Prix")
    parser.add_argument("--session", type=str, default="Q", help="Session type")
    parser.add_argument("--driver1", type=str, help="Code for Driver 1")
    parser.add_argument("--driver2", type=str, help="Code for Driver 2")
    return parser.parse_args()

def main():
    # Check if arguments were provided (Fast Mode)
    # If only script name is present (len=1), go Interactive
    if len(sys.argv) == 1:
        year, gp, sessionType, driver1, driver2 = interactiveInput()
    else:
        # Fast Mode logic
        args = parse_args()
        if not all([args.year, args.race, args.driver1, args.driver2]):
             print("❌ Error: In Fast Mode, you must provide --year, --race, --driver1, and --driver2")
             print("   Or run without arguments to use the Wizard.")
             return
        year = args.year
        gp = args.race
        sessionType = args.session
        driver1 = args.driver1.upper()
        driver2 = args.driver2.upper()

    print(f"\n🚀 Starting Analysis: {year} {gp} [{sessionType}]")
    print(f"⚔️  Duel: {driver1} vs {driver2}")

    if driver1 == driver2:
        print("❌ Error: Please select two different drivers.")
        return

    # Load Data (Full Load)
    session = loadSession(year, gp, sessionType)
    if not session:
        print("❌ Session load failed.")
        return

    # Get Laps
    d1Lap, d1Tel = getFastestLap(session, driver1)
    d2Lap, d2Tel = getFastestLap(session, driver2)
    
    if d1Tel is None or d2Tel is None:
        print("❌ Could not extract telemetry for one or both drivers.")
        return
    
    # Compute Delta
    deltaData = computeDeltaTime(d1Tel, d2Tel)
    
    # Plot
    plotAnalysis(session, d1Tel, driver1, d2Tel, driver2, deltaData)
    
    print("\n📊 Dashboard generated successfully!")
    plt.show()

if __name__ == "__main__":
    main()