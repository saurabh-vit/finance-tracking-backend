"""
Transactions router: full CRUD + filtered listing with pagination.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user, require_role
from models.transaction import Transaction
from models.user import User
from schemas.transaction import (
    PaginatedTransactions,
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _get_transaction_or_404(transaction_id: int, db: Session) -> Transaction:
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id={transaction_id} not found.",
        )
    return txn


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=PaginatedTransactions,
    summary="List transactions (paginated, filterable)",
)
def list_transactions(
    type: Optional[str] = Query(None, description="Filter by type: 'income' or 'expense'"),
    category: Optional[str] = Query(None, description="Filter by category (case-insensitive)"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Records per page (max 100)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer", "analyst", "admin")),
) -> PaginatedTransactions:
    """
    Retrieve a paginated, optionally filtered list of transactions.

    - **Admins** see all users' transactions.
    - **Others** see only their own.
    """
    if type and type not in ("income", "expense"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="type must be 'income' or 'expense'.",
        )

    query = db.query(Transaction)

    # Scope: admins see everything, others see their own
    if current_user.role != "admin":
        query = query.filter(Transaction.user_id == current_user.id)

    if type:
        query = query.filter(Transaction.type == type)
    if category:
        query = query.filter(Transaction.category.ilike(f"%{category.strip()}%"))
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    total = query.count()
    data = (
        query.order_by(Transaction.date.desc(), Transaction.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedTransactions(total=total, page=page, page_size=page_size, data=data)


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new transaction (admin only)",
)
def create_transaction(
    txn_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Transaction:
    """
    Create a new transaction record.  **Admin role required.**
    """
    new_txn = Transaction(
        user_id=current_user.id,
        amount=txn_in.amount,
        type=txn_in.type,
        category=txn_in.category.strip(),
        date=txn_in.date,
        notes=txn_in.notes,
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Get a single transaction",
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer", "analyst", "admin")),
) -> Transaction:
    """
    Retrieve one transaction by ID.

    - **Admins** can access any transaction.
    - **Others** can only access their own transactions.
    """
    txn = _get_transaction_or_404(transaction_id, db)

    if current_user.role != "admin" and txn.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this transaction.",
        )
    return txn


@router.put(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Update a transaction (admin only)",
)
def update_transaction(
    transaction_id: int,
    txn_in: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),  # noqa: ARG001
) -> Transaction:
    """
    Partially update an existing transaction.  **Admin role required.**
    """
    txn = _get_transaction_or_404(transaction_id, db)

    update_data = txn_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if isinstance(value, str) and field == "category":
            value = value.strip()
        setattr(txn, field, value)

    db.commit()
    db.refresh(txn)
    return txn


@router.delete(
    "/{transaction_id}",
    summary="Delete a transaction (admin only)",
)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),  # noqa: ARG001
) -> dict:
    """
    Delete a transaction by ID.  **Admin role required.**
    """
    txn = _get_transaction_or_404(transaction_id, db)
    db.delete(txn)
    db.commit()
    return {"detail": "Transaction deleted successfully"}
