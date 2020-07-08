"""Unit tests for bank_report.py"""

import pytest

from bank_api.bank import Bank, Account
from bank_api.bank_report import BankReport


@pytest.fixture
def bank() -> Bank:
    return Bank()


def test_get_balance_for_account(bank):
    bank.create_account('Test')
    bank.add_funds('Test', 123)
    bank.add_funds('Test', 234)
    bank_report = BankReport(bank)
        
    assert bank_report.get_balance('Test') == 357


def test_get_balance_for_empty_account(bank):
    bank.create_account('EmptyAccount')
    bank_report = BankReport(bank)
        
    assert bank_report.get_balance('EmptyAccount') == 0


def test_get_balance_for_negative_account(bank):
    bank.create_account('NegativeAccount')
    bank.add_funds('NegativeAccount', -123)
    bank.add_funds('NegativeAccount', -234)
    bank_report = BankReport(bank)
        
    assert bank_report.get_balance('NegativeAccount') == -357


def test_get_balance_for_non_existant_account_errors(bank):
    bank_report = BankReport(bank)
    with pytest.raises(ValueError):
        bank_report.get_balance('NonExistant')