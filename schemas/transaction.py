"""
Pydantic schemas for Transaction requests and responses.
"""

from datetime import date, datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, field_validator, ConfigDict


class TransactionCreate(BaseModel):
    amount: float
    type: Literal["income", "expense"]
    category: str
    date: date
    notes: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0.")
        return v

    @field_validator("category")
    @classmethod
    def category_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Category must not be empty.")
        return v

    @field_validator("date")
    @classmethod
    def date_not_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Transaction date cannot be in the future.")
        return v


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Amount must be greater than 0.")
        return v

    @field_validator("category")
    @classmethod
    def category_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Category must not be empty.")
        return v

    @field_validator("date")
    @classmethod
    def date_not_future(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v > date.today():
            raise ValueError("Transaction date cannot be in the future.")
        return v


class TransactionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "amount": 50000.0,
                "type": "income",
                "category": "salary",
                "date": "2025-03-01",
                "notes": "March salary",
                "created_at": "2025-03-01T10:00:00"
            }
        }
    )

    id: int
    user_id: int
    amount: float
    type: str
    category: str
    date: date
    notes: Optional[str]
    created_at: datetime


class PaginatedTransactions(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[TransactionResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 15,
                "page": 1,
                "page_size": 10,
                "data": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "amount": 50000.0,
                        "type": "income",
                        "category": "salary",
                        "date": "2025-03-01",
                        "notes": "March salary",
                        "created_at": "2025-03-01T10:00:00"
                    }
                ]
            }
        }
    )


# Summary response schemas
class OverviewResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float
    transaction_count: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_income": 222000.0,
                "total_expense": 43200.0,
                "balance": 178800.0,
                "transaction_count": 15
            }
        }
    )


class CategorySummary(BaseModel):
    category: str
    total: float
    count: int


class ByCategoryResponse(BaseModel):
    categories: List[CategorySummary]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "categories": [
                    {"category": "salary", "total": 150000.0, "count": 3},
                    {"category": "rent", "total": 25500.0, "count": 3},
                    {"category": "food", "total": 9200.0, "count": 3}
                ]
            }
        }
    )


class MonthlyData(BaseModel):
    month: str
    income: float
    expense: float
    net: float


class MonthlyResponse(BaseModel):
    year: int
    monthly: List[MonthlyData]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "year": 2025,
                "monthly": [
                    {"month": "January", "income": 65000.0, "expense": 12700.0, "net": 52300.0},
                    {"month": "February", "income": 50000.0, "expense": 11400.0, "net": 38600.0},
                    {"month": "March", "income": 62000.0, "expense": 11600.0, "net": 50400.0}
                ]
            }
        }
    )


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
                "app": "Finance Tracking System",
                "version": "1.0.0"
            }
        }
    )
