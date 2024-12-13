# import json
# import time
# from datetime import date, timedelta
# from typing import Self, Annotated
# from uuid import UUID, uuid4
# from enum import Enum
# from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, PositiveFloat, validate_call, HttpUrl
#
#
# class Department(Enum):
#     HR = "HR"
#     SALES = "SALES"
#     IT = "IT"
#     ENGINEERING = "ENGINEERING"
#
#
# class Employee(BaseModel):
#     employee_id: UUID = Field(default_factory=uuid4, frozen=True)
#     name: str = Field(min_length=1, frozen=True)
#     email: EmailStr = Field(pattern=r".+@example\.com$")
#     date_of_birth: date = Field(alias="birth_day", repr=False, frozen=True)
#     salary: float = Field(alias="compensations", gt=0, repr=False)
#     department: Department
#     elected_benefits: bool
#
#
#     @field_validator('date_of_birth')
#     @classmethod
#     def check_valid_age(cls, date_of_birth: date) -> date:
#         today = date.today()
#         eighteen_years_ago = date(today.year - 18, today.month, today.day)
#         if date_of_birth > eighteen_years_ago:
#             raise ValueError("Employee to young")
#         return date_of_birth
#
#     @model_validator(mode="after")
#     def check_it_benefits(self) -> Self:
#         department = self.department
#         elected_benefits = self.elected_benefits
#
#         if department == Department.IT and elected_benefits is True:
#             raise ValueError("IT tolko vkatyn")
#         return self
#
#
#
#
# criss = Employee(
#     name="Chris DeTuma",
#     email="cdetuma@example.com",
#     birth_day=date.today() - timedelta(days=365 * 19),
#     compensations=123_000.00,
#     department="IT",
#     elected_benefits=False,
# )
#
#
# @validate_call
# def send_invoice(
#         client_name: Annotated[str, Field(min_length=1)],
#         client_email: EmailStr,
#         items_purchased: list[str],
#         amount_owed: PositiveFloat
# ) -> str:
#     email_str = f"""
#     Dear {client_name}, \n
#     Thank you for choosing xyz inc! You
#     owe ${amount_owed:,.2f} for the following items: \n
#     {items_purchased}
#     """
#     print(f"Sending email to {client_email}...")
#     time.sleep(2)
#     return email_str
#
#
# arr = send_invoice("i", "gora228@mail.ru", ['arcane', 'vaifu'], 1_000_000)
#
#
# new_employee_dict = {
#     "name": "Chris DeTuma",
#     "email": "cdetuma@example.com",
#     "birth_day": "1998-04-02",
#     "compensations": 123_000.00,
#     "department": "IT",
#     "elected_benefits": False,
# }
#
#
# b = Employee.model_validate(new_employee_dict)
# dump = b.model_dump()
# dump_j = b.model_dump_json()
# dump_s = b.model_json_schema()
# aa = json.dumps(dump_s)
# a = 9
#
#

