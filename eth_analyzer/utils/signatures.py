import os

def load_signatures(filepath):
    signatures = {}
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Signature file not found: {filepath}")

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if "|" in line:
                name, selector = line.split("|")
                signatures[selector.lower()] = name
    return signatures

def decode_function_signature(input_data, functions_map):
    if input_data and input_data.startswith("0x") and len(input_data) >= 10:
        selector = input_data[2:10].lower()
        return functions_map.get(selector, f"Unknown Function (0x{selector})")
    return "Unknown Function"

def decode_event_signature(topic_0, events_map):
    topic = topic_0.lower().removeprefix("0x")
    return events_map.get(topic, "Unknown Event")

