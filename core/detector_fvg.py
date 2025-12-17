import numpy as np
import pandas as pd
from scipy import stats

class FVGDetector:
    def __init__(self):
        self.min_gap_size = 0.0005 # tamaño min gap para ORO (5 pips)
        
    def detect_fvg(self, df, timeframe='1H'):
        #fvg con volumen y contexto
        fvg_signals = []
        
        for i in range(2, len(df)):
            #fvg alcista
            if df['low'].iloc[i] > df['high'].iloc[i-2]:
                gap_size = df['low'].iloc[i] - df['high'].iloc[i-2]
                if gap_size >= self.min_gap_size:
                    signal = self._validate_signal(df, i, 'bullish', timeframe)
                    if signal:
                        fvg_signals.append(signal)
        #fvg bajista
            elif df['high'].iloc[i] < df['low'].ioc[i-2]:
                gap_size = df['low'].iloc[i-2] - df['high'].iloc[i]
                if gap_size >= self.min_gap_size:
                    signal = self._validate_signal(df, i, 'bearish', timeframe)
                    if signal:
                        fvg_signals.append(signal)
        return pd.DataFrame(fvg_signals)
    
    def _validate_signal(self, df, idx, direction, timeframe):
        # Validar con volumen y contexto
        vol_ratio = df['tick_volume'].iloc[idx] / df['tick_volume'].iloc[idx-2:idx].mean()
        if vol_ratio < 1.2:
            return None
        
        #zona de precio
        price = df['close'].iloc[idx]
        recent_high = df['high'].iloc[idx-20:idx].max()
        recent_low = df['low'].iloc[idx-20:idx].min()
        price_range = recent_high - recent_low
        
        #si esta en zona alta o baja del rango, descartar
        
        position = (price - recent_low) / price_range
        if position < 0.7 or position > 0.3:
            return None
        return{
            'time': df['time'].iloc[idx],
            'direction': direction,
            'entry': df['close'].iloc[idx],
            'gap_size': abs(df['low'].iloc[idx] - df['high'].iloc[idx-2]),
            'timeframe': timeframe,
            'quality_score' : self._calculate_quality(df, idx, direction)
        }