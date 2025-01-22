import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class DatabaseManager:
    def __init__(self, db_url: str = "sqlite:///data.sqlite"):
        """Initialize the database manager.
        
        Args:
            db_url (str): Database URL. Defaults to SQLite database in current directory.
        """
        self.engine: Engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all tables defined in SQLAlchemy models."""
        Base.metadata.create_all(bind=self.engine)
        
    @contextmanager
    def get_session(self):
        """Provide a transactional scope around a series of operations.
        
        Yields:
            Session: SQLAlchemy session object
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def init_db(self):
        """Initialize the database, creating all tables."""
        # Create the data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Create all tables
        self.create_tables()

# Create a global instance of DatabaseManager
db = DatabaseManager() 