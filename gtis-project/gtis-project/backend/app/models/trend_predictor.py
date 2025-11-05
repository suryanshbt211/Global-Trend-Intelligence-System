import pandas as pd
import numpy as np
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class TrendPredictor:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.metrics = {}
        
    def predict(self, data: pd.DataFrame, keyword: str, periods: int = 30):
        df = data.copy()
        df = df.reset_index()
        df.columns = ['ds', 'y']
        predictions = {}
        
        try:
            prophet_pred = self._predict_prophet(df, periods)
            predictions['prophet'] = prophet_pred
        except Exception as e:
            print(f"Prophet error: {e}")
            
        try:
            arima_pred = self._predict_arima(df, periods)
            predictions['arima'] = arima_pred
        except Exception as e:
            print(f"ARIMA error: {e}")
            
        if predictions:
            ensemble = self._ensemble_predictions(predictions)
            predictions['ensemble'] = ensemble
            
        return predictions
    
    def _predict_prophet(self, df: pd.DataFrame, periods: int):
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,
            changepoint_prior_scale=0.05
        )
        model.fit(df)
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        train_pred = forecast[forecast['ds'].isin(df['ds'])]['yhat'].values
        mape = mean_absolute_percentage_error(df['y'].values, train_pred)
        rmse = np.sqrt(mean_squared_error(df['y'].values, train_pred))
        self.metrics['prophet'] = {'mape': mape, 'rmse': rmse}
        
        return {
            'dates': forecast['ds'].tail(periods).dt.strftime('%Y-%m-%d').tolist(),
            'values': forecast['yhat'].tail(periods).tolist(),
            'lower_bound': forecast['yhat_lower'].tail(periods).tolist(),
            'upper_bound': forecast['yhat_upper'].tail(periods).tolist(),
            'mape': mape,
            'rmse': rmse
        }
    
    def _predict_arima(self, df: pd.DataFrame, periods: int):
        model = ARIMA(df['y'].values, order=(5, 1, 2))
        fitted_model = model.fit()
        forecast = fitted_model.forecast(steps=periods)
        
        train_pred = fitted_model.fittedvalues
        mape = mean_absolute_percentage_error(df['y'].values[1:], train_pred[1:])
        rmse = np.sqrt(mean_squared_error(df['y'].values[1:], train_pred[1:]))
        self.metrics['arima'] = {'mape': mape, 'rmse': rmse}
        
        future_dates = pd.date_range(start=df['ds'].max(), periods=periods + 1, freq='D')[1:]
        
        return {
            'dates': future_dates.strftime('%Y-%m-%d').tolist(),
            'values': forecast.tolist(),
            'mape': mape,
            'rmse': rmse
        }
    
    def _ensemble_predictions(self, predictions: dict):
        weights = {}
        total_weight = 0
        
        for model_name, pred in predictions.items():
            if 'mape' in pred:
                weight = 1 / (pred['mape'] + 0.01)
                weights[model_name] = weight
                total_weight += weight
        
        for model_name in weights:
            weights[model_name] /= total_weight
        
        ensemble_values = np.zeros(len(next(iter(predictions.values()))['values']))
        
        for model_name, pred in predictions.items():
            if model_name in weights:
                ensemble_values += np.array(pred['values']) * weights[model_name]
        
        return {
            'dates': next(iter(predictions.values()))['dates'],
            'values': ensemble_values.tolist(),
            'weights': weights
        }
    
    def get_model_metrics(self):
        return self.metrics
    
    def is_ready(self):
        return True
