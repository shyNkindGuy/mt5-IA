import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

class OpportunityScorer:
    def __init__(self):
        self.model = self._build_model()
        self.features = [
            'gap_size_normalized',
            'volume_ratio',
            'trend_strength',
            'volatility_ratio',
            'support_distance',
            'timeframe_multiplier' # 1 para 1h, 4 para 4h
        ]
    def prepare_features(self, fvg_signal, market_context):
        #preparar feautures para el modelo
        features = np.array([
            fvg.signal['gap_size'] / market_context['atr'],
            fvg_signal['volume_ratio'],
            market_context['trend_strength'],
            market_context['volatility_ratio'],
            market_context['support_distance'],
            4 if fvg_signal['timeframe'] == '4H' else 1
        ]).reshape(1, -1)
        
        return features
    
    def score_opportunity(self, features):
        #devolver 0-1 basado enm probabilidad de que llegue a TP antes que SL
        
        score = np.mean([
            min(features[0][0] * 2, 1.0),
            min(features[0][1] / 3, 1.0),
            min(features[0][2] + 0.5, 0),
            1 - abs(features[0][4] * 2)
        ])
        return np.clip(score, 0.1, 0.95)
    
    def train_advanced_model(self, historical_data):
        #entrenar modelo xgboost con datos historicos: X: fvg + contexto y: 1 si alcanzo TP, 0 si alcanzo SL primero
        
        pass
