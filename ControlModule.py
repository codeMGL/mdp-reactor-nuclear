# Import required dependencies
import numpy as np
import mdptoolbox


class ControlModule:
    def __init__(self):
        """Dummy constructor to use the Python Class as a namespace"""
        pass

    @staticmethod  # Hace que la función no necesite un argumento
    def generate_P(probs) -> np.ndarray:
        """Function that generates the probabilities (transition) matrix"""
        ### TO BE COMPLETED BY THE STUDENTS ###
        # 3x3 o 3x3x3 o 100x100x3
        matriz_P = np.zeros((3, 10, 10), dtype=np.float64)

        probs_maintain = probs[1]
        print(probs_maintain)

        for i in range(10):
            for j in range(10):
                if i == j:
                    matriz_P[1][i][j] = probs_maintain[1]
                elif i + 1 == j:
                    matriz_P[1][i][j] = probs_maintain[2]
                elif i-1 == j:
                    matriz_P[1][i][j] = probs_maintain[0]
                


        print("Probabilidades:\n", matriz_P.shape)
        print(matriz_P)
        return matriz_P
        ...

    @staticmethod
    def generate_R() -> np.ndarray:
        """Function that generates the rewards (costs) matrix"""
        ### TO BE COMPLETED BY THE STUDENTS ###
        ...

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
