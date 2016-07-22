import uuid

import sqlalchemy as sa
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy_utils import Timestamp, force_auto_coercion
from sqlalchemy_utils.types import (ChoiceType, PasswordType, ScalarListType,
                                    UUIDType)

from .config import config

Base = declarative_base()
engine = sa.create_engine(config.DATABASE_URL)
session = scoped_session(sessionmaker(bind=engine))

force_auto_coercion()


#
# Models
#
class User(Base, Timestamp):
    """User model."""
    __tablename__ = 'users'

    id = sa.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password = sa.Column(PasswordType(schemes=['pbkdf2_sha512']),
                         nullable=False)
    name = sa.Column(sa.String(255))


class BatchStatus(Enum):
    """Batch Status Enum."""
    CREATED = 'created'
    COMMITED = 'commited'
    DONE = 'created'
    CANCELED = 'canceled'


BatchStatus.CREATED.label = 'Created'
BatchStatus.COMMITED.label = 'Commited'
BatchStatus.DONE.label = 'Done'
BatchStatus.CANCELED.label = 'Canceled'


class Batch(Base, Timestamp):
    """Coffee Batch."""
    __tablename__ = 'batches'

    id = sa.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    brewmaster_id = sa.Column(UUIDType, sa.ForeignKey('users.id'),
                              nullable=False)
    brewmaster = relationship('User')
    status = sa.Column(ChoiceType(BatchStatus, impl=sa.String(64)),
                       nullable=True,
                       default=BatchStatus.CREATED)
    participants = sa.Column(ScalarListType(), nullable=False)
    """
    FIXME: Don't forget to add the brewmaster to this list...

    Note: We are using the ScalarListType here (which is actually just a
    comma-separated string of UUIDs) in order to have a nice interface to
    add/remove users from the batch like: `batch.participants.append(user1)`.
    In the future we may need to move this to another table/relationship.
    """
