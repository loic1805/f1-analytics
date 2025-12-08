import streamlit as st
import fastf1
import fastf1.plotting
from telemetry import loadSession, loadSessionLight, getFastestLap
from analysis import computeDeltaTime
from plotter import plotAnalysis
from track import plotTrackMap

st.set_page_config(page_title="F1 Telemetry Analytics", layout="wide")

st.title("F1 Telemetry Analytics")
st.markdown("**Multi-Driver Telemetry Comparison.** *Select up to 5 drivers to analyze speed and gaps.*")

#sidebar configuration
with st.sidebar:
    st.header("Session Configuration")
    year = st.selectbox("Season", range(2025, 2018, -1))
    #schedule loader
    try:
        schedule = fastf1.get_event_schedule(year, include_testing=False)
        gp_list = schedule['EventName'].tolist()
        gp = st.selectbox("Grand Prix", gp_list)
    except:
        gp = "Bahrain Grand Prix"

    sessionType = st.radio("Session", ["Q", "R", "FP1", "FP2", "FP3"], horizontal=True)
    
    #dynamic drivers list
    #we cache this because loading the driver list takes a few seconds
    @st.cache_data
    def get_drivers(y, g, s):
        session = loadSessionLight(y, g, s)
        if session:
            return session.drivers #the ids
        return []

    #we get the driver Codes from the session
    #we need to load the light session first to know who drove
    with st.spinner(f"Loading Driver List for {gp}..."):
        session_light = loadSessionLight(year, gp, sessionType)
        
    driver_options = []
    if session_light:
        #let's sort drivers by team or abbreviation
        try:
            driver_options = sorted(session_light.results['Abbreviation'].dropna().unique().tolist())
        except:
            driver_options = ["VER", "LEC", "HAM", "NOR", "PIA", "RUS", "ALO"]
    st.divider()
    selected_drivers = st.multiselect(
        "Select Drivers (Max 5)", 
        options=driver_options, 
        default=driver_options[:2] if len(driver_options) > 1 else [],
        max_selections=5
    )
    if selected_drivers:
        ref_driver = st.selectbox("Reference Driver (Baseline)", options=selected_drivers, index=0)
    else:
        ref_driver = None
    run_btn = st.button("Analyze Telemetry", type="primary", disabled=not selected_drivers)

#main logic
if run_btn and selected_drivers:
    drivers_data = {} #to store telemetry: {'VER': {'tel': df, 'color': 'blue'}, ...}
    deltas = {} #to store gaps: {'LEC': delta_df}
    with st.status("⬇Processing Telemetry...", expanded=True) as status:
        #loading full sessions
        status.write(f"Downloading full telemetry for {year} {gp}...")
        session = loadSession(year, gp, sessionType)
        if not session:
            st.error("Failed to load session.")
            st.stop()
        #loop through drivers
        for driver in selected_drivers:
            status.write(f"Processing {driver}...")
            #get lap data
            lap, tel = getFastestLap(session, driver)
            if tel is not None:
                #store data
                team_color = fastf1.plotting.get_driver_color(driver, session=session)
                drivers_data[driver] = {'tel': tel, 'color': team_color, 'lapTime': lap['LapTime']}
            else:
                st.warning(f"No telemetry found for {driver}")
        #then we compute the delts
        if ref_driver in drivers_data:
            ref_tel = drivers_data[ref_driver]['tel']
            for driver in selected_drivers:
                if driver != ref_driver and driver in drivers_data:
                    # calc delta, in a ref vs driver way (we want the gap to ref)
                    #if computeDeltaTime(ref, driver) result is positivz, it means that ref is ahead
                    delta_df = computeDeltaTime(ref_tel, drivers_data[driver]['tel'])
                    deltas[driver] = delta_df
        status.update(label="Analysis Complete!", state="complete")
    #to keep it clean we plot the reference driver
    map_driver = ref_driver if ref_driver else selected_drivers[0]
    if map_driver in drivers_data:
        st.subheader(f"Track Dominance Map ({map_driver})")
        with st.spinner("Generating Heatmap..."):
            map_fig = plotTrackMap(session, map_driver, drivers_data[map_driver]['tel'])
            st.plotly_chart(map_fig, use_container_width=True)
    st.divider()
    st.subheader(f"Lap Comparison (Reference: {ref_driver})")
    #lap time metrics
    cols = st.columns(len(selected_drivers))
    for i, driver in enumerate(selected_drivers):
        if driver in drivers_data:
            lap_time = str(drivers_data[driver]['lapTime']).split('days')[-1].strip()[:-3] #to runcate the microseconds
            #the color choice
            if driver == ref_driver:
                cols[i].metric(label=driver, value=lap_time, delta="Ref", delta_color="off")
            else:
                #now let's compute the gap in final lap time
                gap = (drivers_data[driver]['lapTime'] - drivers_data[ref_driver]['lapTime']).total_seconds()
                cols[i].metric(label=driver, value=lap_time, delta=f"{gap:+.3f}s", delta_color="inverse")

    #plots
    with st.expander("Export Data"):
        st.write("Download the calculated delta data for external analysis.")
        #let's combine the data into a nice CSV format
        for driver, df in deltas.items():
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"Download {driver} vs {ref_driver} CSV",
                data=csv,
                file_name=f"delta_{driver}_vs_{ref_driver}.csv",
                mime='text/csv',
            )
    fig = plotAnalysis(session, drivers_data, deltas, ref_driver)
    st.plotly_chart(fig, use_container_width=True)