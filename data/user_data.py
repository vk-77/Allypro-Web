"""
Test data for the Elements web application.

Contains customer, location, service, and payment details used across
the Selenium-based regression suite.
"""

USER_DATA = {
    "customer_name": "DwayneHayes",
    "customer_id": "9102084",
    "location_id": "9102084-0001",
    "contact_name": "Kelli Braun",
    "service_id": "0001",
    "address": "NEW YORK",
    "postal_code": "10001",
    "new_city": "Brooklyn",
    "batch_id": "0000067966",
    "company": "ALLYPRO",
    "assigned_user": "automation test MVC",
    "automation_user": "AutoMVC",
    "email": "automvc@allypro.test",
    "yeison_b": "YeisonB",
    "mobile": "1234567890",
    "payment": {
        "card_holder_name": "Test User",
        "amount": "12",
        "card_number": "4111111111111111",
        "expiration_month": "01",
        "expiration_year": "2029",
        "cvv": "231",
        "zip_code": "12345",
        "detail_note": "Test Note",
    },
    "batch_id_2": "0000073577",
}
