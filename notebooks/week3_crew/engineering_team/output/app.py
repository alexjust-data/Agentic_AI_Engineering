
import gradio as gr
from accounts import Account

# Create an instance of the Account class
account = Account(username="test_user")

# Define functions for each tab
def create_account(username):
    global account
    account = Account(username=username)
    return f"Account for {username} created successfully!"

def deposit(amount):
    account.deposit_funds(amount)
    return f"Deposited ${amount:.2f}. Current balance: ${account.balance:.2f}"

def withdraw(amount):
    success = account.withdraw_funds(amount)
    if success:
        return f"Withdrew ${amount:.2f}. Current balance: ${account.balance:.2f}"
    else:
        return "Withdrawal failed due to insufficient balance."

def buy_stock(symbol, quantity):
    success = account.buy_shares(symbol, quantity)
    if success:
        return f"Purchased {quantity} shares of {symbol}. Current balance: ${account.balance:.2f}"
    else:
        return "Purchase failed due to insufficient balance or invalid quantity."

def sell_stock(symbol, quantity):
    success = account.sell_shares(symbol, quantity)
    if success:
        return f"Sold {quantity} shares of {symbol}. Current balance: ${account.balance:.2f}"
    else:
        return "Sell failed due to invalid quantity or holdings."

def view_balance():
    return f"Current balance: ${account.balance:.2f}"

def view_holdings():
    return account.report_holdings()

def view_transactions():
    return account.report_transactions()

# Set up Gradio UI
with gr.Blocks() as app:
    with gr.Tab("Account"):
        username_input = gr.Textbox(label="Username")
        create_account_btn = gr.Button("Create Account")
        create_account_btn.click(create_account, inputs=username_input, outputs=gr.Textbox())

        deposit_amount = gr.Number(label="Amount to Deposit")
        deposit_btn = gr.Button("Deposit")
        deposit_btn.click(deposit, inputs=deposit_amount, outputs=gr.Textbox())

        withdraw_amount = gr.Number(label="Amount to Withdraw")
        withdraw_btn = gr.Button("Withdraw")
        withdraw_btn.click(withdraw, inputs=withdraw_amount, outputs=gr.Textbox())

    with gr.Tab("Trading"):
        stock_symbol = gr.Dropdown(['AAPL', 'TSLA', 'GOOGL'], label="Stock Symbol")
        quantity = gr.Number(label="Quantity")

        buy_btn = gr.Button("Buy")
        buy_btn.click(buy_stock, inputs=[stock_symbol, quantity], outputs=gr.Textbox())

        sell_btn = gr.Button("Sell")
        sell_btn.click(sell_stock, inputs=[stock_symbol, quantity], outputs=gr.Textbox())

    with gr.Tab("Reports"):
        view_balance_btn = gr.Button("View Balance")
        view_balance_btn.click(view_balance, outputs=gr.Textbox())

        view_holdings_btn = gr.Button("View Holdings")
        view_holdings_btn.click(view_holdings, outputs=gr.Dataframe())

        view_transactions_btn = gr.Button("View Transaction History")
        view_transactions_btn.click(view_transactions, outputs=gr.Dataframe())

app.launch()