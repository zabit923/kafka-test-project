import factory
from faker import Faker

from core.database.models import Aplication

fake = Faker()


class AplicationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Aplication
        sqlalchemy_session = None

    user_name = factory.LazyAttribute(lambda _: fake.user_name())
    description = factory.LazyAttribute(lambda _: fake.text())
