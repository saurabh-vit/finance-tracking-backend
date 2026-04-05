"""
Summary / analytics router.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from finance_system.dependencies import get_db, get_current_user, require_role
from finance_system.models.transaction import Transaction
from finance_system.models.user import User
from finance_system.schemas.transaction import (
    TransactionResponse,
    OverviewResponse,
    ByCategoryResponse,
    MonthlyResponse,
)
from finance_system.services import summary_service

router = APIRouter(prefix="/summary", tags=["Summary"])


def _is_admin(user: User) -> bool:
    return user.role == "admin"


@router.get(
    "/overview",
    response_model=OverviewResponse,
    summary="Financial overview (total income, expense, balance)",
)
def overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer", "analyst", "admin")),
) -> OverviewResponse:
    """
    Returns total income, total expense, balance, and transaction count.

    - **Admins** see aggregate across all users.
    - **Others** see their own data only.
    """
    return summary_service.get_overview(db, current_user.id, _is_admin(current_user))


@router.get(
    "/by-category",
    response_model=ByCategoryResponse,
    summary="Spending / income breakdown by category (analyst, admin)",
)
def by_category(
    type: Optional[str] = Query(None, description="Filter by 'income' or 'expense'"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("analyst", "admin")),
) -> ByCategoryResponse:
    """
    Returns per-category totals and counts, optionally filtered by transaction type.

    **Requires analyst or admin role.**
    """
    return summary_service.get_by_category(
        db, current_user.id, _is_admin(current_user), type
    )


@router.get(
    "/monthly",
    response_model=MonthlyResponse,
    summary="Month-by-month breakdown for a given year (analyst, admin)",
)
def monthly(
    year: int = Query(
        default_factory=lambda: datetime.now(timezone.utc).year,
        description="Year to analyse (defaults to current year)",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("analyst", "admin")),
) -> MonthlyResponse:
    """
    Returns income, expense, and net for every month in *year*.

    **Requires analyst or admin role.**
    """
    return summary_service.get_monthly(db, current_user.id, _is_admin(current_user), year)


@router.get(
    "/recent",
    response_model=list[TransactionResponse],
    summary="Most recent transactions",
)
def recent(
    limit: int = Query(5, ge=1, le=20, description="Number of transactions to return (max 20)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer", "analyst", "admin")),
) -> list[Transaction]:
    """
    Return the *limit* most recent transactions sorted by date descending.

    - **Admins** see all users' transactions.
    - **Others** see only their own.
    """
    query = db.query(Transaction)
    if not _is_admin(current_user):
        query = query.filter(Transaction.user_id == current_user.id)

    return (
        query.order_by(Transaction.date.desc(), Transaction.id.desc())
        .limit(limit)
        .all()
    )
