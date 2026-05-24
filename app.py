import streamlit as st
from bank_management import Bank

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Bank Management System")


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------------------------------------------
# BEFORE LOGIN
# ---------------------------------------------------

if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Create Account", "Login"]
    )

    # ---------------------------------------------------
    # CREATE ACCOUNT
    # ---------------------------------------------------

    if menu == "Create Account":

        st.subheader("📝 Create New Account")

        name = st.text_input("Enter Name")

        email = st.text_input("Enter Email")

        pin = st.text_input(
            "Enter 4 Digit PIN",
            type="password"
        )

        age = st.number_input(
            "Enter Age",
            min_value=18,
            step=1
        )

        phone = st.text_input(
            "Enter Phone Number"
        )

        if st.button("Create Account"):

            try:

                success, response = Bank.create_account(
                    name=name,
                    email=email,
                    pin=int(pin),
                    age=age,
                    phone=int(phone)
                )

                if success:

                    st.success(
                        "✅ Account Created Successfully"
                    )

                    st.write("## 📄 Account Details")

                    st.write(
                        f"👤 Name : {response['name']}"
                    )

                    st.write(
                        f"📧 Email : {response['email']}"
                    )

                    st.write(
                        f"📱 Phone : {response['phone']}"
                    )

                    st.write(
                        f"🎂 Age : {response['age']}"
                    )

                    st.write(
                        f"🏦 Account Number : {response['accountNumber']}"
                    )

                    st.write(
                        f"💰 Balance : ₹{response['balance']}"
                    )

                else:
                    st.error(response)

            except:
                st.error("❌ Please Enter Valid Details")

    # ---------------------------------------------------
    # LOGIN
    # ---------------------------------------------------

    elif menu == "Login":

        st.subheader("🔐 Login")

        acc_number = st.text_input(
            "Enter Account Number"
        )

        pin = st.text_input(
            "Enter PIN",
            type="password"
        )

        if st.button("Login"):

            try:

                user = Bank.login(
                    acc_number,
                    int(pin)
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.rerun()

                else:
                    st.error(
                        "❌ Invalid Account Number or PIN"
                    )

            except:
                st.error("❌ Enter Valid Credentials")


# ---------------------------------------------------
# AFTER LOGIN
# ---------------------------------------------------

else:

    user = st.session_state.user

    st.sidebar.success(
        f"Welcome {user['name']} 👋"
    )

    operation = st.sidebar.selectbox(
        "Bank Operations",
        [
            "View Account Details",
            "Check Balance",
            "Deposit Money",
            "Withdraw Money",
            "Update Account",
            "Delete Account",
            "Logout"
        ]
    )

    # ---------------------------------------------------
    # VIEW ACCOUNT DETAILS
    # ---------------------------------------------------

    if operation == "View Account Details":

        st.subheader("📄 Account Details")

        st.write(f"👤 Name : {user['name']}")

        st.write(f"📧 Email : {user['email']}")

        st.write(f"📱 Phone : {user['phone']}")

        st.write(f"🎂 Age : {user['age']}")

        st.write(
            f"🏦 Account Number : {user['accountNumber']}"
        )

        st.write(
            f"💰 Balance : ₹{user['balance']}"
        )

    # ---------------------------------------------------
    # CHECK BALANCE
    # ---------------------------------------------------

    elif operation == "Check Balance":

        st.subheader("💰 Account Balance")

        st.info(
            f"Current Balance : ₹{user['balance']}"
        )

    # ---------------------------------------------------
    # DEPOSIT MONEY
    # ---------------------------------------------------

    elif operation == "Deposit Money":

        st.subheader("💵 Deposit Money")

        amount = st.number_input(
            "Enter Amount",
            min_value=1.0
        )

        if st.button("Deposit"):

            success, msg = Bank.deposit_money(
                user,
                amount
            )

            if success:

                st.success(msg)

                st.rerun()

            else:
                st.error(msg)

    # ---------------------------------------------------
    # WITHDRAW MONEY
    # ---------------------------------------------------

    elif operation == "Withdraw Money":

        st.subheader("🏧 Withdraw Money")

        amount = st.number_input(
            "Enter Amount",
            min_value=1.0
        )

        if st.button("Withdraw"):

            success, msg = Bank.withdraw_money(
                user,
                amount
            )

            if success:

                st.success(msg)

                st.rerun()

            else:
                st.error(msg)

    # ---------------------------------------------------
    # UPDATE ACCOUNT
    # ---------------------------------------------------

    elif operation == "Update Account":

        st.subheader("✏️ Update Account")

        new_name = st.text_input(
            "Enter New Name",
            value=user["name"]
        )

        new_email = st.text_input(
            "Enter New Email",
            value=user["email"]
        )

        new_phone = st.text_input(
            "Enter New Phone Number",
            value=str(user["phone"])
        )

        new_pin = st.text_input(
            "Enter New 4 Digit PIN",
            value=str(user["pin"]),
            type="password"
        )

        if st.button("Update Account"):

            try:

                success, msg = Bank.update_account(
                    user=user,
                    name=new_name,
                    email=new_email,
                    phone=int(new_phone),
                    pin=int(new_pin)
                )

                if success:

                    st.success(msg)

                    st.rerun()

                else:
                    st.error(msg)

            except:
                st.error("❌ Invalid Details")

    # ---------------------------------------------------
    # DELETE ACCOUNT
    # ---------------------------------------------------

    elif operation == "Delete Account":

        st.subheader("🗑️ Delete Account")

        confirm = st.checkbox(
            "I confirm account deletion"
        )

        if confirm:

            if st.button("Delete Account"):

                success, msg = Bank.delete_account(
                    user
                )

                if success:

                    st.success(msg)

                    st.session_state.logged_in = False
                    st.session_state.user = None

                    st.rerun()

    # ---------------------------------------------------
    # LOGOUT
    # ---------------------------------------------------

    elif operation == "Logout":

        st.session_state.logged_in = False
        st.session_state.user = None

        st.success(
            "✅ Logged Out Successfully"
        )

        st.rerun()