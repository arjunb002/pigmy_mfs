import streamlit as st
import random
import string
import re
import pandas as pd
import sys

class Bank_Account():
    # Simulate 20 existing serial numbers (already registered/fake)
    existing_serial_numbers = {
        'A1B2C3D4E5', 'F6G7H8I9J0', 'K1L2M3N4O5', 'P6Q7R8S9T0',
        'U1V2W3X4Y5', 'Z6A7B8C9D0', 'E1F2G3H4I5', 'J6K7L8M9N0',
        'O1P2Q3R4S5', 'T6U7V8W9X0', 'Y1Z2A3B4C5', 'D6E7F8G9H0',
        'I1J2K3L4M5', 'N6O7P8Q9R0', 'S1T2U3V4W5', 'X6Y7Z8A9B0',
        'C1D2E3F4G5', 'H6I7J8K9L0', 'M1N2O3P4Q5', 'R6S7T8U9V0'
    }

    def __init__(self, name_of_customer, daily_deposit, int_rate, maturity, serial_number):
        self.name_of_customer = name_of_customer
        self.daily_deposit = daily_deposit
        self.int_rate = int_rate
        self.maturity = maturity
        self.serial_number = serial_number.strip().upper()
        self.fake_notes = {
            2000: 444023,
            500: 383842,
            200: 36913,
            100: 17245,
            50: 22652,
            20: 0,
            10: 3241
        }

    def bank_note(self):
        return self.serial_number

    def total_investment(self):
        self.investment_amount = self.daily_deposit * self.maturity
        return self.investment_amount

    def total_return(self):
        self.with_int = self.investment_amount * (1 + self.int_rate)
        return self.with_int

    def bank_cost(self):
        self.cost_bank = self.with_int - self.investment_amount
        return self.cost_bank

    def agency_cost(self):
        self.agent_cost = self.investment_amount * 0.035
        return self.agent_cost

    def hardware_cost(self):
        self.machine_cost = 500
        return self.machine_cost

    def total_cost_bank(self):
        self.bank_total = self.bank_cost() + self.agency_cost() + self.hardware_cost()
        return self.bank_total

    def display_fake_notes(self):
        st.markdown("\n📄 **Fake Currency Note Report in 2025 (Predicted from Govt Data):**")
        for denomination, count in sorted(self.fake_notes.items(), reverse=True):
            st.write(f"₹{denomination}: {count} fake notes")

    def get_fake_notes_df(self):
        return pd.DataFrame({
            "Denomination": list(self.fake_notes.keys()),
            "Fake Notes": list(self.fake_notes.values())
        })

def is_valid_serial(serial):
    # 10 alphanumeric characters
    return bool(re.fullmatch(r"[A-Z0-9]{10}", serial))

# Streamlit UI
st.title("🏦 Daily Deposit Account System of 'X' Bank")
st.write("Enter your deposit details and bank note serial number below:")

if 'checked_serials' not in st.session_state:
    st.session_state['checked_serials'] = []

with st.form("deposit_form"):
    name_of_customer = st.text_input("Enter your name:")
    daily_deposit = st.number_input("Enter the daily depositing amount:", min_value=0, step=1)
    int_rate = st.number_input("Enter the interest rate you desire (e.g. 0.04):", min_value=0.0, step=0.01, format="%0.4f")
    maturity = st.number_input("Enter the number of days:", min_value=0, step=1)
    serial_number = st.text_input("Enter the bank note serial number:")
    submitted = st.form_submit_button("Submit")

if submitted:
    error = None
    serial_upper = serial_number.strip().upper()
    if daily_deposit < 0 or int_rate < 0 or maturity < 0:
        error = "Input can't be negative. Please enter positive values."
    elif not serial_upper:
        error = "Serial number cannot be empty."
    elif not is_valid_serial(serial_upper):
        error = "Serial number must be exactly 10 alphanumeric characters (A-Z, 0-9)."

    if error:
        st.error(error)
    else:
        if serial_upper in Bank_Account.existing_serial_numbers:
            st.warning("\n⚠️ Already registered. Possible FAKE note detected!")
            status = "Fake/Registered"
        else:
            st.success("\n✅ Serial number accepted. No match in registered database.")
            status = "Accepted"
        Bank_Account.existing_serial_numbers.add(serial_upper)
        st.session_state['checked_serials'].append({
            "Name": name_of_customer,
            "Serial Number": serial_upper,
            "Status": status
        })

        account = Bank_Account(name_of_customer, daily_deposit, int_rate, maturity, serial_upper)
        st.markdown("---")
        st.header("💰 Summary Report")

        # Use columns for a neat layout
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**👤 Name:** {account.name_of_customer}")
            st.markdown(f"**🔢 Serial Number:** {account.bank_note()}")
            st.metric("💵 Total Investment", f"₹{account.total_investment():,.2f}")
            st.metric("💸 Total Return (with Interest)", f"₹{account.total_return():,.2f}")

        with col2:
            st.metric("🏦 Bank Cost (Interest Paid)", f"₹{account.bank_cost():,.2f}")
            st.metric("🤝 Agent Cost", f"₹{account.agency_cost():,.2f}")
            st.metric("🖨️ Machine Cost", f"₹{account.hardware_cost():,.2f}")
            st.metric("🧮 Total Bank Cost per Person", f"₹{account.total_cost_bank():,.2f}")

        # Optionally, group details in an expander
        with st.expander("See detailed calculations"):
            st.write(f"**Name:** {account.name_of_customer}")
            st.write(f"**Serial Number:** {account.bank_note()}")
            st.write(f"**Total Investment:** ₹{account.total_investment():,.2f}")
            st.write(f"**Total Return with Interest:** ₹{account.total_return():,.2f}")
            st.write(f"**Bank Cost (Interest Earned by customer):** ₹{account.bank_cost():,.2f}")
            st.write(f"**Agent Cost of the bank is:** ₹{account.agency_cost():,.2f}")
            st.write(f"**Machine cost for the bank:** ₹{account.hardware_cost():,.2f}")
            st.write(f"**Total Cost for the bank per person:** ₹{account.total_cost_bank():,.2f}")

        account.display_fake_notes()
        # Fake notes bar chart
        st.subheader("Fake Notes by Denomination (Bar Chart)")
        fake_notes_df = account.get_fake_notes_df().set_index("Denomination")
        st.bar_chart(fake_notes_df)

# Show checked serials in this session
if st.session_state['checked_serials']:
    st.markdown("---")
    st.subheader("Checked Serial Numbers This Session")
    st.dataframe(pd.DataFrame(st.session_state['checked_serials']))
