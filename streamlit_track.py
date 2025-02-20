import streamlit as st
import pandas as pd
import os
from datetime import datetime

# CSV file where we store historical snapshots
CSV_FILE = "investment_history.csv"

def load_history():
    """
    Loads the investment history from CSV if it exists,
    otherwise returns an empty DataFrame.
    """
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=[
            "Date",
            "Investment Name",
            "Units",
            "Cost Price",
            "Current Price",
            "Profit",
            "Percentage Difference"
        ])

def save_history(df_history: pd.DataFrame):
    """
    Saves the investment history DataFrame to CSV.
    Appends to existing CSV or creates a new one if none exists.
    """
    # If the CSV doesn't exist, write with headers, otherwise append
    if not os.path.exists(CSV_FILE):
        df_history.to_csv(CSV_FILE, index=False)
    else:
        df_history.to_csv(CSV_FILE, mode='a', header=False, index=False)

def main():
    st.title("Investment Performance Tracker")

    # Create two tabs: Input and Performance
    tab1, tab2 = st.tabs(["Input Tab", "Performance Over Time"])

    # -----------------------------
    # 1) INPUT TAB
    # -----------------------------
    with tab1:
        st.subheader("Enter Today's Prices for Your Investments")

        # Create an initial DataFrame for user inputs
        initial_data = {
            "Investment Name": [""],
            "Units": [0],
            "Cost Price": [0.0],
            "Current Price": [0.0],
        }
        
        input_df = pd.DataFrame(initial_data)
        
        # Let user edit multiple rows if needed
        edited_df = st.experimental_data_editor(
            input_df,
            num_rows="dynamic",
            use_container_width=True,
            key="investment_editor"
        )
        
        # Calculate Profit & Percentage Difference
        if not edited_df.empty:
            edited_df["Profit"] = (edited_df["Current Price"] - edited_df["Cost Price"]) * edited_df["Units"]
            edited_df["Percentage Difference"] = (
                (edited_df["Current Price"] - edited_df["Cost Price"]) / edited_df["Cost Price"] * 100
            ).round(2)
            
            st.write("Calculated Performance (Preview):")
            st.dataframe(edited_df)

        if st.button("Save Investments"):
            # Append today's entries to the historical CSV
            if not edited_df.empty:
                today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                edited_df["Date"] = today
                
                # Reorder columns for consistency
                edited_df = edited_df[
                    [
                        "Date",
                        "Investment Name",
                        "Units",
                        "Cost Price",
                        "Current Price",
                        "Profit",
                        "Percentage Difference",
                    ]
                ]

                save_history(edited_df)
                st.success("Investments saved successfully!")
            else:
                st.warning("No data to save. Please fill in the table first.")

    # -----------------------------
    # 2) PERFORMANCE OVER TIME TAB
    # ----------------------------
