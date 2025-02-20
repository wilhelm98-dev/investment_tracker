import streamlit as st
import json

class InvestmentTracker:
    def __init__(self, filename='portfolio.json'):
        self.filename = filename
        self.portfolio = self.load_portfolio()

    def load_portfolio(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_portfolio(self):
        with open(self.filename, 'w') as file:
            json.dump(self.portfolio, file, indent=4)

    def add_investment(self, name, amount, price_per_unit):
        investment = {
            'name': name,
            'amount': amount,
            'price_per_unit': price_per_unit
        }
        self.portfolio.append(investment)
        self.save_portfolio()

    def calculate_total_value(self):
        return sum(investment['amount'] * investment['price_per_unit'] for investment in self.portfolio)

# Streamlit App
tracker = InvestmentTracker()

st.title("Investment Tracker")

st.sidebar.header("Add New Investment")
name = st.sidebar.text_input("Investment Name")
amount = st.sidebar.number_input("Amount", min_value=0.0, format='%f')
price_per_unit = st.sidebar.number_input("Price per Unit", min_value=0.0, format='%f')
if st.sidebar.button("Add Investment") and name and amount > 0 and price_per_unit > 0:
    tracker.add_investment(name, amount, price_per_unit)
    st.sidebar.success("Investment added successfully!")

st.header("Portfolio")
if tracker.portfolio:
    for idx, investment in enumerate(tracker.portfolio, start=1):
        st.write(f"{idx}. {investment['name']} - Amount: {investment['amount']}, Price/Unit: ${investment['price_per_unit']}")
else:
    st.write("Portfolio is empty.")

st.header("Total Portfolio Value")
total_value = tracker.calculate_total_value()
st.write(f"${total_value}")
