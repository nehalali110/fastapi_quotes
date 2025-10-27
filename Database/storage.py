from sqlmodel import SQLModel, Field, create_engine, Session

class Hero2(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str 
    secret_name: str
    age : int | None = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///./Database/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    print("Main running storage")
    SQLModel.metadata.create_all(engine)

def create_heroes():
    hero1 = Hero2(name="Ironman", secret_name="Robert Downey Jr", age=23)
    hero2 = Hero2(name="nothing",secret_name="onepunchman")

    with Session(engine) as session:
        session.add(hero1)
        session.add(hero2)
        session.commit()

def main():
    create_db_and_tables()
    create_heroes()

if __name__ == "__main__":
    main()

