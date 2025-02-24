from pydantic import BaseModel


class Dealer(BaseModel):
    name: str
    address: str


class Customer(BaseModel):
    name: str
    address: str
    email: str | None
    phone_number: str | None


class Car(BaseModel):
    model: str
    plate: str | None


class WorkOrder(BaseModel):
    id: str
    total_amount: float
    date: str
    dealer: Dealer
    customer: Customer
    car: Car
