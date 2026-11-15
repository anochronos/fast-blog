from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# just sqlite for now, file gets created in whatever dir you run the app from
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# check_same_thread=False is needed bc fastapi can run sync routes in a
# threadpool, so a connection might get used on a different thread than
# the one that opened it. sqlite blocks that by default
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# factory for db sessions. turned off autocommit/autoflush so i control
# exactly when stuff gets written
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# all the models inherit from this so create_all() can find them
class Base(DeclarativeBase):
    pass


# dependency for routes - opens a session per request and the `with`
# makes sure it gets closed after the response, even if something errors
def get_db():
    with SessionLocal() as db:
        yield db
