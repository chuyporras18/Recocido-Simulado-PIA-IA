import math
from random import randint
from secrets import choice
from time import time


# Creamos nuestra instancia de la ruta con dos parametros: uno sera el total de tiendas que tendra cada ciudad, y el otro
# sera el total de ciudades que tendremos.


def instancia_ruta(totalStores, totalCity):

    # Creamos nuestra lista que contendra la informacion de las rutas de cada ciudad.
    mrute = []

    # Iteramos el total de ciudades.
    for city in range(totalCity):

        # Creamos una lista que contendra la informacion de las rutas de la ciudad en la iteracion actual.
        cityRutes = []

        # Iteramos el total de tiendas.
        for store in range(totalStores):

            # Creamos una lista que contendra la informacion de las rutas disponibles para cada tienda.
            storesRutes = []

            # Iteramos el total de tiendas mas 1.
            for rute in range(1, totalStores + 1):

                # Si la ruta de la tienda actual es igual a la misma tienda, saltamos a la proxima iteracion, ya que no nos interesa
                # la ruta de una tienda hacia si mismo.
                if rute == store + 1:
                    continue

                # Creamos un tiempo aleatorio que tardara en llegar a dicha tienda desde 10 a 30 minutos.
                time = randint(10, 30)

                # A la lista de rutas de la tienda le agregamos la tupla con la informacion, que contendra el numero de tienda a que se
                # se llega y su tiempo de translado.
                storesRutes.append((rute, time))

            # Si la ciudad no es la ultima, le agregamos tambien a la ruta hacia la proxima ciudad.
            if city + 1 != totalCity:
                storesRutes.append((rute + 1, randint(40, 80)))

            # Despues le agregamos las rutas de las tiendas a la lista de rutas de la ciudad actual.
            cityRutes.append(storesRutes)

        # Ya por ultimo, le agregamos la lista de rutas de la ciudad a la lista de ciudades.
        mrute.append(cityRutes)

    # Devolvemos la lista.
    return mrute


# Para generar nuestros vecinos, solamente necesitamos un parametro, que sera la informacion de la ruta.
def generar_vecino(rute):

    # Creamos una lista vacia que sera para nuestro vecino.
    vecino = []

    # Itramos cada elementro o ciudad de la lista de la ruta.
    for city in rute:

        # Generemaos una lista de las posibles tiendas a las que se puede llegar.
        stores = list(range(1, len(city) + 1))

        # Creamos una lista auxiliar para nuestro subvecino, que sera para la lista de cada ciudad.
        subvecino = []

        # Mientras aun haya tiendas disponibles en la lista creada anteriormente, hacemos...
        while len(stores) > 0:

            # Escogemos una tienda al azar de la lista disponible.
            store = choice(stores)

            # Se lo agregamos a nuestro subvecino.
            subvecino.append(store)

            # Lo quitamos de la lista de tiendas aun no visitadas.
            stores.remove(store)

        # Si nuesto vecino no ha llegado a su ultimo elemento, hacemos...
        if len(vecino) != len(rute) - 1:

            # Le agregamos tambien la informacion de la proxima ciudad.
            subvecino.append(len(city) + 1)

        # Le agregamos nuestra lista de la ruta de ciuades a nuestro vecino.
        vecino.append(subvecino)

    # Devolvemos el vecino.
    return vecino


# Para obtener el tiempo o los costos de la solucion, solo necesitamos dos parametros, el vecino o la solucion que se va a revisar,
# y la ruta con la informacion.
def obtener_tiempo(vecino, rute):

    # Creamos un contador que tendra el tiempo de la solucion.
    time = 0

    # Iteramos para cada lista de nuestro vecino.
    for list in range(len(vecino) - 1):

        # Iteramos para cada elemento en la lista de nuestro vecino.
        for element in range(len(vecino[list]) - 2):

            # Creamos una variable auxiliar que contendra la informacion de la tienda en la ciudad de cada ciudad.
            mElement = rute[list][vecino[list][element] - 1]

            # Iteramos para cada tupla de dicha lista.
            for smElement in range(len(mElement)):

                # Comparamos si el elemento de la solucion es igual a la tienda en la lista actual.
                if mElement[smElement][0] == vecino[list][element + 1]:

                    # Incrementamos el tiempo con el tiempo en dicha tupla.
                    time += mElement[smElement][1]

                    # Rompemos para no seguir iterando.
                    break

        # Cuando haya terminado, tambien le agregaremos el tiempo que tarda en dirigirse a la proxima ciudad.
        time += rute[list][vecino[list][-2] - 1][-1][1]

    # Iteramos para la lista de nuestro vecino.
    for i in range(len(vecino[list + 1]) - 1):

        # Iteramos la ultima ciudad de nuestra ruta.
        for j in rute[-1][vecino[list + 1][i] - 1]:

            # Comparamos si el elemento de la solucion es igual a la tienda en la lista actual.
            if vecino[list + 1][i + 1] == j[0]:

                # Incrementamos el tiempo con el tiempo en dicha tupla.
                time += j[1]

                # Rompemos para no seguir iterando.
                break

    # Devolvemos el tiempo.
    return time


# Debido que al querer igualar una variable a otra, se igualan las direcciones de memoria, por lo que, al querer modificar una se modifican todas con dicha direccion.


def copiar_nueva_variable(s):

    # Creamos una lista vacia.
    nuevo = []

    # Iteramos a traves de cada elemento del parametro.
    for i in s:

        # Lo copiamos a la nueva lista.
        nuevo.append(i)

    # Retornamos la nueva lista.
    return nuevo


# Para resolver utilizando el algoritmo del recocido simulado, necesitamos de dos parametros, el cual sera el total de tiendas
# en cada ciudad y el total de ciudades.
def recocido_simulado(totalStores, totalCity):

    # Creamos una ruta con nuestra instancia.
    rute = instancia_ruta(totalStores, totalCity)

    # Obtenemos el tiempo actual del proceso.
    initial_time = time()

    # Inicializamor los parametros necesiarios para el algoritmo.

    iterations = 650
    temperature = 15
    dec_temp = -0.1

    # Generamos nuestra solucion inicial.
    initial_s = generar_vecino(rute)

    # Copiamos dicha solucion en otra variable.
    s = copiar_nueva_variable(initial_s)

    # Iteramos la cantidad de iteraciones establecidas.
    for i in range(iterations):

        # Generamos un nuevo vecino.
        vecino = copiar_nueva_variable(generar_vecino(rute))

        # Obtenemos el tiempo o el costo de la solucion anterior.
        dis_a = obtener_tiempo(s, rute)

        # Obtenemos el tiempo o costo de la solucion actual o el vecino.
        dis_b = obtener_tiempo(vecino, rute)

        # Comparamos dichas soluciones para ver si son mejores.
        if dis_a >= dis_b:

            # Si se cumple, hacemos a nuestra solucion igual al vecino.
            s = copiar_nueva_variable(vecino)

            # Pasamos a la siguiente iteracion.
            continue

       # Debido al desbordamiento de decimales en las divisiones, metemos el codigo en un try-except.
        try:

            # Creamos una expresion que devovlera un decimal para validar si se tomara la solucion peor.
            expression = math.pow(math.e, (dis_a - dis_b) / temperature)

            # Comparamos si esta en el rango disponible.
            if expression > randint(0, 1):

                # Nuestra nueva solucion sera el vecino aunque sea peor.
                s = copiar_nueva_variable(vecino)

                # Decrementamos la temperatura.
                temperature += dec_temp

                # Si la temperatura se llego a cero, volvemos a decrementar para evitar divisiones entre cero.
                if temperature == 0:
                    temperature += dec_temp
                continue

        except OverflowError:
            continue

    # Obtenemos el tiempo final del proceos.
    final_time = time()

    # Obtenemos el reusltado de la solucion inicial.
    initial_s_t = obtener_tiempo(initial_s, rute)

    # Obtenemos el resultado de la solucion final.
    final_s_t = obtener_tiempo(s, rute)

    # Imprimimos los resultados.
    print(f"{initial_s_t} min : {final_s_t} min en {final_time - initial_time}s")

    # Devolvemos una tupla con la informacion necesaria.
    return initial_s_t, final_s_t, (final_time - initial_time)


# Para resolver utilizando el algoritmo, solo necesitamos como parametro la ruta de la cual se va a extrar la informacion.
def busqueda_costos(rute):

    # Obtenemos el tiempo actual del proceso.
    initial_time = time()

    # Creamos una lista donde ira nuesto vecino.
    vecino = []

    # Iteramos a traves de las ciudades en la ruta.
    for city in rute:

        # Creamos una lista donde iran las tiendas a visitar de cada ciudad.
        subvecino = []

        # Iteramos a traves de cada tienda en la ciudad.
        for store in city:

            # Creamos dos variables de control para ver cual es el precio mas barato.
            bestPrice = 40
            indexOf = 0

            # Iteramos a traves de cada local de las tiendas.
            for local in store:

                # Comparamos si el precio de dicho local es menor al que se tiene guardado, y que ademas ese local no se haya visitado ya.
                if local[1] < bestPrice and local[0] not in subvecino:

                    # Si se cumple guardamos el mejor precio y el numero de tienda.
                    bestPrice = local[1]
                    indexOf = local[0]

            # Al terminar de comparar se lo agregamos a la lista de tiendas.
            subvecino.append(indexOf)

        # Despues esa lista de tiendas se la agregamos a la lista de ciudades.
        vecino.append(subvecino)

    # Iteramos a traves de cada lista de la ciudad.
    for i in range(len(vecino) - 1):

        # Le agregamos el cambio de ciudad en la lista de locales.
        vecino[i].append(len(vecino[i]) + 1)

    # Obtenemos el tiempo final del proceos.
    final_time = time()

    final_s_t = obtener_tiempo(vecino, rute)
    # Imprimimos los resultados.
    print(f"{final_s_t} min en {final_time - initial_time}s")

    # Devolvemos una tupla con la informacion necesaria.
    return final_s_t, (final_time - initial_time)