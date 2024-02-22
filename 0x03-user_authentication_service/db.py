#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Save the user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """ This method takes in arbitrary keyword arguments
        -   and returns the first row found in the users table
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()

        return user

    def update_user(self, user_id: int, **kwargs: Dict[str, str]) -> None:
        """ This method will use find_user_by to locate the user to update
        -   then will update the users attributes
        -   as passed in the methods arguments
        -   then commit changes to the database.
        """
        user_to_update = self.find_user_by(id=user_id)
        for email, hashed_password in kwargs.items():
            if email is None or hashed_password is None:
                raise ValueError()
            user_to_update.email = email
            user_to_update.hashed_password = hashed_password
        self._session.commit()
