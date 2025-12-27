from locale import currency
from pydantic import BaseModel, Field
from typing import Optional

class ExpenseDataModal(BaseModel):
    amount: Optional[str] = Field(title="expenseAmount", description="Amount of the expense")
    merchant: Optional[str] = Field(title="merchantName", description="Merchant name to whom the expense is made")
    currency: Optional[str] = Field(title="currency", description="Currency of the transaction")
    