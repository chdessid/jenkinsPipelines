import psycopg2

pgconn = psycopg2.connect(user="postgres",password="postgres",host="localhost",port="5432",database="jaridaa_dev")
pgcursor = pgconn.cursor()
pgconn.autocommit = True
