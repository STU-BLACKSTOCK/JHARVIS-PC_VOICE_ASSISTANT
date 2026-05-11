import psutil

def get_system_stats() -> dict:
    try:
        # CPU
        cpu_usage = psutil.cpu_percent(interval=0.5)
        
        # RAM
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_total = round(ram.total / (1024**3), 2)
        ram_used = round(ram.used / (1024**3), 2)
        
        # Battery
        battery_info = "N/A"
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                battery_info = f"{battery.percent}% {'(Plugged In)' if battery.power_plugged else ''}"

        return {
            "cpu_percent": cpu_usage,
            "ram_percent": ram_usage,
            "ram_detail": f"{ram_used}GB / {ram_total}GB",
            "battery": battery_info,
            "gpus": []
        }
    except Exception as e:
        print(f"Error fetching system stats: {e}")
        return {}

def format_system_stats_for_speech() -> str:
    stats = get_system_stats()
    if not stats: return "I am unable to retrieve system statistics at this moment."
    
    response = f"CPU usage is at {stats['cpu_percent']} percent. "
    response += f"RAM usage is at {stats['ram_percent']} percent. "
    if stats['battery'] != 'N/A':
        response += f"Battery is at {stats['battery']}. "
    
    return response
