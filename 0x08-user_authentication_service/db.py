from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


from user import Base
from user import User


class DB:

    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Save the user to the database
            Return
             - User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kw) -> User:
        """
            Takes in arbitrary keyword arguments
            Return
                - First row found in the users table as filtered
                by the method’s input arguments.
        """
        q = self._session.query(User).filter_by(**kw).first()
        return q

    def update_user(self, user_id: int, **kws) -> User:
        """ Locates the user to update it.
        """
        try:
            user_upd = self.find_user_by(id=user_id)
            for key, value in kws.items():
                setattr(user_upd, key, value)
            self._session.commit()
        except Exception:
            raise ValueError
