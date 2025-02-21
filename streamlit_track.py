import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# File path for data storage
DATA_FILE = 'investments_data.csv'

# Load existing data or initialize DataFrame
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=['Date', 'Type', 'Name', 'Amount', 'CostPrice', 'CurrentPrice', 'Profit', 'PercentageChange'])

# Save data to CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Calculate profit and percentage change
def calculate_performance(amount, cost_price, current_price):
    profit = (current_price - cost_price) * amount
    percentage_change = ((current_price - cost_price) / cost_price) * 100
    return profit, percentage_change

# Main app
st.sidebar.title("💸 Investment Tracker")
page = st.sidebar.radio("Navigate", ["📥 Input", "📈 Performance", "💰 Net Worth"])

# Load data
df = load_data()

if page == "📥 Input":
    st.title("📥 Input - Add Today's Prices")

    with st.form(key='input_form'):
        date = st.date_input("Date")
        investment_type = st.selectbox("Type", ["Stocks", "Bonds", "Real Estate", "Crypto", "Other"])
        name = st.text_input("Name")
        amount = st.number_input("Amount", min_value=0.0)
        cost_price = st.number_input("Cost Price per Unit", min_value=0.0)
        current_price = st.number_input("Current Price per Unit", min_value=0.0)

        submit_button = st.form_submit_button(label='Save Investments')

    if submit_button:
        profit, percentage_change = calculate_performance(amount, cost_price, current_price)
        new_data = pd.DataFrame({
            'Date': [date],
            'Type': [investment_type],
            'Name': [name],
            'Amount': [amount],
            'CostPrice': [cost_price],
            'CurrentPrice': [current_price],
            'Profit': [profit],
            'PercentageChange': [percentage_change]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success("Investment data saved!")

    st.write("### Current Investments")
    st.dataframe(df)

elif page == "📈 Performance":
    st.title("📈 Performance Over Time")

    if not df.empty:
        investment_names = df['Name'].unique()
        selected_investment = st.selectbox("Select Investment", ['Total Portfolio'] + list(investment_names))

        if selected_investment == 'Total Portfolio':
            df['CumulativeProfit'] = df.groupby('Date')['Profit'].transform('sum')
            st.line_chart(df.set_index('Date')['CumulativeProfit'])
        else:
            investment_df = df[df['Name'] == selected_investment]
            st.line_chart(investment_df.set_index('Date')['Profit'])

    else:
        st.warning("No investment data available. Please add investments in the Input tab.")

elif page == "💰 Net Worth":
    st.title("💰 Net Worth")

    if not df.empty:
        total_net_worth = (df['Amount'] * df['CurrentPrice']).sum()
        st.metric(label="Total Net Worth", value=f"${total_net_worth:,.2f}")

        category_breakdown = df.groupby('Type').apply(lambda x: (x['Amount'] * x['CurrentPrice']).sum())
        st.bar_chart(category_breakdown)

    else:
        st.warning("No investment data available. Please add investments in the Input tab.")
