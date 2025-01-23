import streamlit as st
import pandas as pd

# Default Values
default_exrate = 30
default_months = 13
main_applicant_sek = 10584
spouse_sek = 4410
child_sek = 2646

# Title in main section
st.markdown(
    "<h3>Calculate the Minimum Living Expense Requirement for Sweden - 2025</h3>", 
    unsafe_allow_html=True
)


# User Inputs moved to the sidebar
st.sidebar.header("User Inputs")

ex_rate = st.sidebar.number_input("Enter Exchange Rate:", value=default_exrate)
no_of_months = st.sidebar.number_input("Enter Number of Months:", value=default_months)
is_spouse = st.sidebar.selectbox("Is your spouse travelling with you?", ["Yes", "No"])
no_of_kids = st.sidebar.selectbox("How many kids do you have?", range(0, 6))  # Dropdown for 0-6

# Calculations
main_cost = main_applicant_sek * no_of_months

if is_spouse == "Yes":
    spouse_cost = spouse_sek * no_of_months
else:
    spouse_cost = 0

child_cost = no_of_kids * child_sek * no_of_months
living_ex = main_cost + spouse_cost + child_cost

rs_living_ex = living_ex * ex_rate
rs_living_ex_margin = rs_living_ex * 1.3

# Display the results in the main section
st.write(f"Your minimum living expenses for <b style='color:red;'>{no_of_months}</b> months will be SEK <b style='color:red;'>{living_ex:,.2f}</b>", unsafe_allow_html=True)
st.write(f"(LKR: <b style='color:red;'>{rs_living_ex:,.2f}</b> at the exchange rate of <b style='color:red;'>{ex_rate}</b>)", unsafe_allow_html=True)

st.write(f"If you need to keep an extra 30% in your bank, the final balance will be LKR <b style='color:red;'>{rs_living_ex_margin:,.2f}</b>.", unsafe_allow_html=True)


# Margin Calculation in two columns
col3, col4 = st.columns(2)

with col3:
    margin = st.slider("Or change your expected extra % of bank balance:", 10, 100, 30, step=5)

# Calculate margin-adjusted costs
marginX = (1 + (margin / 100))
new_margin = rs_living_ex * marginX
st.write(f"Your expected bank balance with extra {margin}% added to the minimum living cost LKR: <span style='color:red;'>{new_margin:,.2f}</span>.", unsafe_allow_html=True)

# Breakdown of costs
rs_main_cost = main_cost * ex_rate
rs_spouse_cost = spouse_cost * ex_rate
rs_child_cost = child_cost * ex_rate

rs_main_cost_m = rs_main_cost * marginX
rs_spouse_cost_m = rs_spouse_cost * marginX
rs_child_cost_m = rs_child_cost * marginX

# Divider for clarity
st.divider()

# Creating the DataFrame
data = {
    "Applicant": ["You", "Spouse", "Kids", "Total"],
    "SEK": [main_cost, spouse_cost, child_cost, living_ex],
    "LKR": [rs_main_cost, rs_spouse_cost, rs_child_cost, rs_living_ex],
    "Expected LKR": [rs_main_cost_m, rs_spouse_cost_m, rs_child_cost_m, new_margin]
}

df = pd.DataFrame(data)

# Display DataFrame
st.write("#### Living Expenses Breakdown")
st.dataframe(df)

# Option to download the DataFrame as a CSV file
csv = df.to_csv(index=False)
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name='living_expense_breakdown.csv',
    mime='text/csv'
)

# Divider for clarity
st.divider()

# Notes section moved to the sidebar
st.sidebar.header("Notes")
st.sidebar.write("""
    Current values taken from [Migrationsverket](https://www.migrationsverket.se/English/Private-individuals/Studying-in-Sweden/Higher-education/Residence-permit-for-studies-in-higher-education.html#family).
    The current exchange rate (LKR to SEK) fluctuates around 30, so it's kept as the default. You can change it with the rate of your relevant bank.
""")
st.sidebar.write("""
    Based on calculations done through an Excel sheet shared by the "SL Sweden Members" group. The group or Admins have no connection with this web app.
""")
st.write("""
    This calculator provides a rough estimate of your living expenses. Keep in mind that costs can fluctuate. We strongly recommend checking the official websites for the latest information. Your privacy is important to us – this tool does not collect any personal data. (2025 - Jan)
""")
