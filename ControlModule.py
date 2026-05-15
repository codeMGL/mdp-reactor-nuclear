# Import required dependencies
import numpy as np
import mdptoolbox


class ControlModule:
    def __init__(self):
        """Dummy constructor to use the Python Class as a namespace"""
        pass

    @staticmethod
    def generate_P(
        probs: np.ndarray, n_states: np.int32 = 100, n_actions: np.int32 = 3
    ) -> np.ndarray:
        """Function that generates the probabilities (transition) matrix"""

        # Initialization of the Probability matrix
        matrix_P = np.zeros((3, n_states, n_states), dtype=np.float64)

        probs_decrease = probs[0]
        probs_maintain = probs[1]
        probs_increase = probs[2]

        # ---------------- DECREASE ----------------
        for initial_state in range(n_states):
            for final_state in range(n_states):
                if initial_state == final_state:
                    matrix_P[0][initial_state][final_state] = probs_decrease[2]
                elif initial_state - 1 == final_state:
                    matrix_P[0][initial_state][final_state] = probs_decrease[1]
                elif initial_state - 2 == final_state:
                    matrix_P[0][initial_state][final_state] = probs_decrease[0]

        # ---------------- MAINTAIN ----------------
        for initial_state in range(n_states):
            for final_state in range(n_states):
                if initial_state == final_state:
                    matrix_P[1][initial_state][final_state] = probs_maintain[1]
                elif initial_state + 1 == final_state:
                    matrix_P[1][initial_state][final_state] = probs_maintain[2]
                elif initial_state - 1 == final_state:
                    matrix_P[1][initial_state][final_state] = probs_maintain[0]

        # ---------------- INCREASE ----------------
        for initial_state in range(n_states):
            for final_state in range(n_states):
                if initial_state == final_state:
                    matrix_P[2][initial_state][final_state] = probs_increase[0]
                elif initial_state + 1 == final_state:
                    matrix_P[2][initial_state][final_state] = probs_increase[1]
                elif initial_state + 2 == final_state:
                    matrix_P[2][initial_state][final_state] = probs_increase[2]

        # ---------------- EDGE CORRECTION ----------------
        # We count how many non-zero elements are to normalize the whole line
        # Returns the index of the position where the prob is not null
        for action in range(n_actions):
            # Transposing the matrix
            for initial_state in range(n_states):
                non_zero_elts = np.where(matrix_P[action, initial_state, :] != 0)[0]
                # We divide all elements by the sum of the total probabilities
                if len(non_zero_elts) > 0:
                    alpha_val = 0
                    for idx in non_zero_elts:
                        alpha_val += matrix_P[action][initial_state][idx]

                    matrix_P[action][initial_state] *= 1 / alpha_val
                # Adding an average probability if all elts are null
                if len(non_zero_elts) == 0:
                    for end_state in range(n_states):
                        matrix_P[action][initial_state][end_state] = 1 / n_states

        return matrix_P

    @staticmethod
    def generate_R(demand_t: np.float64, n_states: np.int32 = 100) -> np.ndarray:
        """Function that generates the rewards (costs) matrix"""
        # Initialization of the Rewards matrix
        matrix_R = np.zeros((3, n_states, n_states), dtype=np.float64)
        # Method explained at the memory of the project
        # ---------------- DECREASE ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):
                delta_t = demand_t - (estado_final / n_states)
                coste = abs(delta_t)

                if demand_t > (estado_inicial / n_states):
                    coste *= 2

                matrix_R[0][estado_inicial][estado_final] = -coste

        # ---------------- MAINTAIN ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):
                delta_t = demand_t - (estado_final / n_states)
                coste = abs(delta_t)

                matrix_R[1][estado_inicial][estado_final] = -coste

        # ---------------- INCREASE ----------------
        for estado_inicial in range(n_states):
            for estado_final in range(n_states):
                delta_t = demand_t - (estado_final / n_states)
                coste = abs(delta_t)

                if demand_t < (estado_inicial / n_states):
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

        # Running the algorithm to converge to a single best action
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
        # Array of zeros of size 'demand'
        response = np.zeros_like(a=demand, dtype=np.float64)
        current_state = np.int32(0)

        # Matrix with the positions each action can apply
        action_deltas = [
            np.array([-2, -1, 0], dtype=np.int32),
            np.array([-1, 0, 1], dtype=np.int32),
            np.array([0, 1, 2], dtype=np.int32),
        ]

        P = ControlModule.generate_P(probs, n_states, n_actions)

        for t in range(demand.shape[0]):

            # Generation of the matrix R
            R = ControlModule.generate_R(demand[t], n_states)

            # Calculation of the best action
            action = ControlModule.control_iteration(
                P=P,
                R=R,
                estado_actual=current_state,
                gamma=gamma,
            )

            # Normalizing probs array
            sum = np.sum(probs[action])
            if sum == 0:
                for i in range(len(probs[action])):
                    probs[action][i] = 1 / sum
            else:
                probs[action] /= sum
                
            # Execution of the action (taking account uncertainty)
            state_increment = np.random.choice(a=action_deltas[action], p=probs[action])
            current_state = current_state + state_increment

            # The current state must be within the borders
            current_state = max(0, min(n_states - 1, current_state))

            # We add the next state to the array to return it
            response[t] = current_state / n_states

        return response
