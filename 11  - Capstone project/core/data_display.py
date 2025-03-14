import streamlit as st

class StreamlitDataDisplay:
    def render(self, data):
        """Displays the dataset from SQLite using Streamlit"""
        if data is not None and not data.empty:
            st.write("### 🚗 Car Dataset Overview")
            st.dataframe(data)
        else:
            st.warning("No data found in the database.")