# Import required dependencies
import numpy as np
import mdptoolbox

class ControlModule:
    def __init__(self):
        """ Dummy constructor to use the Python Class as a namespace """
        pass

    @staticmethod
    def generate_P(probs) -> np.ndarray:
        """Function that generates the probabilities (transition) matrix"""
        ### TO BE COMPLETED BY THE STUDENTS ###
        # 3x3 o 3x3x3 o 100x100x3
        matrix_P = np.zeros((3, 10, 10), dtype=np.float64) # cambiar a 100x100

        probs_decrease = probs[0]
        probs_maintain = probs[1]
        probs_increase = probs[2]
        

        # ---------------- DECREASE ----------------
        for i in range(10):
            for j in range(10):
                if i == j:
                    matrix_P[0][i][j] = probs_decrease[2]
                elif i - 1 == j:
                    matrix_P[0][i][j] = probs_decrease[1]
                elif i - 2 == j:
                    matrix_P[0][i][j] = probs_decrease[0]

        # ---------------- MAINTAIN ----------------
        for i in range(10): 
            for j in range(10):
                if i == j:
                    matrix_P[1][i][j] = probs_maintain[1]
                elif i + 1 == j:
                    matrix_P[1][i][j] = probs_maintain[2]
                elif i - 1 == j:
                    matrix_P[1][i][j] = probs_maintain[0]
                    
        # ---------------- INCREASE ----------------
        for i in range(10):
            for j in range(10):
                if i == j:
                    matrix_P[2][i][j] = probs_increase[0]
                elif i + 1 == j:
                    matrix_P[2][i][j] = probs_increase[1]
                elif i + 2 == j:
                    matrix_P[2][i][j] = probs_increase[2]
                    


        print("Probabilidades:\n")
        print(matrix_P)
        return matrix_P

    @staticmethod  
    def generate_R(estado_actual, demand) -> np.ndarray:
        """ Function that generates the rewards (costs) matrix """
        demand = np.floor(demand[0] * 100)
        demand = 4
        Coste_inicial = abs(estado_actual - demand)
        matriz_calculo_costes = np.zeros((3,3))

        print(matriz_calculo_costes) #debería printearse una matriz 3x3 llena de ceros


        # Se mantiene constanteeeeeee
        matriz_cambios_estado = np.array([[-2,-1,0],
                                          [-1,0,1], # 3 x 3
                                          [0,1,2]])
        matriz_P = np.zeros((3, 100, 100), dtype=np.float64) # cambiar a 100x100

        # ----------------Jorge--------------------------------------------------------------
        #Calculas la matriz que guarda los costes a partir de cada cambio de estado a partir de las posibles acciones
        # for estado_inicial in range(3):
        #     for state in range(100):
        #         for j in range(3):
        #             coste_final_asociado = matriz_cambios_estado[estado_inicial][j]# 10 x 3
        #             probabilidad = probs[estado_inicial][j]
        #             next_state = state + coste_final_asociado
        #             next_state = np.clip(next_state, 0, 100 - 1)
        #             matriz_calculo_costes[estado_inicial][j] = coste_final_asociado
        #             matriz_P[estado_inicial][state][next_state] = 1 
        # print (matriz_P)
        #-------------------------- Fin Jorge---------------------------------------------------
        
        #-------------------------------Territorio de Angel-------------------
        # for i in range(3):
        #     for j in range(3):
        #         coste_accion_asociado = matriz_cambios_estado[i][j]# 10 x 3
        #         next_state = state + coste_final_asociado
        #         matriz_calculo_costes[i][j] = coste_final_asociado
        # print (matriz_P)
        #------------------------------Fin Territorio de Ángel ------------------------

        print(matriz_calculo_costes)
        
        ########################################################################
        matrix_R = np.zeros((10, 10), dtype=np.float64) # cambiar a 100x100
        
        # for action in range(3):
        for estado_inicial in range(10): # estados/estado inicial
            for estado_final in range(10): # resultado/estado final

                # movimientos = matriz_cambios_estado[acciones][resultados]
                
                # estado_siguiente = estado_actual + movimientos
                # print(acciones, estados, resultados, ">", estado_siguiente)

                # matriz_R[acciones][estados][estado_siguiente] = estado_siguiente
            
                delta_t = abs(estado_inicial - estado_final)
                
                
                # Comprobamos si la acción nos aleja del estado final (demanda)
                # Si la distancia hasta la la demanda es mayor ahora vs. en el estado final,
                # nos hemos alejado. Hay que multiplicar x2 la distancia
                if abs(estado_final - demand) > abs(estado_inicial - demand):
                    delta_t = delta_t * 2
                    print("Nos alejamos", estado_inicial, estado_final, "d_t", delta_t)
                matrix_R[estado_inicial][estado_final] = delta_t
                
        # # ---------------- MAINTAIN ----------------
        # accion = 1 # maintain
        # for estado_inicial in range(10): # estados/estado inicial
        #     for estado_final in range(10): # resultado/estado final
        #         delta_t = np.abs(estado_inicial - estado_final)
                
                    
        #         # Comprobamos si la acción nos aleja del estado final (demanda)
        #         # if estado_final - demand < estado_inicial - demand:
        #         if estado_final != estado_inicial: # Significa que no cambiamos de estado; nos alejamos del objetivo
        #             delta_t = delta_t * 2
        #         matrix_R[accion][estado_inicial][estado_final] = delta_t        
        
        print("DEMANDA ACTUAL: ", demand) 
        print(matrix_R)
        
        # Creamos unos tests
        for estado_inicial in range(1, 9):
            for estado_final in range(estado_inicial - 1, estado_inicial + 1):
                coste = matrix_R[estado_inicial][estado_final]
                print(f"Para ir desde {estado_inicial} hasta {estado_final} --> Coste: {coste}")
                
        return matriz_calculo_costes
        """
        DEMANDA ACTUAL:  4
        [[ 0.  1.  2.  3.  4.  5.  6.  7.  8. 18.]
        [ 2.  0.  1.  2.  3.  4.  5.  6. 14. 16.]
        [ 4.  2.  0.  1.  2.  3.  4. 10. 12. 14.]
        [ 6.  4.  2.  0.  1.  2.  6.  8. 10. 12.]
        [ 8.  6.  4.  2.  0.  2.  4.  6.  8. 10.]
        [10.  8.  6.  2.  1.  0.  2.  4.  6.  8.]
        [12. 10.  4.  3.  2.  1.  0.  2.  4.  6.]
        [14.  6.  5.  4.  3.  2.  1.  0.  2.  4.]
        [ 8.  7.  6.  5.  4.  3.  2.  1.  0.  2.]
        [ 9.  8.  7.  6.  5.  4.  3.  2.  1.  0.]]

        """



    @staticmethod  
    def control_iteration() -> np.int32:
        """ Function that computes one control-iteration """
        ### TO BE COMPLETED BY THE STUDENTS ###
        ...

    @staticmethod  
    def control_loop(demand: np.ndarray, 
                     probs: np.ndarray,
                     n_states: np.int32, 
                     n_actions: np.int32,
                     gamma: np.float64) -> np.ndarray:
        """ Function that computes all the required iterations (control-loop) to satisfy the power demand """
        ### TO BE COMPLETED BY THE STUDENTS ###

        ### DUMMY BEHAVIOUR TO PREVENT CRASHING (MUST BE DELETED AFTER THE FULL IMPLEMENTATION) ###
        return np.zeros_like(a=demand, dtype=np.float64)
        ### ###
#:)


