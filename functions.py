import sqlite3
import csv
import os

# 1. Función para crear la base de datos y la tabla si no existen
def init_db(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs_incident (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip_origin TEXT,
            type_event TEXT,
            severity_level TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

# 2. Menú de acciones
def print_actions():
    print("\n---------------------------------")
    print("0. Exit")
    print("1. add new incident")
    print("2. list all logs")
    print("3. filter by severity level")
    print("4. export as csv")
    print("5. delete incident")
    print("---------------------------------")

# 3. Agregar incidente (INSERT)
def add_incident(db_path):
    print("\n--- Add New Incident ---")
    timestamp = input("Enter timestamp: ")
    ip_origin = input("Enter ip origin: ")
    type_event = input("Enter event type: ")
    severity_level = input("Enter severity level: ")
    description = input("Enter description: ")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs_incident (timestamp, ip_origin, type_event, severity_level, description)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, ip_origin, type_event, severity_level, description))
    conn.commit()
    conn.close()
    print("¡Incidente guardado correctamente en la base de datos!")

# 4. Listar todos los incidentes (SELECT *)
def list_logs(db_path):
    print("\n---------- List All Logs -----------------------")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, ip_origin, type_event, severity_level, description FROM logs_incident")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No hay incidentes registrados.")
        return

    print(f"{'ID':<5} | {'Timestamp':<18} | {'IP Origin':<15} | {'Event Type':<15} | {'Severity':<10} | {'Description'}")
    print("-" * 85)
    for row in rows:
        print(f"{row[0]:<5} | {row[1]:<18} | {row[2]:<15} | {row[3]:<15} | {row[4]:<10} | {row[5]}")

# 5. Filtrar por nivel de severidad (SELECT WHERE)
def list_security_level(db_path):
    print("\n------- Filter by Severity Level --------------------------")
    severity = input("Enter severity level to filter (low, medium, high): ").strip()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, ip_origin, type_event, severity_level, description 
        FROM logs_incident 
        WHERE LOWER(severity_level) = LOWER(?)
    """, (severity,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"No se encontraron registros con severidad '{severity}'.")
        return

    print(f"{'ID':<5} | {'Timestamp':<18} | {'IP Origin':<15} | {'Event Type':<15} | {'Severity':<10} | {'Description'}")
    print("-" * 85)
    for row in rows:
        print(f"{row[0]:<5} | {row[1]:<18} | {row[2]:<15} | {row[3]:<15} | {row[4]:<10} | {row[5]}")

# 6. Exportar a CSV
def export_csv(db_path):
    print("\n--- Export as CSV ---")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, ip_origin, type_event, severity_level, description FROM logs_incident")
    rows = cursor.fetchall()
    conn.close()

    export_path = os.path.join(os.path.dirname(db_path), "incidents_export.csv")
    with open(export_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "timestamp", "ip_origin", "type_event", "severity_level", "description"])
        writer.writerows(rows)

    print(f"¡Datos exportados con éxito a: {export_path}!")

# 7. Eliminar incidente por ID (DELETE)
def delete_incident(db_path):
    print("\n--- Delete Incident ---")
    try:
        incident_id = int(input("Enter incident ID to delete: "))
    except ValueError:
        print("Por favor ingresa un ID numérico válido.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM logs_incident WHERE id = ?", (incident_id,))
    if not cursor.fetchone():
        print(f"No existe ningún incidente con ID {incident_id}.")
        conn.close()
        return

    cursor.execute("DELETE FROM logs_incident WHERE id = ?", (incident_id,))
    conn.commit()
    conn.close()
    print(f"¡Incidente #{incident_id} eliminado exitosamente!")
