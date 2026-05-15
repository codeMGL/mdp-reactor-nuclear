# Import required dependencies
import numpy as np

def MAE(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    """ Implementation of the Mean Absolute Error (MAE) """
    return np.float64((np.sum(abs(y_pred - y_true)))/len(y_pred))
    # return 0.0 DUMMY

def MSE(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    """ Implementation of the Mean Squared Error (MSE) """
    return np.float64(np.sum(abs((y_pred - y_true)**2))/len(y_pred))
    # return 0.0 DUMMY

def R2(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    """ Implementation of the R2 metric """
    return np.float64(1-(np.sum((y_true - y_pred)**2)/np.sum((y_true - np.mean(y_true))**2)))
    # return 0.0 DUMMY

def Corr(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    """Implementation of the Pearson's Correlation Coefficient"""

    if np.std(y_true) == 0 or np.std(y_pred) == 0:
        return np.float64(0.0)

    return np.float64(np.corrcoef(y_true, y_pred)[0, 1])