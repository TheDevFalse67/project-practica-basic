from functions import *

# Apuntamos la ruta al archivo .db de la base de datos
path_database = r'------------------------------------------------------'

# Inicializamos la base de datos y la tabla si aún no existen
init_db(path_database)

while True:
    print_actions()
    try:
        option = int(input("Enter your option: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        continue
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        break

    if option == 0:
        print("Exiting...")
        break
    elif option == 1:
        add_incident(path_database)
    elif option == 2:
        list_logs(path_database)
    elif option == 3:
        list_security_level(path_database)
    elif option == 4:
        export_csv(path_database)
    elif option == 5:
        delete_incident(path_database)
    else:
        print("Invalid option. Please enter an option from 0 to 5.")
