from sqlmodel import create_engine, Session

DB_URL = "postgresql://fastapi_taskman:fastapi_taskman@127.0.0.1:5432/fastapi_taskman"
engine = create_engine(DB_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
