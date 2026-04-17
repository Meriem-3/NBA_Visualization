from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Base SQLite locale
engine = create_engine("sqlite:///sportstats.db", echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine) #interagir avec la base


class PlayerStat(Base):

    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_name = Column(String(100))
    team_abbreviation = Column(String(10))
    age = Column(Integer)
    player_height = Column(Float)
    player_weight = Column(Float)
    college = Column(String(100))
    country = Column(String(50))
    draft_year = Column(String(10))
    draft_round = Column(String(10))
    draft_number = Column(String(10))
    gp = Column(Integer)
    pts = Column(Float)
    reb = Column(Float)
    ast = Column(Float)
    net_rating = Column(Float)
    oreb_pct = Column(Float)
    dreb_pct = Column(Float)
    usg_pct = Column(Float)
    ts_pct = Column(Float)
    ast_pct = Column(Float)
    season = Column(String(20))



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
 


def init_db():
    
    #Crée les tables en base si elles n'existent pas encore. 
    Base.metadata.create_all(engine)