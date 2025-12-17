import asyncio
from core.mt5_client import MT5Client
from core.fvg_detector import FVGDetector
from core.risk_manager import DynamicRiskManager
from ai.predictor import OpportunityScorer
from execution.signal_bot import TradingSignalBot
from execution.order_executor import OrderExecutor

class TradingBot:
    def __init__(self, config):
        self.mode = config['mode']
        self.symbols = config['symbols']
        self.timeframes = config['timeframes']
        
        self.mt5 = MT5Client(**config['mt5'])
        self.fvg_detector = FVGDetector()
        self.risk_manager = DynamicRiskManager(capital=config['capital'])
        self.scorer = OpportunityScorer()
        
        if self.mode == 'signal':
            self.bot = TradingSignalBot(mode='SIGNAL', config=config['notifications'])
        else:
            self.bot = TradingSignalBot(mode='EXECUTE', config=config['notifications'])
            self.executor = OrderExecutor(self.mt5, self.risk_manager)
            
    async def run_cycle(self):
        for symbol in self.symbols:
            for tf in self.timeframes:
                #obtener datos
                df = self.mt5.get_rates(symbol, tf, bars=500)
                #detectar fvg
                fvg_signals = self.fvg_detector.detect_fvg(df, tf)
                
                for _, signal in fvg_signals.iterrows():
                    market_context = self._get_market_context(df)
                    features = self.scorer.prepare_features(signal, market_context)
                    opportunity_score = self.scorer.score_opportunity(features)
                    
                    trade_plan = self._calculate_trade_plan(signal, opportunity_score)
                    
                    if self.mode == 'signal':
                        await self.bot.send_signal(signal, opportunity_score)
                    else:
                        if opportunity_score >= 0.6: #umbral minimo
                            risk_calc = self.risk_manager.calculate_position_size(
                                symbol,
                                entry=signal['entry'],
                                stop_loss=trade_plan['sl'],
                                opportunity_score=opportunity_score
                            )
                            
                            self.executor.execute_order(
                                symbol,
                                signal=signal,
                                risk_calc=risk_calc,
                                trade_plan=trade_plan
                            )
                            await self.bot.send_signal(signal, opportunity_score)
                            
    def _calculate_trade_plan(self, signal, score):
        #calcular SL y TP basado en estructura de mercado
        if signal['direction'] == 'bullish':
        #calcular del minimo del FVG, TP con ratio 1:1.5 minimo 
            sl = signal['entry'] - signal['gap_size'] * 1.2 
            tp = signal['entry'] + signal['gap_size'] * (1.5 + score) 
        else:
            sl = signal['entry'] + signal['gap_size'] * 1.2
            tp = signal['entry'] - signal['gap_size'] * (1.5 + score)
        
        return {'sl': sl, 'tp': tp, 'rr_ratio': abs(tp - signal['entry'] / abs(sl - signal['entry']))}
     