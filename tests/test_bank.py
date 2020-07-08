"""Unit tests for bank.py"""

import pytest

from bank_api.bank import Bank, Account


@pytest.fixture
def bank() -> Bank:
    return Bank()


def test_accounts_are_immutable():
    account = Account('Immutable')
    with pytest.raises(Exception):
        # This operation should raise an exception
        account.name = 'Mutable'


def test_bank_creates_empty(bank):
    assert len(bank.accounts) == 0
    assert len(bank.transactions) == 0


def test_can_create_and_get_account(bank):
    bank.create_account('Test')
    account = bank.get_account('Test')

    assert len(bank.accounts) == 1
    assert account.name == 'Test'


def test_cannot_duplicate_accounts(bank):
    bank.create_account('duplicate')
    bank.create_account('duplicate')

    assert len(bank.accounts) == 1


def test_cannot_modify_accounts_set(bank):
    accounts = bank.accounts
    accounts.add(Account('New Account'))

    assert len(bank.accounts) == 0


def test_can_add_some_funds_to_account(bank):
    bank.create_account('New Account')
    bank.add_funds('New Account', 123)

    assert len(bank.transactions) == 1
    assert bank.transactions.pop().amount == 123
    assert bank.transactions.pop().account.name == 'New Account'


def test_can_add_no_funds_to_account(bank):
    bank.create_account('New Account')
    bank.add_funds('New Account', 0)

    assert len(bank.transactions) == 1
    assert bank.transactions.pop().amount == 0
    assert bank.transactions.pop().account.name == 'New Account'


def test_cannot_add_not_int_funds_to_account(bank):
    bank.create_account('New Account')
    with pytest.raises(TypeError):
        # This operation should raise a TypeError
        bank.add_funds('New Account', 'string')


def test_cannot_add_funds_to_non_existent_account(bank):
    bank.create_account('New Account')
    with pytest.raises(ValueError):
        # This operation should raise a ValueError
        bank.add_funds('Invalid Account Name', 123)


def test_can_move_some_funds_to_account(bank):
    bank.create_account('From Account')
    bank.add_funds('From Account', 123)
    bank.create_account('To Account')
    bank.move_funds('From Account', 'To Account', 1)

    transactions_from = [t for t in bank.transactions if t.account.name == 'From Account']
    transactions_to = [t for t in bank.transactions if t.account.name == 'To Account']

    assert len(transactions_from) == 2
    assert len(transactions_to) == 1
    assert transactions_from.pop().amount == -1
    assert transactions_from.pop().amount == 123
    assert transactions_to.pop().amount == 1


def test_can_move_no_funds_to_account(bank):
    bank.create_account('From Account')
    bank.create_account('To Account')
    bank.move_funds('From Account', 'To Account', 0)

    transactions_from = [t for t in bank.transactions if t.account.name == 'From Account']
    transactions_to = [t for t in bank.transactions if t.account.name == 'To Account']

    assert len(transactions_from) == 1
    assert len(transactions_to) == 1
    assert transactions_from.pop().amount == 0
    assert transactions_to.pop().amount == 0


def test_cannot_move_not_int_funds_to_account(bank):
    bank.create_account('From Account')
    bank.create_account('To Account')
    with pytest.raises(TypeError):
        # This operation should raise a TypeError
        bank.move_funds('From Account', 'To Account', 'string')


def test_cannot_move_funds_from_non_existent_account(bank):
    bank.create_account('From Account')
    bank.create_account('To Account')
    with pytest.raises(ValueError):
        # This operation should raise a ValueError
        bank.move_funds('Invalid Account Name', 'To Account', 123)


def test_cannot_move_funds_to_non_existent_account(bank):
    bank.create_account('From Account')
    bank.create_account('To Account')
    with pytest.raises(ValueError):
        # This operation should raise a ValueError
        bank.move_funds('From Account', 'Invalid Account Name', 123)