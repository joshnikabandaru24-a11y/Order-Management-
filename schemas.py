from pydantic import BaseModel


# VERIFY
class VerifyRequest(BaseModel):
    order_id: int
    postal_code: str


# MODIFY
class ModifyRequest(BaseModel):
    order_id: int
    new_item: str


# RETURN
class ReturnRequest(BaseModel):
    order_id: int
    reason: str


# REPORT ISSUE
class IssueRequest(BaseModel):
    order_id: int
    issue_type: str
    description: str