# Import required dependencies
import numpy as np
import mdptoolbox


class ControlModule:
    def __init__(self):
        """Dummy constructor to use the Python Class as a namespace"""
        pass

    @staticmethod
    def generate_P(probs) -> np.ndarray:
        """Function that generates the probabilities (transition) matrix"""
        ### TO BE COMPLETED BY THE STUDENTS ###
        # 3x3 o 3x3x3 o 100x100x3
        matrix_P = np.zeros((3, 10, 10), dtype=np.float64)  # cambiar a 100x100

        probs_decrease = probs[0]
        probs_maintain = probs[1]
        probs_increase = probs[2]
        # ---------------- DECREASE ----------------
        for estado_inicial in range(10):
            for estado_final in range(10):
                if estado_inicial == estado_final:
                    matrix_P[0][estado_inicial][estado_final] = probs_decrease[2]
                elif estado_inicial - 1 == estado_final:
                    matrix_P[0][estado_inicial][estado_final] = probs_decrease[1]
                elif estado_inicial - 2 == estado_final:
                    matrix_P[0][estado_inicial][estado_final] = probs_decrease[0]

        # ---------------- MAINTAIN ----------------
        for estado_inicial in range(10):
            for estado_final in range(10):
                if estado_inicial == estado_final:
                    matrix_P[1][estado_inicial][estado_final] = probs_maintain[1]
                elif estado_inicial + 1 == estado_final:
                    matrix_P[1][estado_inicial][estado_final] = probs_maintain[2]
                elif estado_inicial - 1 == estado_final:
                    matrix_P[1][estado_inicial][estado_final] = probs_maintain[0]

        # ---------------- INCREASE ----------------
        for estado_inicial in range(10):
            for estado_final in range(10):
                if estado_inicial == estado_final:
                    matrix_P[2][estado_inicial][estado_final] = probs_increase[0]
                elif estado_inicial + 1 == estado_final:
                    matrix_P[2][estado_inicial][estado_final] = probs_increase[1]
                elif estado_inicial + 2 == estado_final:
                    matrix_P[2][estado_inicial][estado_final] = probs_increase[2]

        print("Probabilidades:\n")
        print(matrix_P)
        """
        [[[0.8   0.    0.    0.    0.    0.    0.    0.    0.    0.   ]
        [0.025 0.8   0.    0.    0.    0.    0.    0.    0.    0.   ]
        [0.175 0.025 0.8   0.    0.    0.    0.    0.    0.    0.   ]
        [0.    0.175 0.025 0.8   0.    0.    0.    0.    0.    0.   ]
        [0.    0.    0.175 0.025 0.8   0.    0.    0.    0.    0.   ]
        [0.    0.    0.    0.175 0.025 0.8   0.    0.    0.    0.   ]
        [0.    0.    0.    0.    0.175 0.025 0.8   0.    0.    0.   ]
        [0.    0.    0.    0.    0.    0.175 0.025 0.8   0.    0.   ]
        [0.    0.    0.    0.    0.    0.    0.175 0.025 0.8   0.   ]
        [0.    0.    0.    0.    0.    0.    0.    0.175 0.025 0.8  ]]

        [[0.6   0.35  0.    0.    0.    0.    0.    0.    0.    0.   ]
        [0.05  0.6   0.35  0.    0.    0.    0.    0.    0.    0.   ]
        [0.    0.05  0.6   0.35  0.    0.    0.    0.    0.    0.   ]
        [0.    0.    0.05  0.6   0.35  0.    0.    0.    0.    0.   ]
        [0.    0.    0.    0.05  0.6   0.35  0.    0.    0.    0.   ]
        [0.    0.    0.    0.    0.05  0.6   0.35  0.    0.    0.   ]
        [0.    0.    0.    0.    0.    0.05  0.6   0.35  0.    0.   ]
        [0.    0.    0.    0.    0.    0.    0.05  0.6   0.35  0.   ]
        [0.    0.    0.    0.    0.    0.    0.    0.05  0.6   0.35 ]
        [0.    0.    0.    0.    0.    0.    0.    0.    0.05  0.6  ]]

        [[0.    0.2   0.8   0.    0.    0.    0.    0.    0.    0.   ]
        [0.    0.    0.2   0.8   0.    0.    0.    0.    0.    0.   ]
        [0.    0.    0.    0.2   0.8   0.    0.    0.    0.    0.   ]
        [0.    0.    0.    0.    0.2   0.8   0.    0.    0.    0.   ]
        [0.    0.    0.    0.    0.    0.2   0.8   0.    0.    0.   ]
        [0.    0.    0.    0.    0.    0.    0.2   0.8   0.    0.   ]
        [0.    0.    0.    0.    0.    0.    0.    0.2   0.8   0.   ]
        [0.    0.    0.    0.    0.    0.    0.    0.    0.2   0.8  ]
        [0.    0.    0.    0.    0.    0.    0.    0.    0.    0.2  ]
        [0.    0.    0.    0.    0.    0.    0.    0.    0.    0.   ]]]
        """

        return matrix_P

    @staticmethod
    def generate_R(estado_actual, demand, n_states: np.int32 = 100) -> np.ndarray:
        """Function that generates the rewards (costs) matrix"""
        demand = np.floor(demand[0] * 100)
        # demand = 2
        """
        Coste_inicial = abs(estado_actual - demand)
        matriz_calculo_costes = np.zeros((3, 3))

        print(matriz_calculo_costes)  # debería printearse una matriz 3x3 llena de ceros

        # Se mantiene constanteeeeeee
        matriz_cambios_estado = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])  # 3 x 3
        matriz_P = np.zeros((3, 100, 100), dtype=np.float64)  # cambiar a 100x100
        # Calculas la matriz que guarda los costes a partir de cada cambio de estado a partir de las posibles acciones
        for estado_inicial in range(3):
            for state in range(100):
                for j in range(3):
                    coste_final_asociado = matriz_cambios_estado[estado_inicial][
                        j
                    ]  # 10 x 3

                    next_state = state + coste_final_asociado
                    next_state = np.clip(next_state, 0, 100 - 1)
                    matriz_calculo_costes[estado_inicial][j] = coste_final_asociado
                    matriz_P[estado_inicial][state][next_state] = 1
        print(matriz_P)

        # -------------------------------Territorio de Angel-------------------
        # for i in range(3):
        #     for j in range(3):
        #         coste_accion_asociado = matriz_cambios_estado[i][j]# 10 x 3
        #         next_state = state + coste_final_asociado
        #         matriz_calculo_costes[i][j] = coste_final_asociado
        # print (matriz_P)

        print(matriz_calculo_costes)
        """

        ########################################################################
        matrix_R = np.zeros((3, 10, 10))
        # cambiar a 100x100
        # quitar DEBUGGING
        # son recompensas, poner costes negativos

        # Se calcula la matriz de distancias entre el estado actual s y el estado futuro s'
        # Aunque no se pueden alcanzar algunos estados (ej, pasar de s a s + 40),
        # como en la matriz de probabilidades esa probabilidad es nula, el coste es indiferente
        # Entonces, calculamos la distancia entre 'estado_inicial' y 'estado_final' y la duplicamos
        # si la acción elegida se aleja del objetivo 'demand'

        # ---------------- DECREASE ----------------
        for estado_inicial in range(10):
            for estado_final in range(10):

                delta_t = demand - estado_final

                # Comprobamos si la acción nos aleja del estado final (demanda)
                # Si la distancia hasta la demanda es mayor en el estado actual vs. en el estado final,
                # nos hemos alejado. Hay que multiplicar x2 la distancia
                if delta_t > 0:
                    # print(
                    #     "Nos alejamos (decrease)",
                    #     estado_inicial,
                    #     estado_final,
                    #     "d_t",
                    #     delta_t,
                    # )
                    delta_t = -abs(delta_t * 2)
                else:
                    delta_t = abs(delta_t)  # Para DEBUGING

                # Rellenamos la matriz para estado_final x estado_inicial
                matrix_R[0][estado_final][estado_inicial] = delta_t

        # ---------------- MAINTAIN ----------------
        for estado_inicial in range(10):
            for estado_final in range(10):

                delta_t = demand - estado_final

                # Comprobamos si la acción nos aleja del estado final (demanda)
                # Si la distancia hasta la demanda es mayor en el estado actual vs. en el estado final,
                # nos hemos alejado. Hay que multiplicar x2 la distancia
                if delta_t != 0:
                    # print(
                    #     "Nos alejamos (maintain)",
                    #     estado_inicial,
                    #     estado_final,
                    #     "d_t",
                    #     delta_t,
                    # )
                    delta_t = -abs(delta_t * 2)
                else:
                    delta_t = abs(delta_t)  # Para DEBUGING

                matrix_R[1][estado_final][estado_inicial] = delta_t

        # ---------------- INCREASE ----------------
        for estado_inicial in range(10):
            for estado_final in range(10):

                delta_t = demand - estado_final

                # Comprobamos si la acción nos aleja del estado final (demanda)
                # Si la distancia hasta la demanda es mayor en el estado actual vs. en el estado final,
                # nos hemos alejado. Hay que multiplicar x2 la distancia
                if delta_t < 0:
                    # print(
                    #     "Nos alejamos (increase)",
                    #     estado_inicial,
                    #     estado_final,
                    #     "d_t",
                    #     delta_t,
                    # )
                    delta_t = -abs(delta_t * 2)
                else:
                    delta_t = abs(delta_t)  # Para DEBUGING

                matrix_R[2][estado_final][estado_inicial] = delta_t

        print()
        print("DEMANDA ACTUAL: ", demand)
        print(matrix_R)

        # Creamos unos tests
        print()
        for estado_inicial in range(1, 3):
            for estado_final in range(estado_inicial - 1, estado_inicial + 2):
                coste0 = matrix_R[0][estado_final][estado_inicial]
                coste1 = matrix_R[1][estado_final][estado_inicial]
                coste2 = matrix_R[2][estado_final][estado_inicial]
                print(
                    f"ACCIÓN: decrease. Para ir desde {estado_inicial} hasta {estado_final} --> Coste: {coste0}"
                )
                print(
                    f"ACCIÓN: maintain. Para ir desde {estado_inicial} hasta {estado_final} --> Coste: {coste1}"
                )
                print(
                    f"ACCIÓN: increase. Para ir desde {estado_inicial} hasta {estado_final} --> Coste: {coste2}"
                )
        """
        [[[ *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.]
        [ *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.]
        [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]
        [  1.   1.   1.   1.   1.   1.   1.   1.   1.   1.]
        [  2.   2.   2.   2.   2.   2.   2.   2.   2.   2.]
        [  3.   3.   3.   3.   3.   3.   3.   3.   3.   3.]
        [  4.   4.   4.   4.   4.   4.   4.   4.   4.   4.]
        [  5.   5.   5.   5.   5.   5.   5.   5.   5.   5.]
        [  6.   6.   6.   6.   6.   6.   6.   6.   6.   6.]
        [  7.   7.   7.   7.   7.   7.   7.   7.   7.   7.]]

        [[ *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.]
        [ *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.]
        [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]
        [ *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.]
        [ *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.]
        [ *6.  *6.  *6.  *6.  *6.  *6.  *6.  *6.  *6.  *6.]
        [ *8.  *8.  *8.  *8.  *8.  *8.  *8.  *8.  *8.  *8.]
        [*10. *10. *10. *10. *10. *10. *10. *10. *10. *10.]
        [*12. *12. *12. *12. *12. *12. *12. *12. *12. *12.]
        [*14. *14. *14. *14. *14. *14. *14. *14. *14. *14.]]

        [[  2.   2.   2.   2.   2.   2.   2.   2.   2.   2.]
        [  1.   1.   1.   1.   1.   1.   1.   1.   1.   1.]
        [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]
        [ *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.  *2.]
        [ *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.  *4.]
        [ *6.  *6.  *6.  *6.  *6.  *6.  *6.  *6.  *6.  *6.]
        [ *8.  *8.  *8.  *8.  *8.  *8.  *8.  *8.  *8.  *8.]
        [*10. *10. *10. *10. *10. *10. *10. *10. *10. *10.]
        [*12. *12. *12. *12. *12. *12. *12. *12. *12. *12.]
        [*14. *14. *14. *14. *14. *14. *14. *14. *14. *14.]]]
        """
        return matrix_R

    @staticmethod
    def control_iteration() -> np.int32:
        """Function that computes one control-iteration"""
        ### TO BE COMPLETED BY THE STUDENTS ###
        ...

    @staticmethod
    def control_loop(
        demand: np.ndarray,
        probs: np.ndarray,
        n_states: np.int32,
        n_actions: np.int32,
        gamma: np.float64,
    ) -> np.ndarray:
        """Function that computes all the required iterations (control-loop) to satisfy the power demand"""
        ### TO BE COMPLETED BY THE STUDENTS ###

        ### DUMMY BEHAVIOUR TO PREVENT CRASHING (MUST BE DELETED AFTER THE FULL IMPLEMENTATION) ###
        return np.zeros_like(a=demand, dtype=np.float64)
        ### ###


#:)
