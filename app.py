import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import (
    create_database,
    add_transaction,
    get_transactions,
    delete_transaction
)


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Smart Expense Manager",
    page_icon="💰",
    layout="wide"
)


# =====================================================
# CREATE DATABASE
# =====================================================

create_database()


# =====================================================
# TITLE
# =====================================================

st.title("💰 Smart Expense Manager")

st.write(
    "Track your income, expenses and financial activities easily."
)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📌 Menu")

menu = st.sidebar.radio(
    "Choose an option:",
    [
        "📊 Dashboard",
        "➕ Add Transaction",
        "📋 Transactions",
        "🗑️ Delete Transaction"
    ]
)


# =====================================================
# LOAD TRANSACTIONS
# =====================================================

df = get_transactions()


# =====================================================
# DASHBOARD
# =====================================================

if menu == "📊 Dashboard":

    st.header("📊 Financial Dashboard")

    if df.empty:

        st.info(
            "No transactions available. "
            "Please add your first transaction."
        )

    else:

        # ---------------------------------------------
        # CALCULATE INCOME
        # ---------------------------------------------

        total_income = df[
            df["transaction_type"] == "Income"
        ]["amount"].sum()


        # ---------------------------------------------
        # CALCULATE EXPENSE
        # ---------------------------------------------

        total_expense = df[
            df["transaction_type"] == "Expense"
        ]["amount"].sum()


        # ---------------------------------------------
        # CALCULATE BALANCE
        # ---------------------------------------------

        balance = total_income - total_expense


        # ---------------------------------------------
        # DISPLAY METRICS
        # ---------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💵 Total Income",
                f"₹{total_income:,.2f}"
            )

        with col2:
            st.metric(
                "💸 Total Expense",
                f"₹{total_expense:,.2f}"
            )

        with col3:
            st.metric(
                "💰 Balance",
                f"₹{balance:,.2f}"
            )


        st.divider()


        # =================================================
        # EXPENSE ANALYSIS
        # =================================================

        expense_df = df[
            df["transaction_type"] == "Expense"
        ]


        if not expense_df.empty:

            # ---------------------------------------------
            # CATEGORY DATA
            # ---------------------------------------------

            category_data = (
                expense_df
                .groupby("category")["amount"]
                .sum()
                .reset_index()
            )


            col1, col2 = st.columns(2)


            # ---------------------------------------------
            # PIE CHART
            # ---------------------------------------------

            with col1:

                st.subheader("🍕 Expense Distribution")

                pie_chart = px.pie(
                    category_data,
                    names="category",
                    values="amount",
                    hole=0.4
                )

                st.plotly_chart(
                    pie_chart,
                    use_container_width=True
                )


            # ---------------------------------------------
            # BAR CHART
            # ---------------------------------------------

            with col2:

                st.subheader("📊 Category-wise Spending")

                bar_chart = px.bar(
                    category_data,
                    x="category",
                    y="amount",
                    text_auto=True
                )

                st.plotly_chart(
                    bar_chart,
                    use_container_width=True
                )


# =====================================================
# ADD TRANSACTION
# =====================================================

elif menu == "➕ Add Transaction":

    st.header("➕ Add New Transaction")


    # ---------------------------------------------
    # TRANSACTION TYPE
    # ---------------------------------------------

    transaction_type = st.selectbox(
        "Transaction Type",
        [
            "Expense",
            "Income"
        ]
    )


    # ---------------------------------------------
    # DATE
    # ---------------------------------------------

    transaction_date = st.date_input(
        "Date",
        value=date.today()
    )


    # ---------------------------------------------
    # CATEGORY
    # ---------------------------------------------

    if transaction_type == "Expense":

        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Bills",
                "Entertainment",
                "Health",
                "Rent",
                "Other"
            ]
        )

    else:

        category = st.selectbox(
            "Income Category",
            [
                "Salary",
                "Freelance",
                "Business",
                "Investment",
                "Other"
            ]
        )


    # ---------------------------------------------
    # AMOUNT
    # ---------------------------------------------

    amount = st.number_input(
        "Amount (₹)",
        min_value=1.0,
        step=100.0
    )


    # ---------------------------------------------
    # DESCRIPTION
    # ---------------------------------------------

    description = st.text_input(
        "Description",
        placeholder="Example: Grocery shopping"
    )


    # ---------------------------------------------
    # SAVE BUTTON
    # ---------------------------------------------

    if st.button(
        "💾 Save Transaction",
        use_container_width=True
    ):

        add_transaction(
            str(transaction_date),
            transaction_type,
            category,
            amount,
            description
        )

        st.success(
            "Transaction added successfully! ✅"
        )

        st.balloons()


# =====================================================
# VIEW TRANSACTIONS
# =====================================================

elif menu == "📋 Transactions":

    st.header("📋 All Transactions")

    df = get_transactions()


    if df.empty:

        st.info("No transactions found.")

    else:

        # ---------------------------------------------
        # SEARCH
        # ---------------------------------------------

        search = st.text_input(
            "🔍 Search transaction"
        )


        if search:

            search = search.lower()

            filtered_df = df[
                df.astype(str)
                .apply(
                    lambda row:
                    row.str.lower()
                    .str.contains(search)
                    .any(),
                    axis=1
                )
            ]

        else:

            filtered_df = df


        # ---------------------------------------------
        # DISPLAY DATA
        # ---------------------------------------------

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )


        # ---------------------------------------------
        # DOWNLOAD CSV
        # ---------------------------------------------

        csv_data = filtered_df.to_csv(
            index=False
        )

        st.download_button(
            "📥 Download CSV",
            csv_data,
            "transactions.csv",
            "text/csv"
        )


# =====================================================
# DELETE TRANSACTION
# =====================================================

elif menu == "🗑️ Delete Transaction":

    st.header("🗑️ Delete Transaction")

    df = get_transactions()


    if df.empty:

        st.info("No transactions available.")

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


        transaction_id = st.number_input(
            "Enter Transaction ID to delete",
            min_value=1,
            step=1
        )


        if st.button(
            "🗑️ Delete Transaction",
            use_container_width=True
        ):

            delete_transaction(
                transaction_id
            )

            st.success(
                "Transaction deleted successfully! ✅"
            )

            st.rerun()