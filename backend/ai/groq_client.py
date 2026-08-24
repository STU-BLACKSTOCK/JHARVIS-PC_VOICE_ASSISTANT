import os
import json
from groq import Groq
from dotenv import load_dotenv
from backend.productivity import notes_tasks
from backend.ai.tools import AVAILABLE_TOOLS, dispatch_tool_call

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    client = None
    print(f"Failed to initialize Groq client: {e}")

_resolved_model = None

def get_active_model() -> str:
    """Dynamically resolves the best active model available on the user's Groq key."""
    global _resolved_model
    if _resolved_model:
        return _resolved_model

    # Check env override
    env_model = os.getenv("GROQ_MODEL")
    if env_model:
        _resolved_model = env_model
        return _resolved_model

    candidates = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3.6-27b",
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama3-70b-8192",
        "llama-3.1-8b-instant"
    ]

    if client:
        try:
            available = [m.id for m in client.models.list().data]
            for cand in candidates:
                if cand in available:
                    _resolved_model = cand
                    print(f"[Groq AI Brain]: Selected active model '{_resolved_model}'")
                    return _resolved_model
        except Exception:
            pass

    _resolved_model = "openai/gpt-oss-120b"
    return _resolved_model

# In-memory sliding window conversation buffer
_conversation_history = []
MAX_HISTORY_TURNS = 12

SYSTEM_PROMPT = """You are J.A.R.V.I.S., an elite AI desktop companion, executive trading assistant, and autonomous operations agent.
You have access to tools for productivity (notes, tasks, email, alarms, clipboard), system hardware telemetry, market data, paper trading execution, technical analysis (RSI, MACD, EMA), and desktop automation.
- Keep responses concise, clear, and professional.
- Whenever a user asks to take a note, track a task, check stock/crypto prices, run technical analysis, buy/sell paper stocks, or automate something, ALWAYS invoke the appropriate tool.
- Speak directly, confidently, and efficiently like J.A.R.V.I.S.
"""

def reset_conversation():
    global _conversation_history
    _conversation_history = []

def aiProcess(command: str, broadcast_callback=None) -> str:
    """
    Processes natural language commands using Groq LLaMA 3.3 with multi-turn memory
    and autonomous tool calling.
    """
    if not client:
        return "Groq API key is not configured in .env. Please set GROQ_API_KEY."

    global _conversation_history

    # Append user turn
    _conversation_history.append({"role": "user", "content": command})
    notes_tasks.log_conversation("user", command)

    # Trim history to sliding window
    trimmed_history = _conversation_history[-MAX_HISTORY_TURNS:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + trimmed_history

    active_model = get_active_model()

    try:
        # Step 1: Initial call with tools
        completion = client.chat.completions.create(
            messages=messages,
            model=active_model,
            tools=AVAILABLE_TOOLS,
            tool_choice="auto",
            temperature=0.6,
            max_tokens=800,
        )

        response_message = completion.choices[0].message

        # Step 2: Check if tool calling was triggered
        if response_message.tool_calls:
            # Add assistant's tool call intent to messages
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                func_name = tool_call.function.name
                try:
                    func_args = json.loads(tool_call.function.arguments)
                except Exception:
                    func_args = {}

                if broadcast_callback:
                    broadcast_callback({
                        "type": "tool_executing",
                        "tool": func_name,
                        "args": func_args
                    })

                # Dispatch tool
                tool_output = dispatch_tool_call(func_name, func_args, broadcast_callback)

                # Append tool result turn
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": str(tool_output)
                })

            # Step 3: Second call to generate final answer with tool data
            second_completion = client.chat.completions.create(
                messages=messages,
                model=active_model,
                tools=AVAILABLE_TOOLS,
                temperature=0.6,
                max_tokens=600,
            )
            final_reply = second_completion.choices[0].message.content or tool_output
        else:
            final_reply = response_message.content or "Task acknowledged."

        # Append assistant turn to history
        _conversation_history.append({"role": "assistant", "content": final_reply})
        notes_tasks.log_conversation("jarvis", final_reply)
        return final_reply

    except Exception as e:
        print(f"Groq tool-calling agent notice ({e}), retrying direct completion...")
        # Fallback to direct chat
        try:
            fallback = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": command}
                ],
                model=active_model,
                temperature=0.7,
                max_tokens=500,
            )
            ans = fallback.choices[0].message.content
            _conversation_history.append({"role": "assistant", "content": ans})
            return ans
        except Exception as fb_err:
            return f"I'm having trouble connecting to my neural network: {fb_err}"

