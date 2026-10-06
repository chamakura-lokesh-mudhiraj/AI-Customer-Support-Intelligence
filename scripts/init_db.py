from app.core.database import Base, engine
from app.models.ticket_db import TicketDB


def init_database():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_database()