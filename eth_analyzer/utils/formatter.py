def clean_hex(data):
    if isinstance(data, bytes):
        return "0x" + data.hex()
    elif isinstance(data, str):
        if data.startswith("0x"):
            return data
        else:
            return "0x" + data
    else:
        return str(data)

def format_time_ago(seconds):
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

