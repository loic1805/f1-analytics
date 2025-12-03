import fastf1

#setting up a cache folder so we don't spam the F1 servers..
fastf1.Cache.enable_cache('cache') 

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def testConnection():
    print(f"{Colors.YELLOW}Calling the API...{Colors.RESET}")
    try:
        #for this test, we'll try to fetch the very minimal data for 2024 Bahrain qualification session
        session = fastf1.get_session(2024, 'Bahrain', 'Q')
        session.load(telemetry=False, laps=False, weather=False)
        print(f"\n{Colors.GREEN}Connected to: {session.event.EventName}{Colors.RESET}")
        return True
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        return False

if __name__ == "__main__":
    testConnection()