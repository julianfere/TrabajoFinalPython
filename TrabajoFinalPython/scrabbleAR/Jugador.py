import PySimpleGUI as sg
from Jugadores import Jugadores


class Jugador(Jugadores):
    def __init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo):
        Jugadores.__init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo)

    def _analizo(self, keys_ordenados, menor_1, menor_2, j,
                 k):  # menor_1 = fila_menor (caso horizontal) o columna_menor (caso vertical)
        for i in range(1,
                       len(keys_ordenados)):  # menor_2 = columna_menor (caso horizontal) o fila_menor (caso vertical)
            if keys_ordenados[i][j] != menor_1:  # j = 0 si es la fila (horizontal) o 1 si es columna (vertical)
                return False  # aca comparamos las filas/columnas de cada letra con la de la primera
            if keys_ordenados[i][k] - i != menor_2:  # k = 1 si es la columna (horizontal) o 0 si es la fila (vertical)
                return False  # si son contiguas, la resta de las mayores columnas/filas - i siempre es igual a la de la menor
        return True

    def _estan_en_el_centro(self, keys_ordenados):
        centro = self.long_tablero // 2
        if (centro, centro) in keys_ordenados:
            return True
        else:
            return False

    def jugar(self, palabra_nueva, letras_usadas, posiciones_ocupadas_tablero,
              primer_turno):  # ex confirmar palabra de nivel1
        keys_ordenados = sorted(palabra_nueva.keys())  # los ordeno por columna de menor a mayor
        columna_menor = keys_ordenados[0][1]  # me guarda la columna mas chica con la cual voy a hacer una comparacion
        fila_menor = keys_ordenados[0][0]  # me guardo la primer fila para compararla con las otras a ver si son iguales
        actualizar_juego = False
        # ahora analizamos si es valida o no:
        if not self._analizo(keys_ordenados, fila_menor, columna_menor, 0, 1) and not self._analizo(keys_ordenados,
                                                                                                    columna_menor,
                                                                                                    fila_menor, 1, 0):
            sg.popup_ok('Palabra no válida, por favor ingrese en forma horizontal o vertical')
        else:
            lista_letras_ordenadas = []
            for key in keys_ordenados:
                lista_letras_ordenadas.append(palabra_nueva[key])
            palabra_obtenida = ''.join(lista_letras_ordenadas)
            palabra_obtenida.strip()
            if self.es_palabra_valida(palabra_obtenida):
                al_centro = self._estan_en_el_centro(keys_ordenados)
                if (not primer_turno) or (primer_turno and al_centro):
                    posiciones_ocupadas_tablero.extend(palabra_nueva.keys())
                    ## funcion que suma los puntos por letra y segun cada boton duplica o resta puntos:
                    self.sumar_puntos(palabra_nueva)
                    actualizar_juego = True  # con esto despues se actualiza la ventana
                    for k in letras_usadas.keys():  # saco fichas de la bolsa para ponerlas en letras
                        self.fichas[k] = ""
                elif primer_turno and not al_centro:
                    sg.popup('La primer palabra debe ir en el centro')
            else:
                sg.popup_ok('Palabra no válida, por favor ingrese otra')
        return letras_usadas, palabra_nueva, actualizar_juego, posiciones_ocupadas_tablero
