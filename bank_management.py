import json
import random
import string
from pathlib import Path


class Bank:

    database = "bankData.json"

    # LOAD DATABASE

    if Path(database).exists():

        with open(database, "r") as fs:

            try:
                data = json.load(fs)

            except:
                data = []

    else:
        data = []

    # SAVE DATABASE

    @classmethod
    def save_data(cls):

        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    # GENERATE ACCOUNT NUMBER

    @staticmethod
    def generate_account_number():

        letters = ''.join(
            random.choices(string.ascii_uppercase, k=4)
        )

        numbers = ''.join(
            random.choices(string.digits, k=4)
        )

        symbol = random.choice("@#$%&")

        account_number = list(
            letters + numbers + symbol
        )

        random.shuffle(account_number)

        return ''.join(account_number)

    # CREATE ACCOUNT

    @classmethod
    def create_account(
        cls,
        name,
        email,
        pin,
        age,
        phone
    ):

        # VALIDATIONS

        if age < 18:
            return False, "User must be 18+"

        if len(str(phone)) != 10:
            return False, "Phone number must be 10 digits"

        if len(str(pin)) != 4:
            return False, "PIN must be 4 digits"

        # CHECK DUPLICATE EMAIL

        for user in cls.data:

            if user["email"] == email:
                return False, "Email already exists"

        user_data = {

            "name": name,
            "email": email,
            "pin": pin,
            "age": age,
            "phone": phone,
            "accountNumber": cls.generate_account_number(),
            "balance": 0
        }

        cls.data.append(user_data)

        cls.save_data()

        return True, user_data

    # LOGIN

    @classmethod
    def login(cls, account_number, pin):

        for user in cls.data:

            if (
                user["accountNumber"] == account_number
                and
                user["pin"] == pin
            ):

                return user

        return None

    # DEPOSIT MONEY

    @classmethod
    def deposit_money(cls, user, amount):

        if amount <= 0:
            return False, "Invalid Amount"

        user["balance"] += amount

        cls.save_data()

        return True, f"₹{amount} Deposited Successfully"

    # WITHDRAW MONEY

    @classmethod
    def withdraw_money(cls, user, amount):

        if amount <= 0:
            return False, "Invalid Amount"

        if amount > user["balance"]:
            return False, "Insufficient Balance"

        user["balance"] -= amount

        cls.save_data()

        return True, f"₹{amount} Withdrawn Successfully"

    # UPDATE ACCOUNT

    @classmethod
    def update_account(
        cls,
        user,
        name,
        email,
        phone,
        pin
    ):

        if len(str(phone)) != 10:
            return False, "Phone number must be 10 digits"

        if len(str(pin)) != 4:
            return False, "PIN must be 4 digits"

        user["name"] = name
        user["email"] = email
        user["phone"] = phone
        user["pin"] = pin

        cls.save_data()

        return True, "Account Updated Successfully"

    # DELETE ACCOUNT

    @classmethod
    def delete_account(cls, user):

        cls.data.remove(user)

        cls.save_data()

        return True, "Account Deleted Successfully"