from app import Base, engine
from app import models  # ensures all models are registered
from sqlalchemy.orm import Session
from sqlalchemy import text  # <-- required

def truncate_all_tables():
    with Session(engine) as session:
        try:
            with session.begin():
                for table in reversed(Base.metadata.sorted_tables):
                    print(f"🔻 Truncating table {table.name}")
                    session.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))
            print("✅ All tables truncated.")
        except Exception as e:
            print(f"❌ Failed to truncate tables: {e}")

if __name__ == "__main__":
    truncate_all_tables()

