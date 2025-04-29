import factory
from faker import Faker
from datetime import date, timedelta
from ..models import Employee
from apps.authentication.tests.factories import UserFactory

fake = Faker()

def generate_phone():
    # Generate a phone number that fits within 15 characters
    return fake.numerify(text='###-###-####')

class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    user = factory.SubFactory(UserFactory)
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    email = factory.LazyAttribute(lambda obj: obj.user.email)  # Use user's email by default
    phone = factory.LazyFunction(generate_phone)
    department = factory.LazyAttribute(lambda _: fake.job())
    position = factory.LazyAttribute(lambda _: fake.job())
    salary = factory.LazyAttribute(lambda _: fake.random_number(digits=5, fix_len=True))
    hire_date = factory.LazyAttribute(lambda _: fake.date_between(start_date='-5y', end_date='today')) 