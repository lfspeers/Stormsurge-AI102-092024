import pandas as pd
import sqlalchemy

# Database connection details
db_user = 'postgres'
db_password = None
db_host = 'localhost'
db_port = '5433'
db_name = 'AzureAI'

# Create the connection string
engine = sqlalchemy.create_engine(f'postgresql://{db_user}@{db_host}:{db_port}/{db_name}')

# Read data from a PostgreSQL table into a Pandas DataFrame
query = "SELECT * FROM INFORMATION_SCHEMA.tables"
# df = pd.DataFrame(engine.connect().execute(sqlalchemy.text(query)))
df = pd.read_sql_query(sql=sqlalchemy.text(query), con=engine.connect())


print(df)