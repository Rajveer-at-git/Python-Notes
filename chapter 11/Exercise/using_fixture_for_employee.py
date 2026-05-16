import pytest
from employee import Employee

@pytest.fixture
def emp_details():
    emp_details = Employee("Rajveer","Choudhary", 100000)
    return emp_details

def test_give_default_raise(emp_details):
    emp_details.give_raise()
    assert emp_details.annual_salary == 105000

def test_give_custom_raise(emp_details):
    emp_details.give_raise(10000)
    assert emp_details.annual_salary == 110000