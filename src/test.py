import duckdb

db = duckdb.connect("chess.duckdb")
db.sql("SET TimeZone='UTC'")

print(db.sql("select * from information_schema.tables"))