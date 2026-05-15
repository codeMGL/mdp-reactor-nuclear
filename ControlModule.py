# Import required dependencies
import numpy as np
import mdptoolbox


class ControlModule:
    def __init__(self):
        """Dummy constructor to use the Python Class as a namespace"""
        pass

    @staticmethod
    def generate_P(probs: np.ndarray, n_states: np.int32 = 100) -> np.ndarray:
        """Function that generates the probabilities (transition) matrix"""
        matrix_P = np.zeros((3, n_states, n_states), dtype=np.float64)  # cambiar a 100x100

        #saca las probabilidades del Json 
        probs_decrease = probs[0]
        probs_maintain = probs[1]
        probs_increase = probs[2]

        #Las probabilidades en los bordes se pierden, así que las filas no suman 1. (Y creo que normalizar es un apaño que no debería estar bien)
        #Ej: COn decrease en estado 1, sumas las probabilidad de bajar a 0, pero no a la de bajar a -1 porque nunca se cumple en los IFs

        #Tantas iteraciones creo que son ineficientes, y mi pc es una patata, así que creo que hay que aprovechar mejor el hecho que
        #sabemos que solo hay que modificar 3 IJs, no hace falta comprobar los 100, el 97% de las comprobaciones son inncesarias

        # ---------------- DECREASE ----------------
        """ 

            DECREASE ANGEL
            for estado_inicial in range(n_states):
                dest_0 = max(0, estado_inicial - 2)
                dest_1 = max(0, estado_inicial - 1)
                dest_2 = estado_inicial

                matrix_P[0][estado_inicial][dest_0] += probs_decrease[0]
                matrix_P[0][estado_inicial][dest_1] += probs_decrease[1]
                matrix_P[0][estado_inicial][dest_2] += probs_decrease[2]
        
        """
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):
                if estado_inicial == estado_final:
                    matrix_P[0][estado_inicial][estado_final] = probs_decrease[2]
                elif estado_inicial - 1 == estado_final:
                    matrix_P[0][estado_inicial][estado_final] = probs_decrease[1]
                elif estado_inicial - 2 == estado_final:
                    matrix_P[0][estado_inicial][estado_final] = probs_decrease[0]

        # ---------------- MAINTAIN ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):
                if estado_inicial == estado_final:
                    matrix_P[1][estado_inicial][estado_final] = probs_maintain[1]
                elif estado_inicial + 1 == estado_final:
                    matrix_P[1][estado_inicial][estado_final] = probs_maintain[2]
                elif estado_inicial - 1 == estado_final:
                    matrix_P[1][estado_inicial][estado_final] = probs_maintain[0]

        # ---------------- INCREASE ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):
                if estado_inicial == estado_final:
                    matrix_P[2][estado_inicial][estado_final] = probs_increase[0]
                elif estado_inicial + 1 == estado_final:
                    matrix_P[2][estado_inicial][estado_final] = probs_increase[1]
                elif estado_inicial + 2 == estado_final:
                    matrix_P[2][estado_inicial][estado_final] = probs_increase[2]

        # ---------------- CORRECCIÓN DE BORDES ----------------
        # Si una acción intenta llevar el reactor por debajo del estado 0
        # o por encima del estado n_states - 1, esa probabilidad no se pierde:
        # se acumula en el borde correspondiente.

        # DECREASE:
        # En estado 0, los movimientos -2 y -1 se quedan en 0.
        matrix_P[0][0][0] += probs_decrease[0] + probs_decrease[1]

        # En estado 1, el movimiento -2 se queda en 0.
        matrix_P[0][1][0] += probs_decrease[0]

        # MAINTAIN:
        # En estado 0, el movimiento -1 se queda en 0.
        matrix_P[1][0][0] += probs_maintain[0]

        # En el último estado, el movimiento +1 se queda en el último estado.
        matrix_P[1][n_states - 1][n_states - 1] += probs_maintain[2]

        # INCREASE:
        # En el penúltimo estado, el movimiento +2 se queda en el último estado.
        matrix_P[2][n_states - 2][n_states - 1] += probs_increase[2]

        # En el último estado, los movimientos +1 y +2 se quedan en el último estado.
        matrix_P[2][n_states - 1][n_states - 1] += probs_increase[1] + probs_increase[2]

        

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
    def generate_R(demand_t: np.float64, n_states: np.int32 = 100) -> np.ndarray:
        """Function that generates the rewards (costs) matrix"""
        demand = np.float64(demand_t) # Debug

        matrix_R = np.zeros((3, n_states, n_states), dtype=np.float64) # (3x)100x100
        # quitar DEBUGGING
        # son recompensas, poner costes negativos

        # Se calcula la matriz de distancias entre el estado actual s y el estado futuro s'
        # Aunque no se pueden alcanzar algunos estados (ej, pasar de s a s + 40),
        # como en la matriz de probabilidades esa probabilidad es nula, el coste es indiferente
        # Entonces, calculamos la distancia entre 'estado_inicial' y 'estado_final' y la duplicamos
        # si la acción elegida se aleja del objetivo 'demand'


        #al final hacer otra iteración exterior, y probar con np.where 
        # ---------------- DECREASE ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):

                delta_t = demand - (estado_final/ n_states)

                coste = abs(delta_t)
                # Comprobamos si la acción nos aleja del estado final (demanda)
                # Si la distancia hasta la demanda es mayor en el estado actual vs. en el estado final,
                # nos hemos alejado. Hay que multiplicar x2 la distancia
                if demand > (estado_inicial/ n_states):
                    # print(
                    #     "Nos alejamos (decrease)",
                    #     estado_inicial,
                    #     estado_final,
                    #     "d_t",
                    #     delta_t,
                    # )
                    coste *= 2
                # else:
                #     delta_t = abs(delta_t)  # Para DEBUGING
                # Rellenamos la matriz para estado_final x estado_inicial
                matrix_R[0][estado_inicial][estado_final] = -coste

        # ---------------- MAINTAIN ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):

                delta_t = demand - (estado_final/ n_states)

                coste = abs(delta_t)


                matrix_R[1][estado_inicial][estado_final] = -coste

        # ---------------- INCREASE ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):

                delta_t = demand - (estado_final/ n_states)

                coste = abs(delta_t)
                # Comprobamos si la acción nos aleja del estado final (demanda)
                # Si la distancia hasta la demanda es mayor en el estado actual vs. en el estado final,
                # nos hemos alejado. Hay que multiplicar x2 la distancia
                if demand < (estado_inicial/ n_states):
                    # print(
                    #     "Nos alejamos (increase)",
                    #     estado_inicial,
                    #     estado_final,
                    #     "d_t",
                    #     delta_t,
                    # )
                    coste *= 2
                # else:
                #     delta_t = abs(delta_t)  # Para DEBUGING

                matrix_R[2][estado_inicial][estado_final] = -coste



        # Creamos unos tests
        # print()
        # for estado_inicial in range(1, 3):
        #     for estado_final in range(estado_inicial - 1, estado_inicial + 2):
        #         coste0 = matrix_R[0][estado_final][estado_inicial]
        #         coste1 = matrix_R[1][estado_final][estado_inicial]
        #         coste2 = matrix_R[2][estado_final][estado_inicial]
        #         print(
        #             f"ACCIÓN: decrease. Para ir desde {estado_inicial} hasta {estado_final} --> Coste: {coste0}"
        #         )
        #         print(
        #             f"ACCIÓN: maintain. Para ir desde {estado_inicial} hasta {estado_final} --> Coste: {coste1}"
        #         )
        #         print(
        #             f"ACCIÓN: increase. Para ir desde {estado_inicial} hasta {estado_final} --> Coste: {coste2}"
        #         )
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
    def control_iteration(P, R, estado_actual, gamma, max_iter=1000) -> np.int32:
        """Function that computes one control-iteration"""

        # ECUACION BELLMAN: V(s) = max_a [ sum_s'( P[s,s',a] * (R[s,s',a] + gamma * V[s']) ) ]


        # print("P y R", P.shape, R.shape)
        # print()
        # print(P[0][:3][:3])
        # print("P\n", P)
        # print(R[0][:3][:3])
        # print()

        # -- Comprobacion provisional de si la matriz P es estocastica
        # La última fila tiene todo ceros, rellenamos con uno en la posicion final
        # print()
        # print("P normalizada\n", P)
        # print(check_stochastic(P))
        # print()
        """
        #politica optima con la libreria .... 
        pi = mdptoolbox.mdp.PolicyIteration(P, R, gamma, max_iter=max_iter)
        pi.setVerbose()
        pi.run()
        print("Policy: ", pi.policy)
        return pi.policy[estado_actual]"""
    
        mdp = mdptoolbox.mdp.ValueIteration(
            transitions=P,
            reward=R,
            discount=gamma,
            max_iter=max_iter
        )

        mdp.run()

        return np.int32(mdp.policy[estado_actual])



    @staticmethod
    def control_loop(demand: np.ndarray,
                    probs: np.ndarray,
                    n_states: np.int32,
                    n_actions: np.int32,
                    gamma: np.float64,) -> np.ndarray:
        
        """Function that computes all the required iterations (control-loop) to satisfy the power demand"""


        respuesta = np.zeros_like(a=demand, dtype=np.float64)  # Almacena las acciones para cada demanda
        current_state = np.int32(0)  # Estado inicial, se puede modificar si se desea empezar en otro estado

        action_deltas = [np.array([-2, -1,  0], dtype=np.int32), np.array([-1,  0,  1], dtype=np.int32),np.array([ 0,  1,  2], dtype=np.int32)]
        ControlModule._P = ControlModule.generate_P(probs, n_states)

        for t in range(demand.shape[0]): # La demanda cambia en el tiempo 

            ControlModule._demand_t = np.float64(demand[t])
            ControlModule._current_state = current_state 

            ControlModule._R = ControlModule.generate_R(ControlModule._demand_t, n_states) # esta demanda concreta.
            action = ControlModule.control_iteration(P= ControlModule._P, R= ControlModule._R, estado_actual = ControlModule._current_state, gamma=gamma)

            state_increment = np.random.choice( a=action_deltas[action], p=probs[action])
            current_state = current_state + state_increment
            current_state = np.int32(np.clip(a=current_state, a_min=0, a_max=n_states - 1))
            respuesta[t] = current_state / n_states
        return respuesta

"""
def check_stochastic(P, tol=1e-6):

    P = np.array(P)
    assert P.ndim == 3, f"P debe ser (A, S, S), tiene forma {P.shape}"
    A, S, _ = P.shape
    ok = True
    for a in range(A):
        row_sums = P[a].sum(axis=1)
        bad = np.where(np.abs(row_sums - 1.0) > tol)[0]
        if len(bad) > 0:
            ok = False
            for s in bad:
                print(f"  Acción {a}, Estado {s}: suma = {row_sums[s]:.8f}")
    if ok:
        print("✅ Matriz estocástica: todas las filas suman 1.")
    else:
        print("❌ Matriz NO estocástica.")
    return ok

""" 

