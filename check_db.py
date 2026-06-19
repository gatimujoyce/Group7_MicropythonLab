import sqlite3

conn = sqlite3.connect('sensor_data.db')

print(f"{'ID':<5} {'Temperature':<15} {'Humidity':<12} {'Reading':<10} {'Timestamp'}")
print('-' * 65)

for row in conn.execute('SELECT * FROM readings'):
    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<12} {row[3]:<10} {row[4]}")

total = conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
print(f"\nTotal rows: {total}")

conn.close()