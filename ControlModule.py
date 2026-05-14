# Import required dependencies
import numpy as np
import mdptoolbox


class ControlModule:
    def __init__(self):
        """Dummy constructor to use the Python Class as a namespace"""
        pass

    @staticmethod
    def generate_P(probs, n_states) -> np.ndarray:
        """Function that generates the probabilities (transition) matrix"""
        ### TO BE COMPLETED BY THE STUDENTS ###
        matrix_P = np.zeros(
            (3, n_states, n_states), dtype=np.float64
        )  # cambiar a 100x100

        probs_decrease = probs[0]
        probs_maintain = probs[1]
        probs_increase = probs[2]
        # ---------------- DECREASE ----------------
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
    def generate_R(demand_t: np.float64, n_states: np.int32 = 100) -> np.ndarray:
        """Function that generates the rewards (costs) matrix"""
        demand = demand_t
        print("Demanda:", demand)

        matrix_R = np.zeros((3, n_states, n_states))
        # cambiar a 100x100
        # quitar DEBUGGING
        # son recompensas, poner costes negativos

        # Se calcula la matriz de distancias entre el estado actual s y el estado futuro s'
        # Aunque no se pueden alcanzar algunos estados (ej, pasar de s a s + 40),
        # como en la matriz de probabilidades esa probabilidad es nula, el coste es indiferente
        # Entonces, calculamos la distancia entre 'estado_inicial' y 'estado_final' y la duplicamos
        # si la acción elegida se aleja del objetivo 'demand'

        # ---------------- DECREASE ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):

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
                # else:
                #     delta_t = abs(delta_t)  # Para DEBUGING

                # Rellenamos la matriz para estado_final x estado_inicial
                matrix_R[0][estado_final][estado_inicial] = -delta_t

        # ---------------- MAINTAIN ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):

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
                # else:
                #     delta_t = abs(delta_t)  # Para DEBUGING

                matrix_R[1][estado_final][estado_inicial] = -delta_t

        # ---------------- INCREASE ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):

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
                # else:
                #     delta_t = abs(delta_t)  # Para DEBUGING

                matrix_R[2][estado_final][estado_inicial] = -delta_t

        print()
        print("DEMANDA ACTUAL: ", demand)
        print(matrix_R)

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
        # print("P y R", P.shape, R.shape)
        # print()
        # print(P[0][:3][:3])
        # print("P\n", P)
        # print(R[0][:3][:3])
        # print()

        # -- Comprobacion provisional de si la matriz P es estocastica
        # La última fila tiene todo ceros, rellenamos con uno en la posicion final
        P[2][-1][-1] = 1

        for a in range(3):
            P[a] = P[a] / P[a].sum(axis=1, keepdims=True)  # renormaliza

        # print()
        # print("P normalizada\n", P)
        # print(check_stochastic(P))
        # print()

        pi = mdptoolbox.mdp.PolicyIteration(P, R, gamma, max_iter=max_iter)
        pi.setVerbose()
        pi.run()
        print("Policy: ", pi.policy)
        return pi.policy[estado_actual]
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
