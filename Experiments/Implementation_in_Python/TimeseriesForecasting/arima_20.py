import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import math

import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)

def splitData(ts):

    test_set_size = int(np.round(0.2*len(ts)))
    train_set = ts[:-test_set_size]    
    test_set = ts[-test_set_size:]

    return train_set, test_set

def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return pd.Series(diff)

def main():

    window_sz = 20

    filepath = "RELIANCE_2010-01-012021-08-30.csv"
    data = pd.read_csv(filepath, usecols=[0,4], names=['date', 'close'], header=0)
    data = data.sort_values('date')
    data['date'] = pd.to_datetime(data['date'])
    
    train_set, test_set = splitData(data['close'].values)

    history = [x for x in test_set[:20]]
    predictions = list()

    data_len = len(test_set) - window_sz

    # walk-forward validation
    for t in range(len(test_set)):
        model = ARIMA(history, order=(0,1,0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test_set[t]
        history.append(obs)
        # print('predicted=%f, expected=%f' % (yhat, obs))


    # evaluate forecasts
    rmse = math.sqrt(mean_squared_error(test_set, predictions))
    print('Test RMSE: %.3f' % rmse)

    # results = pd.DataFrame({'actual': test_set,
    #                    'forecasts': predictions})

    # results.to_csv('arima_20.csv', index=False)




if __name__ == "__main__":
    main()