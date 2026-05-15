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
    """ Implementation of the Pearson's Correlation Coefficient """
    return np.float64(np.sqrt((np.sum((y_true - np.mean(y_true))*(y_pred - np.mean(y_pred)))/len(y_true))/((np.sum((y_true - np.mean(y_true))**2))/len(y_true)* (np.sum((y_pred - np.mean(y_pred))**2)/len(y_pred)))))
    # return 0.0 DUMMY