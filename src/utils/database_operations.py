from src.utils.dependancies import *

class Database:
    def __init__(self):
        load_dotenv()
        self.connection = None

    def connect(self):
        try:
            self.docker_host = os.getenv("HOST_DB")
            self.docker_port = os.getenv("PORT_DB")
            self.postgres_user = os.getenv("POSTGRES_USER")
            self.postgres_password = os.getenv("POSTGRES_PASSWORD")
            self.postgres_db = os.getenv("POSTGRES_DB")
            self.db_url = f'postgresql://{self.postgres_user}:{self.postgres_password}@{self.docker_host}:{self.docker_port}/{self.postgres_db}'
            self.engine = create_engine(self.db_url)
            self.connection = self.engine.connect()
        except Exception as e:
            print(e)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        try:
            result = self.connection.execute(text(query))
            self.connection.commit()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            raise e

    def create_table(self):
        query = f"""
                CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                dob TEXT,
                email TEXT UNIQUE,
                password TEXT,
                reset_token TEXT,
                reset_expiration TIMESTAMP
            );                    
        """

        self.execute_query(query)

    def login(self, email, password):
        query = f"SELECT * from users where email = '{email}' and password = '{password}'"

        result = self.execute_query(query)
        user = result.fetchone()
        return user
    
    def select_user(self, email):
        query = f"SELECT * FROM users where email = '{email}'"
        result = self.execute_query(query)
        user = result.fetchone()
        return user
    
    def update_reset_token(self, reset_token, reset_expiration, email):
        query = f""" 
                UPDATE users
                SET reset_token = '{reset_token}', reset_expiration = '{reset_expiration}'
                WHERE email = '{email}'
            """
        result = self.execute_query(query)
        return result

    def update_first_name(self, first_name, id):
        query = f"UPDATE users SET first_name = '{first_name}' WHERE id = '{id}'"
        result = self.execute_query(query)
        return result
    
    def update_last_name(self, last_name, id):
        query = f"UPDATE users SET last_name = '{last_name}' WHERE id = '{id}'"
        result = self.execute_query(query)
        return result
    
    def update_dob(self, dob, id):
        query = f"UPDATE users SET dob = '{dob}' WHERE id = '{id}'"
        result = self.execute_query(query)
        return result
    
    def update_password(self, password, id):
        query = f"UPDATE users SET password = '{password}' WHERE id = '{id}'"
        result = self.execute_query(query)
        return result
    
    def insert_user(self, first_name, last_name, dob, email_reg, hashed_password):
        query = f"""
                    INSERT INTO users (first_name, last_name, dob, email, password)
                    VALUES ('{first_name}','{last_name}','{dob}','{email_reg}','{hashed_password}')
                """
        result = self.execute_query(query)
        return result