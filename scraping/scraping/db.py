from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from typing import List
from datetime import date
import pymysql

Base = declarative_base()

class Film(Base):
    __tablename__ = 'films'
    
    id = Column(String(10), primary_key=True)
    title = Column(Text)

    reviews = relationship("Review", back_populates="film") # gets populated with the Review objects linked to this film

    def __str__(self):
        return "film : {}".format(self.title)

    def __repr__(self):
        return "<Film(id={}, title={})>".format(self.id, self.title)

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    film_id = Column(String(10), ForeignKey('films.id')) # code of the film
    user = Column(String(50), unique=True)
    rating = Column(String(5))
    date = Column(Date)
    review = Column(Text)

    film = relationship("Film", back_populates="reviews") # gets populated with the Film object linked to this review

    def __str__(self):
        return "user : {}\nreview : {}".format(self.user, self.review)

    def __repr__(self):
        return "<Review(id={}, film={}, user={}, date={}, rating={}, review={})>".format(self.id, self.film_id, self.user, self.date, self.rating, self.review)

class DBManager:
    """Singleton class which is used to get only one database manager instance all over the project."""
    __instance = None
    engine = None

    def __init__(self):
        """Create a new manager instance and the DB, if both not already existing."""
        if DBManager.__instance == None:
            DBManager.__instance = self
            self.engine = create_engine('mysql+pymysql://rsUser:rs_password@localhost/rs_db', echo=True)
            Base.metadata.create_all(self.engine)
        else:
            pass
    
    @staticmethod
    def getInstance():
        """Static access method for always getting the reference to the only manager istance."""
        if DBManager.__instance == None:
            DBManager()
        return DBManager.__instance

    def addFilm(self, id: str, title: str):
        """Take care of making and adding automatically to the db a new :class:`Film` instance, 
        made up of the parameters."""
        Session = sessionmaker(bind=self.engine)
        session = Session()

        film = Film(id=id, title=title)
        session.add(film)

        session.commit()
        session.close()

    def addReview(self, user: str, rating: str, date: date, review: str, film: Film):
        """Take care of making and adding automatically to the db a new :class:`Review` instance, 
        made up of the parameters where `film` (istance of :class:`Film`) is the one the review refers to."""
        Session = sessionmaker(bind=self.engine)
        session = Session()

        review_obj = Review(user=user, rating=rating, date=date, review=review, film=film)
        session.add(review_obj)

        session.commit()
        session.close()

    def getReviewsOf(self, filmID: str) -> List[Review]:
        """Return a list of reviews pair with the film identified by `filmID`.

        If any review does not exist, return an empty list."""
        Session = sessionmaker(bind=self.engine)
        session = Session()

        reviews = session.query(Review).filter_by(film_id=filmID).all()
        
        session.close()
        return reviews

    def getFilmByID(self, ID: str) -> Film:
        """If it exists, return the film (istance of :class:`Film`) having that `ID`
         from the db, otherwise return `None`."""
        
        Session = sessionmaker(bind=self.engine)
        session = Session()

        film = session.query(Film).filter_by(id=ID).first()
        
        session.close()
        return film