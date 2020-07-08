from dataclasses import dataclass
from datetime import datetime
from typing import Set


@dataclass(frozen=True)
class Account:
    name: str


@dataclass(frozen=True)
class Transaction:
    account: Account
    date: datetime
    amount: int


class Bank:
    def __init__(self):
        self._accounts: Set[Account] = set()
        self._transactions: Set[Transaction] = set()

    @property
    def accounts(self) -> Set[Account]:
        """Get a copy of the bank's accounts"""
        return self._accounts.copy()

    @property
    def transactions(self) -> Set[Transaction]:
        """Get a copy of the bank's transactions"""
        return self._transactions.copy()

    def create_account(self, name: str) -> Account:
        """Creates a new account with the name provided"""
        account = Account(name)
        self._accounts.add(account)
        return account

    def get_account(self, name: str) -> Account:
        """Gets the named account, if it exists"""
        for account in self.accounts:
            if account.name == name:
                return account
        raise ValueError('Account not found')

    def add_funds(self, name: str, amount: int) -> None:
        """Add funds to the named account"""
        if not isinstance(amount, int):
            raise TypeError('Amount must be an integer')
        account = self.get_account(name)
        now = datetime.now()
        self._transactions.add(Transaction(account, now, amount))

    def move_funds(self, nameFrom: str, nameTo: str, amount: int) -> None:
        """Move funds from the named account to the named account"""
        if not isinstance(amount, int):
            raise TypeError('Amount must be an integer')
        account_from = self.get_account(nameFrom)
        account_to = self.get_account(nameTo)
        now = datetime.now()
        self._transactions.add(Transaction(account_from, now, -amount))
        self._transactions.add(Transaction(account_to, now, amount))
