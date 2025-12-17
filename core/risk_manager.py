class DynamicRiskManager:
    def __init__(self, capital=1000):
        self.capital = capital
        self.base_risk = 0.01  # 1% base
        self.max_risk = 0.02   # 2% si oportunidad excepcional
        self.min_lot = 0.01
        self.max_lot = 0.1     # 10% de capital máximo
        
    def calculate_position_size(self, symbol, entry, stop_loss, opportunity_score=0.5):
        """
        Calcula lote dinámico basado en:
        1. Riesgo base vs capital
        2. Score de oportunidad (0-1)
        3. Spread actual
        4. Distancia al stop
        """
        # Ajuste riesgo según score (0.5 -> 1%, 1.0 -> 2%)
        risk_percent = self.base_risk + (self.max_risk - self.base_risk) * opportunity_score
        
        risk_amount = self.capital * risk_percent
        
        # Obtener punto mínimo (pip size)
        symbol_info = mt5.symbol_info(symbol)
        point = symbol_info.point
        tick_value = symbol_info.trade_tick_value
        
        # Calcular distancia en pips
        stop_distance = abs(entry - stop_loss) / point
        
        # Spread actual (pips)
        spread = (symbol_info.ask - symbol_info.bid) / point
        
        # Lote base (sin spread)
        lot_base = risk_amount / (stop_distance * tick_value)
        
        # Ajuste por spread (no arriesgar más del 20% en spread)
        spread_risk = spread / stop_distance
        if spread_risk > 0.2:
            lot_base *= 0.8
        
        # Redondear a tamaño de lote válido
        lot_step = symbol_info.volume_step
        lot = round(lot_base / lot_step) * lot_step
        
        # Limites
        lot = max(self.min_lot, min(lot, self.max_lot))
        
        return {
            'lot': lot,
            'risk_percent': risk_percent * 100,
            'risk_amount': risk_amount,
            'stop_distance_pips': stop_distance,
            'spread_pips': spread
        }