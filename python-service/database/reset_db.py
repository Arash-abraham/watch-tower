from db import engine, Base
from sqlalchemy import text

def reset_database():
    #Delete the table programs
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS programs"))
        conn.execute(text("DROP TABLE IF EXISTS subdomains"))
        conn.commit()
        print("Tables dropped successfully!")
    
    Base.metadata.create_all(engine)
    print("Tables recreated with new structure!")

if __name__ == "__main__":
    reset_database()
