import numpy as np

def calculate_sma(closes: list[float], period: int = 20) -> list[float | None]:
    """Calculates Simple Moving Average."""
    if len(closes) < period:
        return [None] * len(closes)
    
    sma = [None] * (period - 1)
    for i in range(period - 1, len(closes)):
        window = closes[i - period + 1 : i + 1]
        sma.append(round(float(np.mean(window)), 2))
    return sma

def calculate_ema(closes: list[float], period: int = 20) -> list[float | None]:
    """Calculates Exponential Moving Average."""
    if len(closes) < period:
        return [None] * len(closes)
    
    multiplier = 2 / (period + 1)
    ema = [None] * (period - 1)
    # Seed with SMA
    initial_sma = float(np.mean(closes[:period]))
    ema.append(round(initial_sma, 2))
    
    curr_ema = initial_sma
    for i in range(period, len(closes)):
        curr_ema = (closes[i] * multiplier) + (curr_ema * (1 - multiplier))
        ema.append(round(curr_ema, 2))
    return ema

def calculate_rsi(closes: list[float], period: int = 14) -> list[float | None]:
    """
    Calculates Relative Strength Index using Wilder's smoothing method.
    RSI = 100 - (100 / (1 + RS))
    """
    if len(closes) <= period:
        return [None] * len(closes)
    
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    
    rsi = [None] * period
    avg_gain = float(np.mean(gains[:period]))
    avg_loss = float(np.mean(losses[:period]))
    
    if avg_loss == 0:
        rsi.append(100.0)
    else:
        rs = avg_gain / avg_loss
        rsi.append(round(100.0 - (100.0 / (1.0 + rs)), 2))
        
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        if avg_loss == 0:
            rsi.append(100.0)
        else:
            rs = avg_gain / avg_loss
            val = 100.0 - (100.0 / (1.0 + rs))
            rsi.append(round(float(val), 2))
            
    return rsi

def calculate_macd(closes: list[float], fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """
    Calculates MACD Line, Signal Line, and MACD Histogram.
    """
    if len(closes) < slow + signal:
        return {"macd": [], "signal": [], "histogram": []}
    
    ema_fast = calculate_ema(closes, fast)
    ema_slow = calculate_ema(closes, slow)
    
    macd_line = []
    valid_macd_values = []
    for f, s in zip(ema_fast, ema_slow):
        if f is not None and s is not None:
            m = round(f - s, 2)
            macd_line.append(m)
            valid_macd_values.append(m)
        else:
            macd_line.append(None)
            
    # Calculate signal line (EMA of MACD line)
    signal_line_valid = calculate_ema(valid_macd_values, signal)
    
    # Pad signal line to match full closes length
    offset = len(macd_line) - len(signal_line_valid)
    full_signal = [None] * offset + signal_line_valid
    
    histogram = []
    for m, sig in zip(macd_line, full_signal):
        if m is not None and sig is not None:
            histogram.append(round(m - sig, 2))
        else:
            histogram.append(None)
            
    return {
        "macd": macd_line,
        "signal": full_signal,
        "histogram": histogram
    }

def calculate_bollinger_bands(closes: list[float], period: int = 20, num_std: float = 2.0) -> dict:
    """
    Calculates Upper, Middle (SMA), and Lower Bollinger Bands.
    """
    if len(closes) < period:
        return {"upper": [], "middle": [], "lower": []}
        
    upper = [None] * (period - 1)
    middle = [None] * (period - 1)
    lower = [None] * (period - 1)
    
    for i in range(period - 1, len(closes)):
        window = closes[i - period + 1 : i + 1]
        m = float(np.mean(window))
        std = float(np.std(window))
        middle.append(round(m, 2))
        upper.append(round(m + (num_std * std), 2))
        lower.append(round(m - (num_std * std), 2))
        
    return {
        "upper": upper,
        "middle": middle,
        "lower": lower
    }

def calculate_all_indicators(candles: list[dict]) -> dict:
    """Calculates all key technical indicators for a given candlestick dataset."""
    if not candles:
        return {}
        
    closes = [c["close"] for c in candles]
    times = [c["time"] for c in candles]
    
    rsi = calculate_rsi(closes, 14)
    macd_dict = calculate_macd(closes, 12, 26, 9)
    ema20 = calculate_ema(closes, 20)
    ema50 = calculate_ema(closes, 50)
    ema200 = calculate_ema(closes, 200) if len(closes) >= 200 else calculate_ema(closes, min(len(closes), 100))
    bb = calculate_bollinger_bands(closes, 20, 2.0)
    
    # Latest snapshot summary
    latest_close = closes[-1]
    latest_rsi = next((r for r in reversed(rsi) if r is not None), 50.0)
    latest_macd = next((m for m in reversed(macd_dict["macd"]) if m is not None), 0.0)
    latest_sig = next((s for s in reversed(macd_dict["signal"]) if s is not None), 0.0)
    latest_hist = next((h for h in reversed(macd_dict["histogram"]) if h is not None), 0.0)
    
    # Signal Interpretation
    trend = "Neutral"
    if latest_rsi > 70:
        sentiment = "Overbought (Potential Bearish Reversal)"
    elif latest_rsi < 30:
        sentiment = "Oversold (Potential Bullish Reversal)"
    elif latest_rsi > 50:
        sentiment = "Bullish Momentum"
    else:
        sentiment = "Bearish Momentum"
        
    if latest_hist > 0 and latest_macd > latest_sig:
        trend = "Bullish MACD Crossover"
    elif latest_hist < 0 and latest_macd < latest_sig:
        trend = "Bearish MACD Crossover"

    return {
        "times": times,
        "closes": closes,
        "rsi": rsi,
        "macd": macd_dict,
        "ema20": ema20,
        "ema50": ema50,
        "ema200": ema200,
        "bollinger": bb,
        "summary": {
            "latest_close": latest_close,
            "latest_rsi": latest_rsi,
            "latest_macd": latest_macd,
            "sentiment": sentiment,
            "trend": trend
        }
    }
