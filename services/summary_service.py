"""
Summary / analytics service.
All heavy query logic lives here; routers stay thin.
"""

from calendar import month_name
from typing import Optional

from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from models.transaction import Transaction


def get_overview(db: Session, user_id: int, is_admin: bool) -> dict:
    """
    Return total_income, total_expense, balance, and transaction_count.
    Admins see all records; regular users see only their own.
    """
    query = db.query(Transaction)
    if not is_admin:
        query = query.filter(Transaction.user_id == user_id)

    income_row = (
        query.filter(Transaction.type == "income")
        .with_entities(func.coalesce(func.sum(Transaction.amount), 0.0))
        .scalar()
    )
    expense_row = (
        query.filter(Transaction.type == "expense")
        .with_entities(func.coalesce(func.sum(Transaction.amount), 0.0))
        .scalar()
    )
    count = query.count()

    total_income = float(income_row or 0.0)
    total_expense = float(expense_row or 0.0)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": round(total_income - total_expense, 2),
        "transaction_count": count,
    }


def get_by_category(
    db: Session,
    user_id: int,
    is_admin: bool,
    type_filter: Optional[str] = None,
) -> dict:
    """
    Return per-category totals and counts.
    Optionally filtered by transaction type ("income" | "expense").
    """
    query = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count"),
    )
    if not is_admin:
        query = query.filter(Transaction.user_id == user_id)
    if type_filter:
        query = query.filter(Transaction.type == type_filter)

    rows = query.group_by(Transaction.category).order_by(func.sum(Transaction.amount).desc()).all()

    categories = [
        {"category": row.category, "total": round(float(row.total), 2), "count": row.count}
        for row in rows
    ]
    return {"categories": categories}


def get_monthly(
    db: Session,
    user_id: int,
    is_admin: bool,
    year: int,
) -> dict:
    """
    Return month-by-month income, expense, and net for the given *year*.
    """
    query = db.query(
        extract("month", Transaction.date).label("month_num"),
        Transaction.type,
        func.sum(Transaction.amount).label("total"),
    )
    if not is_admin:
        query = query.filter(Transaction.user_id == user_id)

    rows = (
        query.filter(extract("year", Transaction.date) == year)
        .group_by("month_num", Transaction.type)
        .all()
    )

    # Build a full 12-month structure, filling zeros where no data exists
    monthly_map: dict[int, dict[str, float]] = {
        m: {"income": 0.0, "expense": 0.0} for m in range(1, 13)
    }
    for row in rows:
        m = int(row.month_num)
        if row.type in ("income", "expense"):
            monthly_map[m][row.type] += float(row.total)

    monthly = [
        {
            "month": month_name[m],
            "income": round(monthly_map[m]["income"], 2),
            "expense": round(monthly_map[m]["expense"], 2),
            "net": round(monthly_map[m]["income"] - monthly_map[m]["expense"], 2),
        }
        for m in range(1, 13)
    ]

    return {"year": year, "monthly": monthly}
