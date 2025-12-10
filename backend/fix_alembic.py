from sqlalchemy import text
from src.core.database import engine

def fix_alembic():
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
            conn.commit()
            print("Successfully dropped alembic_version table.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_alembic()
