import sqlite3

with sqlite3.connect('db/database.db') as db:
    cursor = db.cursor()
    query1 = """ INSERT INTO expenses (id, name) VALUES (1, 'Коммуналка') """
    query2 = """ INSERT INTO expenses (name, id) VALUES ('Бензин', 2) """
    query3 = """ INSERT INTO expenses VALUES (3, 'Интернет') """
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
    db.commit()




