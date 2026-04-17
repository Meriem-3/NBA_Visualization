import pandas as pd              
from app.models import engine

df = pd.read_sql("SELECT * FROM player_stats", engine)
print(df.columns)