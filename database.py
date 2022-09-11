import psycopg2

connection = psycopg2.connect(host="localhost", dbname="OnlineShop", user="postgres", password="postgres")
cursor = connection.cursor()

print('conexão estabeecida')

cursor.execute("CREATE TABLE aulas(id bigserial PRIMARY KEY, name varchar)")
connection.commit()