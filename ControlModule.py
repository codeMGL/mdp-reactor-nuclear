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
        matrix_P = np.zeros((3, n_states, n_states), dtype=np.float64)

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

        # ---------------- CORRECCIÓN DE BORDES ----------------
        matrix_P[0][0][0] += probs_decrease[0] + probs_decrease[1]
        matrix_P[0][1][0] += probs_decrease[0]

        matrix_P[1][0][0] += probs_maintain[0]
        matrix_P[1][n_states - 1][n_states - 1] += probs_maintain[2]

        matrix_P[2][n_states - 2][n_states - 1] += probs_increase[2]
        matrix_P[2][n_states - 1][n_states - 1] += probs_increase[1] + probs_increase[2]

        return matrix_P

    @staticmethod
    def generate_R(demand_t: np.float64, n_states: np.int32 = 100) -> np.ndarray:
        """Function that generates the rewards (costs) matrix"""
        demand = np.float64(demand_t)
        matrix_R = np.zeros((3, n_states, n_states), dtype=np.float64)

        # ---------------- DECREASE ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):
                delta_t = demand - (estado_final / n_states)
                coste = abs(delta_t)

                if demand > (estado_inicial / n_states):
                    coste *= 2

                matrix_R[0][estado_inicial][estado_final] = -coste

        # ---------------- MAINTAIN ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):
                delta_t = demand - (estado_final / n_states)
                coste = abs(delta_t)

                matrix_R[1][estado_inicial][estado_final] = -coste

        # ---------------- INCREASE ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):
                delta_t = demand - (estado_final / n_states)
                coste = abs(delta_t)

                if demand < (estado_inicial / n_states):
                    coste *= 2

                matrix_R[2][estado_inicial][estado_final] = -coste

        return matrix_R

    @staticmethod
    def control_iteration(P, R, estado_actual, gamma, max_iter=1000) -> np.int32:
        """Function that computes one control-iteration"""
        mdp = mdptoolbox.mdp.ValueIteration(
            transitions=P,
            reward=R,
            discount=gamma,
            max_iter=max_iter,
        )

        mdp.run()

        return np.int32(mdp.policy[estado_actual])

    @staticmethod
    def control_loop(
        demand: np.ndarray,
        probs: np.ndarray,
        n_states: np.int32,
        n_actions: np.int32,
        gamma: np.float64,
    ) -> np.ndarray:
        """Function that computes all the required iterations (control-loop) to satisfy the power demand"""
        respuesta = np.zeros_like(a=demand, dtype=np.float64)
        current_state = np.int32(0)

        action_deltas = [
            np.array([-2, -1, 0], dtype=np.int32),
            np.array([-1, 0, 1], dtype=np.int32),
            np.array([0, 1, 2], dtype=np.int32),
        ]

        ControlModule._P = ControlModule.generate_P(probs, n_states)

        for t in range(demand.shape[0]):
            ControlModule._demand_t = np.float64(demand[t])
            ControlModule._current_state = current_state
            ControlModule._R = ControlModule.generate_R(ControlModule._demand_t, n_states)

            action = ControlModule.control_iteration(
                P=ControlModule._P,
                R=ControlModule._R,
                estado_actual=ControlModule._current_state,
                gamma=gamma,
            )

            state_increment = np.random.choice(a=action_deltas[action], p=probs[action])
            current_state = current_state + state_increment
            current_state = np.int32(np.clip(a=current_state, a_min=0, a_max=n_states - 1))
            respuesta[t] = current_state / n_states

        return respuesta
