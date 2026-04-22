import pandas as pd
import pytest
from src.metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


@pytest.fixture
def sample_df():
    # Sales: 2 leavers / 2 employees = 100%
    # HR:    0 leavers / 2 employees = 0%
    # IT:    1 leaver  / 2 employees = 50%
    # Yes overtime: 2 leavers / 3 employees = 66.67%
    # No overtime:  1 leaver  / 3 employees = 33.33%
    # Leavers avg income: (4000+6000+8000)/3 = 6000
    # Stayers avg income: (5000+7000+9000)/3 = 7000
    return pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5, 6],
            "department": ["Sales", "Sales", "HR", "HR", "IT", "IT"],
            "overtime": ["Yes", "Yes", "No", "Yes", "No", "No"],
            "monthly_income": [4000, 6000, 5000, 7000, 8000, 9000],
            "job_satisfaction": [1, 2, 1, 3, 2, 3],
            "attrition": ["Yes", "Yes", "No", "No", "Yes", "No"],
        }
    )


# --- attrition_rate ---

def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": ["Sales", "Sales", "HR", "HR"],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    assert attrition_rate(df) == 50.0


def test_attrition_rate_zero_percent():
    df = pd.DataFrame({"employee_id": [1, 2], "attrition": ["No", "No"]})
    assert attrition_rate(df) == 0.0


def test_attrition_rate_one_hundred_percent():
    df = pd.DataFrame({"employee_id": [1, 2], "attrition": ["Yes", "Yes"]})
    assert attrition_rate(df) == 100.0


def test_attrition_rate_rounds_to_two_decimals():
    df = pd.DataFrame({"employee_id": [1, 2, 3], "attrition": ["Yes", "No", "No"]})
    assert attrition_rate(df) == 33.33


# --- attrition_by_department ---

def test_attrition_by_department_returns_expected_columns(sample_df):
    result = attrition_by_department(sample_df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_values(sample_df):
    result = attrition_by_department(sample_df)

    sales = result[result["department"] == "Sales"].iloc[0]
    assert sales["employees"] == 2
    assert sales["leavers"] == 2
    assert sales["attrition_rate"] == 100.0

    hr = result[result["department"] == "HR"].iloc[0]
    assert hr["employees"] == 2
    assert hr["leavers"] == 0
    assert hr["attrition_rate"] == 0.0

    it = result[result["department"] == "IT"].iloc[0]
    assert it["employees"] == 2
    assert it["leavers"] == 1
    assert it["attrition_rate"] == 50.0


def test_attrition_by_department_sorted_descending(sample_df):
    result = attrition_by_department(sample_df)
    rates = list(result["attrition_rate"])
    assert rates == sorted(rates, reverse=True)


# --- attrition_by_overtime ---

def test_attrition_by_overtime_columns(sample_df):
    result = attrition_by_overtime(sample_df)
    assert list(result.columns) == ["overtime", "employees", "leavers", "attrition_rate"]


def test_attrition_by_overtime_values(sample_df):
    result = attrition_by_overtime(sample_df)

    yes = result[result["overtime"] == "Yes"].iloc[0]
    assert yes["employees"] == 3
    assert yes["leavers"] == 2
    assert yes["attrition_rate"] == 66.67

    no = result[result["overtime"] == "No"].iloc[0]
    assert no["employees"] == 3
    assert no["leavers"] == 1
    assert no["attrition_rate"] == 33.33


# --- average_income_by_attrition ---

def test_average_income_by_attrition_columns(sample_df):
    result = average_income_by_attrition(sample_df)
    assert list(result.columns) == ["attrition", "avg_monthly_income"]


def test_average_income_by_attrition_values(sample_df):
    result = average_income_by_attrition(sample_df)

    leavers = result[result["attrition"] == "Yes"].iloc[0]
    assert leavers["avg_monthly_income"] == 6000.0

    stayers = result[result["attrition"] == "No"].iloc[0]
    assert stayers["avg_monthly_income"] == 7000.0


# --- satisfaction_summary ---

def test_satisfaction_summary_columns(sample_df):
    result = satisfaction_summary(sample_df)
    assert list(result.columns) == ["job_satisfaction", "total_employees", "leavers", "attrition_rate"]


def test_satisfaction_summary_values(sample_df):
    result = satisfaction_summary(sample_df)

    row1 = result[result["job_satisfaction"] == 1].iloc[0]
    assert row1["total_employees"] == 2
    assert row1["leavers"] == 1
    assert row1["attrition_rate"] == 50.0

    row2 = result[result["job_satisfaction"] == 2].iloc[0]
    assert row2["total_employees"] == 2
    assert row2["leavers"] == 2
    assert row2["attrition_rate"] == 100.0

    row3 = result[result["job_satisfaction"] == 3].iloc[0]
    assert row3["total_employees"] == 2
    assert row3["leavers"] == 0
    assert row3["attrition_rate"] == 0.0


def test_satisfaction_summary_sorted_ascending(sample_df):
    result = satisfaction_summary(sample_df)
    scores = list(result["job_satisfaction"])
    assert scores == sorted(scores)
