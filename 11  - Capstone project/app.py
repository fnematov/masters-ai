import streamlit as st
import matplotlib.pyplot as plt
from core.db_manager import SQLiteDBManager
from core.ai_manager import process_message


class App:
    def __init__(self):
        self.db_manager = SQLiteDBManager()

    def show_chart(self):
        """Displays two bar charts: Top 10 Highly Rated Cars & Top 10 Most Ordered Cars"""
        st.markdown("## 📊 Car Insights Dashboard")
        st.write("Here are the top-rated and most ordered cars based on customer interactions and sales.")

        # Fetch Data
        top_rated_cars = self.db_manager.fetch_top_rated_cars()
        top_ordered_cars = self.db_manager.get_top_ordered_cars()

        # Create a two-column layout for dual charts
        col1, col2 = st.columns(2, gap="large")

        # 🔹 Left Chart: Top Rated Cars
        with col1:
            st.markdown("### ⭐ Top 10 Highly Rated Cars")
            if top_rated_cars is not None and not top_rated_cars.empty:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.barh(top_rated_cars["car_name"], top_rated_cars["rating"], color="skyblue")
                ax.set_xlabel("Rating")
                ax.set_title("Top Rated Cars")
                ax.invert_yaxis()
                st.pyplot(fig, use_container_width=True)
            else:
                st.warning("No rating data found.")

        # 🔹 Right Chart: Top Ordered Cars
        with col2:
            st.markdown("### 📦 Top 10 Most Ordered Cars")
            if top_ordered_cars is not None and not top_ordered_cars.empty:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.barh(top_ordered_cars["car_name"], top_ordered_cars["total_orders"], color="lightcoral")
                ax.set_xlabel("Total Orders")
                ax.set_title("Most Ordered Cars")
                ax.invert_yaxis()
                st.pyplot(fig, use_container_width=True)
            else:
                st.warning("No order data found.")

    def show_chat(self):
        """AI Sales Chatbot for a Car Shop"""

        st.markdown("## 🚗 AI Car Sales Manager")
        st.write("Welcome! I'm your **AI-powered Car Sales Manager**. Let me help you find the perfect car!")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "✅ Welcome to our car shop! Looking for your dream car? Ask me anything!", "name": "User_Proxy"}
            ]

        # Create a chat container with a fixed height
        chat_messages = st.container(height=400)

        # Display previous messages inside the container
        with chat_messages:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat input field (fixed at bottom)
        if user_input := st.chat_input("Tell me what car you're looking for..."):
            st.session_state.messages.append({"role": "user", "content": user_input, "name": "User_Proxy"})
            with chat_messages.chat_message("user"):
                st.markdown(user_input)

            # Simulate AI Sales Response
            with st.spinner("Thinking... 🤔"):  # Shows "Thinking..." until response is ready
                response = process_message(st.session_state.messages)  # AI generates the next message

            st.session_state.messages.append({"role": "assistant", "content": response})
            with chat_messages.chat_message("assistant"):
                st.markdown(response)

    def run(self):
        """Runs the Streamlit app with a full-width layout"""
        st.set_page_config(layout="wide")  # Enable full-width mode
        st.title("🚘 Car Data Dashboard")

        # Create a 60-40 column layout that stretches fully
        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            self.show_chart()  # Bigger chart on the left

        with col2:
            self.show_chat()  # Chatbot on the right