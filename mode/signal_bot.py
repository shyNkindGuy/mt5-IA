import asyncio
from telegram import Bot
import discord
from threading import Thread

class TradingSignalBot:
    def __init__(self, mode='SIGNAL', config=None):
        self.mode = mode #'SIGNAL' o 'EXECUTE'
        self.config = config
        
        async def send_signal(self, signal, opportunity_score):
            #enviar señal a telegram y discord
            message = self._format_message(signal, opportunity_score)
        
            if 'telegram' in self.config:
                bot = Bot(token=self.config['telegram']['token'])
                await bot.send_message(
                    chat_id=self.config['telegram']['chat_id'],
                    text = message,
                    parse_mode = 'HTML'
                )
            if 'discord' in self.config:
                webhook = discord.Webhook.from_url(
                    self.config['discord']['webhook'],
                    adapter=discord.RequestsWebhookAdapter()
                )
                webhook.send(message)
    def _format_signal(self, signal, score):
        return f""" 🔔 <b>SEÑAL FVG {signal['direction'].upper()}</b>
        ⏰ Temporalidad: {signal['timeframe']}
        📈 Entrada: {signal['entry']:.5f}
        ⚖️ Score Oportunidad: {score:.2f}/1.0
        
        🎯 TP sugerido: {signal.get('tp', 'Calculando...')}
        🛑 SL sugerido: {signal.get('sl', 'Calculando...')}
        
        💡 <i>Modo: {'SEÑAL' if self.mode == 'SIGNAL' else 'EJECUCIÓN AUTOMÁTICA'}</i>  """                
        