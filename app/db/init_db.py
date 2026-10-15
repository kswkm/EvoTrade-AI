from app.db.base import Base
from app.db.session import engine


def init_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        # DB may not be running in local development or CI; fail-safe so app still starts.
        return
