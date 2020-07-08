from bank_api.bank import Bank


class BankReport:


    def __init__(self, bank: Bank):
        self._bank = bank


    def get_balance(self, name: str) -> int:
        account = self._bank.get_account(name)
        balance = sum(t.amount for t in self._bank.transactions if t.account == account)
        return balance
