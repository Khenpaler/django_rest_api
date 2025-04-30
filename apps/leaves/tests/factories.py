import factory
from faker import Faker
from datetime import date, timedelta
from ..models import Leave, LeaveType
from apps.employees.tests.factories import EmployeeFactory

fake = Faker()

class LeaveTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaveType

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
    max_days = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=30))

class LeaveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Leave

    employee = factory.SubFactory(EmployeeFactory)
    leave_type = factory.SubFactory(LeaveTypeFactory)
    start_date = factory.LazyAttribute(lambda _: fake.date_between(start_date='-30d', end_date='+30d'))
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=fake.random_int(min=1, max=5)))
    reason = factory.LazyAttribute(lambda _: fake.text())
    status = factory.LazyAttribute(lambda _: fake.random_element(elements=('pending', 'approved', 'rejected', 'cancelled'))) 