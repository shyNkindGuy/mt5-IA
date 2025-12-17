CONFIG = {
    'mode': 'signal',
    'capital': 1000,
    
    'mt5': {
        'account': 123,
        'password': 'MTsrypC5',
        'server': 'BrokerServer'
    },
    
    'symbols': ['XAUUSD', 'EURUSD'],
    'timeframes': [mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4],
    
    'notifications': {
        'telegram':{ 
            'token': '7584613694:AAFUAzIv_992sQTNu1m756UulWoyey4JJJM',
            'chat_id': '6400646481'
    },
        'discord':{
            'webhook': 'https://discord.com/api/webhooks/1363281418909651034/NSUTQ-lQbK3gF5ZVPrT1ssN4RQgrES-5kmx8QrRXqfQFL7nP6FwN5ksaJXPb4vYCO4us'
        }
    },
    'risk': {
        'base_risk': 0.01,
        'max_risk': 0.02,
        'min_score_execute': 0.6
    }
}