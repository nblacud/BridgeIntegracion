"""
Pydantic models for Bridge API data structures
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator

class CustomerType(str, Enum):
    INDIVIDUAL = "individual"
    BUSINESS = "business"

class KYCStatus(str, Enum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    REJECTED = "rejected"
    PENDING = "pending"

class PaymentRail(str, Enum):
    ACH = "ach"
    WIRE = "wire"
    POLYGON = "polygon"
    ETHEREUM = "ethereum"
    ARBITRUM = "arbitrum"
    BASE = "base"
    SOLANA = "solana"

class Currency(str, Enum):
    USD = "usd"
    USDC = "usdc"
    USDT = "usdt"

class TransferStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Address(BaseModel):
    """Address model"""
    street_line_1: str
    street_line_2: Optional[str] = None
    city: str
    subdivision: Optional[str] = None  # state/province
    postal_code: str
    country: str

class IdentifyingInformation(BaseModel):
    """Identifying information for KYC"""
    type: str  # ssn, passport, drivers_license, etc.
    issuing_country: str
    number: str
    image_front: Optional[str] = None  # base64 encoded image
    image_back: Optional[str] = None   # base64 encoded image

class Document(BaseModel):
    """Document for KYC"""
    purposes: List[str]
    file: str  # base64 encoded file

class CustomerRequest(BaseModel):
    """Request model for creating a customer"""
    type: CustomerType
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    residential_address: Address
    birth_date: str  # YYYY-MM-DD format
    signed_agreement_id: str
    identifying_information: List[IdentifyingInformation]
    documents: Optional[List[Document]] = None
    
    # Additional fields for international customers
    employment_status: Optional[str] = None
    expected_monthly_payments: Optional[str] = None
    acting_as_intermediary: Optional[str] = None
    most_recent_occupation: Optional[str] = None
    account_purpose: Optional[str] = None
    account_purpose_other: Optional[str] = None
    source_of_funds: Optional[str] = None

class Customer(BaseModel):
    """Customer model"""
    id: str
    type: CustomerType
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    residential_address: Address
    birth_date: str
    status: KYCStatus
    created_at: datetime
    updated_at: datetime

class ExternalAccountRequest(BaseModel):
    """Request model for creating external account"""
    currency: Currency
    account_type: str  # us, international, etc.
    bank_name: str
    account_name: str
    first_name: str
    last_name: str
    account_owner_type: str  # individual, business
    account_owner_name: str
    account: Dict[str, Any]  # Account details (routing, account number, etc.)
    address: Address

class ExternalAccount(BaseModel):
    """External account model"""
    id: str
    customer_id: str
    created_at: datetime
    updated_at: datetime
    bank_name: str
    account_name: str
    account_owner_name: str
    active: bool
    currency: Currency
    account_owner_type: str
    account_type: str
    first_name: str
    last_name: str
    account: Dict[str, Any]
    last_4: str

class TransferSource(BaseModel):
    """Transfer source"""
    payment_rail: PaymentRail
    currency: Currency
    from_address: Optional[str] = None
    external_account_id: Optional[str] = None

class TransferDestination(BaseModel):
    """Transfer destination"""
    payment_rail: PaymentRail
    currency: Currency
    to_address: Optional[str] = None
    external_account_id: Optional[str] = None

class TransferRequest(BaseModel):
    """Request model for creating transfer"""
    amount: str
    on_behalf_of: str  # customer ID
    source: TransferSource
    destination: TransferDestination

class Transfer(BaseModel):
    """Transfer model"""
    id: str
    amount: str
    status: TransferStatus
    on_behalf_of: str
    source: TransferSource
    destination: TransferDestination
    created_at: datetime
    updated_at: datetime

class Wallet(BaseModel):
    """Wallet model"""
    id: str
    customer_id: str
    currency: Currency
    balance: str
    address: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class TOSLinkResponse(BaseModel):
    """Terms of Service link response"""
    url: str
