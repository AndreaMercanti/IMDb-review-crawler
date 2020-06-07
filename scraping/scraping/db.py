from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///prova.db', echo=True)
Base = declarative_base()

class Film(Base):
    __tablename__ = 'films'
    
    id = Column(String, primary_key=True)
    title = Column(Text)

    reviews = relationship("Review", back_populates="film") # gets populated with the Review objects linked to this film

    def __str__(self):
        return "film : {}".format(self.title)

    def __repr__(self):
        return "<Film(id={}, title={})>".format(self.id, self.title)

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    film_id = Column(String, ForeignKey('films.id')) # code of the film
    user = Column(String(50), unique=True)
    rating = Column(String(5))
    date = Column(Date)
    review = Column(Text)

    film = relationship("Film", back_populates="reviews") # gets populated with the Film object linked to this review

    def __str__(self):
        return "user : {}\nreview : {}".format(self.user, self.review)

    def __repr__(self):
        return "<Review(id={}, film={}, user={}, date={}, rating={}, review={})>".format(self.id, self.film_id, self.user, self.date, self.rating, self.review)

Base.metadata.create_all(engine)