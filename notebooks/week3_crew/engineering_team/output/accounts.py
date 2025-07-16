class Account:
    """
    This class provides an account management system for a trading simulation platform.
    """

    def __init__(self, username: str):
        self.username = username
        self.balance = 0.0
        self.portfolio = {}
        self.transactions = []
        self.initial_deposit = 0.0

    def deposit_funds(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
            if self.initial_deposit == 0.0:
                self.initial_deposit = self.balance
            self.transactions.append({'type': 'deposit', 'amount': amount})

    def withdraw_funds(self, amount: float) -> bool:
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append({'type': 'withdrawal', 'amount': amount})
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost <= self.balance and quantity > 0:
            self.balance -= total_cost
            if symbol in self.portfolio:
                self.portfolio[symbol] += quantity
            else:
                self.portfolio[symbol] = quantity
            self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'price': price})
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.portfolio and 0 < quantity <= self.portfolio[symbol]:
            price = get_share_price(symbol)
            total_revenue = price * quantity
            self.portfolio[symbol] -= quantity
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]
            self.balance += total_revenue
            self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity, 'price': price})
            return True
        return False

    def calculate_portfolio_value(self) -> float:
        total_value = 0.0
        for symbol, quantity in self.portfolio.items():
            price = get_share_price(symbol)
            total_value += price * quantity
        return total_value

    def calculate_profit_or_loss(self) -> float:
        current_value = self.calculate_portfolio_value() + self.balance
        return current_value - self.initial_deposit

    def report_holdings(self) -> dict:
        return self.portfolio.copy()

    def report_transactions(self) -> list:
        return self.transactions.copy()

def get_share_price(symbol: str) -> float:
    """
    Mock function to get the current price of a share.
    Returns fixed prices for specific symbols.

    :param symbol: The symbol of the share.
    :return: The current price of the share.
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, -1.0)  # Return -1.0 if the symbol is not recognized