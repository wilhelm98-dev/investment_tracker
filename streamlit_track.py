import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Initialize session state
if 'investments' not in st.session_state:
    st.session_state['investments'] = []
if 'performance_data' not in st.session_state:
    st.session_state['performance_data'] = pd.DataFrame()

# Input Tab
st.title('Investment Performance Tracker')
tab1, tab2 = st.tabs(['Input', 'Performance Over Time'])

with tab1:
    st.header('Enter Today’s Investment Prices')
    name = st.text_input('Investment Name')
    units = st.number_input('Units Bought', min_value=0.0)
    cost_price = st.number_input('Cost Price per Unit', min_value=0.0)
    today_price = st.number_input('Price per Unit Today', min_value=0.0)

    if st.button('Calculate Performance'):
        if name and units > 0 and cost_price > 0 and today_price > 0:
            percentage_difference = ((today_price - cost_price) / cost_price) * 100
            total_profit = (today_price - cost_price) * units
            st.session_state['investments'].append({
                'Name': name,
                'Units': units,
                'Cost Price': cost_price,
                'Today Price': today_price,
                'Percentage Difference (%)': percentage_difference,
                'Total Profit': total_profit
            })
        else:
            st.warning('Please fill in all fields correctly.')

    if st.session_state['investments']:
        df = pd.DataFrame(st.session_state['investments'])
        st.dataframe(df)

    if st.button('Save Investments'):
        if st.session_state['investments']:
            df = pd.DataFrame(st.session_state['investments'])
            df['Date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            if st.session_state['performance_data'].empty:
                st.session_state['performance_data'] = df
            else:
                st.session_state['performance_data'] = pd.concat(
                    [st.session_state['performance_data'], df], ignore_index=True
                )
            st.success('Investments saved!')

with tab2:
    st.header('Performance Over Time')
    if not st.session_state['performance_data'].empty:
        df = st.session_state['performance_data']
        view_option = st.radio('View Performance:', ['Per Product', 'Total Level'])

        if view_option == 'Per Product':
            investment_names = df['Name'].unique()
            selected_investment = st.selectbox('Select Investment', investment_names)
            plot_df = df[df['Name'] == selected_investment]
            fig, ax = plt.subplots()
            ax.plot(plot_df['Date'], plot_df['Total Profit'], marker='o')
            ax.set_title(f'{selected_investment} Performance Over Time')
            ax.set_xlabel('Date')
            ax.set_ylabel('Total Profit')
            st.pyplot(fig)

        else:
            total_df = df.groupby('Date')['Total Profit'].sum().reset_index()
            fig, ax = plt.subplots()
            ax.plot(total_df['Date'], total_df['Total Profit'], marker='o')
            ax.set_title('Total Portfolio Performance Over Time')
            ax.set_xlabel('Date')
            ax.set_ylabel('Total Profit')
            st.pyplot(fig)
    else:
        st.info('No data to display. Please save investments first.')
