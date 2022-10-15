from polygon import RESTClient
import sqlite3
import matplotlib.pyplot as plt


con = sqlite3.connect('C:/Users/feder/Desktop/guido_juan_tiscornia/base_datos/tutorial.db')
cliente = RESTClient("P9tQYJ0HwyLYlx8a8Zx7m0xl_9ScZMIB")

continuar = "seguir"

while(continuar != "salir"): 
    print("1. Actualización de datos")
    print("2. Visualización de datos")
    opcion = input("Indique una opción del menú (salir para terminar): ")
    if (opcion == "1"): 
        ticker = input("Ingrese ticker a pedir: ")
        fecha_inicio = input("Fecha de inicio (formato aaaa-mm-dd): ")
        fecha_fin = input("Fecha de fin (formato aaaa-mm-dd): ")  
        datos_formato_lista = cliente.get_aggs(ticker, 1, "day", fecha_inicio, fecha_fin)
        for i in range(len(datos_formato_lista)): 
            variable = str(datos_formato_lista[i])[4:-1].split(",")
            lista1 = []
            for valor in variable: 
                lista1.append(valor.split("=")[1])
            print(lista1)
            open = float(lista1[0])
            high = float(lista1[1])
            low = float(lista1[2])
            close = float(lista1[3])
            volume = float(lista1[4])
            vwap = float(lista1[5])
            timestamp = int(lista1[6])
            cur = con.cursor()
            consulta = """INSERT INTO finanzas (ticker, open, high, low, close, volume, vwap, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""
            datos = (ticker, open, high, low, close, volume, vwap, timestamp)
            cur.execute(consulta, datos)
            con.commit()


    elif (opcion == "2"): 
        print("1. Resumen de datos")
        print("2. Gráfico de un ticker")
        opcion_2 = input("Indique una opción del menú: ")
        if (opcion_2 == "1"): 
            cur = con.cursor()
            cur.execute("SELECT * from finanzas")
            datos = cur.fetchall()
            for fila in datos: 
                print(fila)
        elif (opcion_2 == "2"): 
            ticker_a_visualizar = input("Ingrese el ticker que desea graficar: ")
            consulta = """SELECT * from finanzas where ticker=?"""
            cur = con.cursor()
            cur.execute(consulta, (ticker_a_visualizar,))
            datos = cur.fetchall()
            ticket_al_cierre = []
            ticket_timestamp = []
            for fila in datos: 
                ticket_al_cierre.append(fila[4])
                ticket_timestamp.append(fila[-1])
                plt.title("Gráfico de la acción " + ticker_a_visualizar)
            plt.plot(ticket_timestamp, ticket_al_cierre, "ro--")
            plt.ylabel(ticker_a_visualizar)
            plt.show()
    elif (opcion == "salir"): 
        continuar = "salir"