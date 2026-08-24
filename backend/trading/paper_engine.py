import json
import os
import uuid
from datetime import datetime
from backend.trading.market_data import get_current_price

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
os.makedirs(DATA_DIR, exist_ok=True)
PORTFOLIO_PATH = os.path.join(DATA_DIR, "paper_portfolio.json")

INITIAL_CASH = 100000.00

def _get_default_portfolio() -> dict:
    return {
        "cash_balance": INITIAL_CASH,
        "realized_pnl": 0.0,
        "positions": {}, # symbol -> { shares, avg_price, total_cost }
        "orders": []     # [{ id, symbol, side, shares, price, total, order_type, status, timestamp }]
    }

def load_portfolio() -> dict:
    if os.path.exists(PORTFOLIO_PATH):
        try:
            with open(PORTFOLIO_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    portfolio = _get_default_portfolio()
    save_portfolio(portfolio)
    return portfolio

def save_portfolio(data: dict):
    try:
        with open(PORTFOLIO_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving paper portfolio: {e}")

def place_order(symbol: str, shares: float, side: str = "BUY", order_type: str = "MARKET", limit_price: float = None) -> dict:
    """
    Executes a paper trade (BUY or SELL).
    """
    sym = symbol.upper().strip()
    side = side.upper().strip()
    order_type = order_type.upper().strip()
    
    if shares <= 0:
        return {"success": False, "message": "Shares must be greater than zero."}
    if side not in ("BUY", "SELL"):
        return {"success": False, "message": "Invalid side. Must be BUY or SELL."}

    current_price = get_current_price(sym)
    exec_price = limit_price if (order_type == "LIMIT" and limit_price is not None) else current_price
    
    if exec_price <= 0:
        return {"success": False, "message": f"Unable to determine market price for {sym}."}

    portfolio = load_portfolio()
    cash = portfolio["cash_balance"]
    positions = portfolio["positions"]
    
    total_order_cost = exec_price * shares

    order_id = str(uuid.uuid4())[:8]
    order_record = {
        "id": order_id,
        "symbol": sym,
        "side": side,
        "shares": shares,
        "price": round(exec_price, 2),
        "total": round(total_order_cost, 2),
        "order_type": order_type,
        "status": "FILLED",
        "timestamp": datetime.now().isoformat()
    }

    if side == "BUY":
        if cash < total_order_cost:
            return {
                "success": False,
                "message": f"Insufficient funds. Need ${total_order_cost:,.2f}, but cash balance is ${cash:,.2f}."
            }
        
        # Deduct cash
        portfolio["cash_balance"] = round(cash - total_order_cost, 2)
        
        # Update or create position
        if sym in positions:
            existing_shares = positions[sym]["shares"]
            existing_cost = positions[sym]["total_cost"]
            new_shares = existing_shares + shares
            new_total_cost = existing_cost + total_order_cost
            new_avg_price = new_total_cost / new_shares
            
            positions[sym] = {
                "shares": round(new_shares, 4),
                "avg_price": round(new_avg_price, 2),
                "total_cost": round(new_total_cost, 2)
            }
        else:
            positions[sym] = {
                "shares": round(shares, 4),
                "avg_price": round(exec_price, 2),
                "total_cost": round(total_order_cost, 2)
            }
            
        msg = f"Successfully BOUGHT {shares} share(s) of {sym} at ${exec_price:,.2f} (${total_order_cost:,.2f} total)."

    else: # SELL
        if sym not in positions or positions[sym]["shares"] < shares:
            avail = positions.get(sym, {}).get("shares", 0)
            return {
                "success": False,
                "message": f"Insufficient shares to sell. You own {avail} shares of {sym}."
            }
            
        pos = positions[sym]
        cost_basis_sold = pos["avg_price"] * shares
        realized_profit = total_order_cost - cost_basis_sold
        
        # Add cash & realized P&L
        portfolio["cash_balance"] = round(cash + total_order_cost, 2)
        portfolio["realized_pnl"] = round(portfolio.get("realized_pnl", 0.0) + realized_profit, 2)
        
        rem_shares = pos["shares"] - shares
        if rem_shares <= 0.0001:
            del positions[sym]
        else:
            pos["shares"] = round(rem_shares, 4)
            pos["total_cost"] = round(pos["avg_price"] * rem_shares, 2)
            
        pnl_str = f"+${realized_profit:,.2f}" if realized_profit >= 0 else f"-${abs(realized_profit):,.2f}"
        msg = f"Successfully SOLD {shares} share(s) of {sym} at ${exec_price:,.2f} (Realized P&L: {pnl_str})."

    portfolio["orders"].insert(0, order_record)
    save_portfolio(portfolio)
    
    return {
        "success": True,
        "message": msg,
        "order": order_record,
        "portfolio": get_portfolio_state()
    }

def get_portfolio_state() -> dict:
    """Calculates live portfolio balances, unrealized P&Ls, and position market values."""
    portfolio = load_portfolio()
    cash = portfolio["cash_balance"]
    positions_raw = portfolio["positions"]
    
    evaluated_positions = []
    total_positions_market_value = 0.0
    total_unrealized_pnl = 0.0
    
    for sym, data in positions_raw.items():
        curr_price = get_current_price(sym)
        shares = data["shares"]
        avg_price = data["avg_price"]
        total_cost = data["total_cost"]
        market_val = round(curr_price * shares, 2)
        unrealized_pnl = round(market_val - total_cost, 2)
        pnl_pct = round((unrealized_pnl / total_cost) * 100, 2) if total_cost > 0 else 0.0
        
        total_positions_market_value += market_val
        total_unrealized_pnl += unrealized_pnl
        
        evaluated_positions.append({
            "symbol": sym,
            "shares": shares,
            "avg_price": avg_price,
            "current_price": curr_price,
            "total_cost": total_cost,
            "market_value": market_val,
            "unrealized_pnl": unrealized_pnl,
            "pnl_pct": pnl_pct
        })
        
    total_portfolio_value = round(cash + total_positions_market_value, 2)
    total_return_dollar = round(total_portfolio_value - INITIAL_CASH, 2)
    total_return_pct = round((total_return_dollar / INITIAL_CASH) * 100, 2)
    
    return {
        "cash_balance": cash,
        "positions_value": round(total_positions_market_value, 2),
        "total_portfolio_value": total_portfolio_value,
        "total_return_dollar": total_return_dollar,
        "total_return_pct": total_return_pct,
        "unrealized_pnl": round(total_unrealized_pnl, 2),
        "realized_pnl": round(portfolio.get("realized_pnl", 0.0), 2),
        "positions": evaluated_positions,
        "orders": portfolio.get("orders", [])[:20]
    }

def reset_portfolio():
    """Resets paper trading portfolio back to $100k initial state."""
    portfolio = _get_default_portfolio()
    save_portfolio(portfolio)
    return get_portfolio_state()
