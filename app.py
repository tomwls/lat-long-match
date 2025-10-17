import streamlit as st
import pandas as pd
from geopy.distance import geodesic

st.title("📍 Device-to-Branch Location Matcher")

# Upload files
branches_file = st.file_uploader("Upload branches file", type=["csv", "xlsx"])
devices_file = st.file_uploader("Upload devices file", type=["csv", "xlsx"])

if branches_file and devices_file:
    # Load files
    branches = pd.read_excel(branches_file) if branches_file.name.endswith("xlsx") else pd.read_csv(branches_file)
    devices = pd.read_excel(devices_file) if devices_file.name.endswith("xlsx") else pd.read_csv(devices_file)

    st.success("✅ Files loaded successfully!")

    # Function to find nearest branch
    def nearest_branch(device_lat, device_lon):
        distances = branches.apply(
            lambda row: geodesic((device_lat, device_lon), (row["Latitude"], row["Longitude"])).meters,
            axis=1
        )
        nearest_idx = distances.idxmin()
        return branches.loc[nearest_idx, "Branch Name"], distances.min()

    # Compute nearest branch for all devices
    devices[["Nearest Branch", "Distance (m)"]] = devices.apply(
        lambda row: pd.Series(nearest_branch(row["Latitude"], row["Longitude"])),
        axis=1
    )

    # Display results
    st.subheader("Matched Results")
    st.dataframe(devices)

    # Download button
    st.download_button(
        label="Download results as CSV",
        data=devices.to_csv(index=False).encode("utf-8"),
        file_name="device_branch_matches.csv",
        mime="text/csv"
    )
