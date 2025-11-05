import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
from typing import Dict

class CorrelationService:
    def __init__(self):
        self.external_data_cache = {}
    
    def compute_correlations(self, keyword: str, external_source: str, max_lag: int = 30):
        external_data = self._get_external_data(external_source)
        if external_data is None:
            return {"error": "External data source not available"}
        
        trend_data = self._simulate_trend_data(keyword)
        correlations = []
        
        for lag in range(-max_lag, max_lag + 1):
            pearson_corr, pearson_p = self._compute_lagged_correlation(trend_data, external_data, lag, 'pearson')
            spearman_corr, spearman_p = self._compute_lagged_correlation(trend_data, external_data, lag, 'spearman')
            
            correlations.append({
                "lag": lag,
                "pearson_correlation": float(pearson_corr),
                "pearson_pvalue": float(pearson_p),
                "spearman_correlation": float(spearman_corr),
                "spearman_pvalue": float(spearman_p)
            })
        
        best = max(correlations, key=lambda x: abs(x['pearson_correlation']))
        
        return {
            "keyword": keyword,
            "external_source": external_source,
            "correlations": correlations,
            "best_correlation": best,
            "interpretation": self._interpret_correlation(best)
        }
    
    def _compute_lagged_correlation(self, series1: np.ndarray, series2: np.ndarray, lag: int, method: str = 'pearson'):
        if lag > 0:
            s1, s2 = series1[lag:], series2[:-lag] if lag > 0 else series2
        elif lag < 0:
            s1, s2 = series1[:lag], series2[-lag:]
        else:
            s1, s2 = series1, series2
        
        min_len = min(len(s1), len(s2))
        s1, s2 = s1[:min_len], s2[:min_len]
        
        return pearsonr(s1, s2) if method == 'pearson' else spearmanr(s1, s2)
    
    def _get_external_data(self, source: str):
        np.random.seed(42)
        return np.random.randn(365) * 10 + 50
    
    def _simulate_trend_data(self, keyword: str):
        np.random.seed(hash(keyword) % 1000)
        return np.random.randn(365) * 20 + 60
    
    def _interpret_correlation(self, best: Dict):
        corr = abs(best['pearson_correlation'])
        lag = best['lag']
        strength = "weak" if corr < 0.3 else "moderate" if corr < 0.7 else "strong"
        direction = "positive" if best['pearson_correlation'] > 0 else "negative"
        
        if lag == 0:
            timing = "simultaneous"
        elif lag > 0:
            timing = f"{lag} days after the trend"
        else:
            timing = f"{abs(lag)} days before the trend"
        
        return f"{strength.capitalize()} {direction} correlation, occurring {timing}"
