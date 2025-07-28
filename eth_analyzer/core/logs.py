from utils.formatter import clean_hex
from utils.signatures import decode_event_signature

# Load once globally
from utils.signatures import load_signatures
import os

EVENTS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "events.txt")
event_signatures = load_signatures(EVENTS_FILE)

def process_logs(receipt):
    logs = receipt.logs
    print(f"  [LOGS] Found {len(logs)} logs")

    for idx, log in enumerate(logs):
        print(f"    [LOG {idx}] Address: {log.address}")
        topics = [t.hex() for t in log.topics]
        print(f"      Topics: {topics}")

        if topics:
            event_name = decode_event_signature(topics[0], event_signatures)
            print(f"      Decoded Event: {event_name}")
        else:
            print("      No topics found (anonymous event?)")

        print(f"      Data: {clean_hex(log.data)}")

