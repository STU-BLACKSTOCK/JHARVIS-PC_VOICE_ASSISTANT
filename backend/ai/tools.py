from backend.productivity import notes_tasks, clipboard, email_service
from backend.reminders import alarms
from backend.automation import system_monitor, web, workflow_engine
from backend.trading import market_data, indicators, paper_engine, portfolio_analytics

AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_note",
            "description": "Saves a quick thought, note, or piece of information for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The note text to save."}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_notes",
            "description": "Retrieves the user's saved notes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of notes to fetch, default 5."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Adds a new to-do task item to the user's task checklist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The task to be accomplished."},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Task urgency."}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "Retrieves the user's pending or completed to-do tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of tasks to fetch, default 10."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_alarm_or_reminder",
            "description": "Sets a timer, alarm, or reminder for X minutes into the future.",
            "parameters": {
                "type": "object",
                "properties": {
                    "minutes": {"type": "number", "description": "Number of minutes until the reminder fires."},
                    "message": {"type": "string", "description": "What to remind the user about."}
                },
                "required": ["minutes", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_clipboard_content",
            "description": "Reads the current text stored in the system clipboard.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_clipboard_content",
            "description": "Copies text to the system clipboard.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to copy to clipboard."}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_unread_emails",
            "description": "Fetches and summarizes recent unread emails from Gmail.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {"type": "integer", "description": "Max emails to read, default 3."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_telemetry",
            "description": "Retrieves live CPU usage, RAM utilization, and battery levels.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_quote",
            "description": "Retrieves the live market price and percentage change for a stock or crypto ticker symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Ticker symbol (e.g. AAPL, NVDA, TSLA, BTC, ETH)."}
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_technical_analysis",
            "description": "Calculates technical indicators including RSI, MACD, EMA trends, and Bollinger Bands for an asset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Ticker symbol (e.g. AAPL, NVDA, TSLA, BTC)."}
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "place_paper_trade",
            "description": "Places a simulated paper trading order (BUY or SELL) in the virtual portfolio ($100k account).",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Ticker symbol (e.g. AAPL, NVDA, TSLA, BTC)."},
                    "shares": {"type": "number", "description": "Number of shares / coins to trade."},
                    "side": {"type": "string", "enum": ["BUY", "SELL"], "description": "Order side (BUY or SELL)."},
                    "order_type": {"type": "string", "enum": ["MARKET", "LIMIT"], "description": "Execution type."},
                    "limit_price": {"type": "number", "description": "Required if order_type is LIMIT."}
                },
                "required": ["symbol", "shares", "side"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_portfolio_summary",
            "description": "Retrieves the current virtual trading portfolio value, cash balance, active positions, and P&L statistics.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_desktop_automation",
            "description": "Automates OS actions like launching apps, typing text, switching windows, or searching browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "instruction": {"type": "string", "description": "Natural language automation command."}
                },
                "required": ["instruction"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "define_word",
            "description": "Fetches the dictionary definition for a given word.",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {"type": "string", "description": "Word to define."}
                },
                "required": ["word"]
            }
        }
    }
]

def dispatch_tool_call(name: str, args: dict, broadcast_callback=None) -> str:
    """Executes a tool call and returns a descriptive string result for the LLM."""
    try:
        if name == "create_note":
            res = notes_tasks.add_note(args.get("content", ""))
            if broadcast_callback:
                broadcast_callback({"type": "productivity_update", "notes": notes_tasks.get_notes()})
            return res
            
        elif name == "get_notes":
            notes = notes_tasks.get_notes(args.get("limit", 5))
            if not notes:
                return "You have no saved notes."
            formatted = [f"• {n.get('content', n)}" for n in notes]
            return "Here are your saved notes:\n" + "\n".join(formatted)
            
        elif name == "create_task":
            res = notes_tasks.add_task(args.get("content", ""), args.get("priority", "medium"))
            if broadcast_callback:
                broadcast_callback({"type": "productivity_update", "tasks": notes_tasks.get_tasks()})
            return res
            
        elif name == "get_tasks":
            tasks = notes_tasks.get_tasks(args.get("limit", 10))
            if not tasks:
                return "Your task list is currently empty."
            formatted = [f"• [{t.get('status', 'pending')}] {t.get('content', t)}" for t in tasks]
            return "Here are your tasks:\n" + "\n".join(formatted)
            
        elif name == "set_alarm_or_reminder":
            mins = float(args.get("minutes", 1))
            msg = args.get("message", "Time is up!")
            
            def reminder_cb(text):
                if broadcast_callback:
                    broadcast_callback({"type": "alarm_triggered", "message": text})
                from backend.speech.speaker import speak
                speak(text)
                
            return alarms.set_reminder(mins, msg, reminder_cb)
            
        elif name == "get_clipboard_content":
            return clipboard.read_from_clipboard()
            
        elif name == "set_clipboard_content":
            return clipboard.copy_to_clipboard(args.get("text", ""))
            
        elif name == "read_unread_emails":
            return email_service.read_latest_emails(args.get("max_results", 3))
            
        elif name == "get_system_telemetry":
            return system_monitor.format_system_stats_for_speech()
            
        elif name == "get_stock_quote":
            sym = args.get("symbol", "AAPL")
            price = market_data.get_current_price(sym)
            return f"The current price for {sym.upper()} is ${price:,.2f}."
            
        elif name == "get_technical_analysis":
            sym = args.get("symbol", "AAPL")
            candles = market_data.get_historical_candles(sym)
            inds = indicators.calculate_all_indicators(candles)
            summ = inds.get("summary", {})
            return (
                f"Technical analysis for {sym.upper()}: "
                f"Price: ${summ.get('latest_close', 0.0):,.2f} | "
                f"RSI (14): {summ.get('latest_rsi', 50.0):.1f} ({summ.get('sentiment', 'Neutral')}) | "
                f"MACD Trend: {summ.get('trend', 'Neutral')}."
            )
            
        elif name == "place_paper_trade":
            res = paper_engine.place_order(
                symbol=args.get("symbol", ""),
                shares=float(args.get("shares", 1)),
                side=args.get("side", "BUY"),
                order_type=args.get("order_type", "MARKET"),
                limit_price=args.get("limit_price")
            )
            if broadcast_callback and res.get("success"):
                broadcast_callback({"type": "portfolio_update", "portfolio": res.get("portfolio")})
            return res.get("message", "Order placed.")
            
        elif name == "get_portfolio_summary":
            state = paper_engine.get_portfolio_state()
            ret_str = f"+${state['total_return_dollar']:,.2f} ({state['total_return_pct']}%)" if state['total_return_dollar'] >= 0 else f"-${abs(state['total_return_dollar']):,.2f} ({state['total_return_pct']}%)"
            return (
                f"Virtual Portfolio Summary: Total Value: ${state['total_portfolio_value']:,.2f} | "
                f"Cash: ${state['cash_balance']:,.2f} | Positions: ${state['positions_value']:,.2f} | "
                f"Overall Return: {ret_str} with {len(state['positions'])} active holding(s)."
            )
            
        elif name == "run_desktop_automation":
            from backend.ai import task_planner
            instruction = args.get("instruction", "")
            steps = task_planner.plan_task(instruction)
            if not steps:
                return "I could not generate an execution plan for that automation."
            if broadcast_callback:
                broadcast_callback({"type": "response", "message": f"Executing {len(steps)} automation step(s)...", "role": "jarvis"})
            results = workflow_engine.run_workflow(steps, broadcast_callback)
            return f"Automation completed. Results: {', '.join(str(r) for r in results[:3])}"
            
        elif name == "define_word":
            return web.define_word(args.get("word", ""))
            
        else:
            return f"Tool {name} is not recognized."
    except Exception as e:
        return f"Error executing {name}: {str(e)}"
