from sqlmodel import SQLModel, Field, create_engine, Session, text

class Hero2(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    name : str 
    secret_name: str
    age : int | None = None

sqlite_file_name = "database2.db"
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

# if __name__ == "__main__":
#     main()


def check_for_missing_field():
    with engine.connect() as eng:
        all_metadata = eng.execute(text("PRAGMA table_info(hero2)"))
        column_info = all_metadata
        modify_flag_found = False
        for column in column_info:
            if column[1] == "modified_at":
                modify_flag_found = True
                break
        
        if not modify_flag_found:
            class temp_hero(SQLModel, table=True):
                id : int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
                name : str 
                secret_name: str
                age : int | None = None
                modified_at: str | None = None
            
            SQLModel.metadata.create_all(engine)
            eng.execute(text("INSERT INTO temp_hero (name, secret_name, age) SELECT name, secret_name, age FROM hero2"))
            eng.execute(text("DROP TABLE hero2"))
            eng.execute(text("ALTER TABLE temp_hero RENAME TO hero2"))

check_for_missing_field()