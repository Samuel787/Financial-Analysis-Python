def initialize(context):
    set_benchmark(sid(24819))
    context.aapl = sid(24)
    schedule_function(ma_crossover_handling, date_rules.every_day(), time_rules.market_open(hours = 1))
    
def ma_crossover_handling(context, data):
    hist = data.history(context.aapl, 'price', 50, '1d')
    log.info(hist.head())
    sma_50 = hist.mean()
    sma_20 = hist[-20:].mean()
    
    open_orders = get_open_orders()
    
    if sma_20 > sma_50:
        if context.aapl not in open_orders:
            order_target_percent(context.aapl, 1.0)
    elif sma_50 > sma_20:
        if context.aapl not in open_orders:
            order_target_percent(context.aapl, -1.0)
        
    record(leverage = context.account.leverage)
    
# def handle_data(context, data):
#     hist = data.history(context.aapl, 'price', 50, '1d')
#     log.info(hist.head())
#     sma_50 = hist.mean()
#     sma_20 = hist[-20:].mean()
    
#     open_orders = get_open_orders()
    
#     if sma_20 > sma_50:
#         if context.aapl not in open_orders:
#             order_target_percent(context.aapl, 1.0)
#     elif sma_50 > sma_20:
#         if context.aapl not in open_orders:
#             order_target_percent(context.aapl, -1.0)
        
#     record(leverage = context.account.leverage)
    