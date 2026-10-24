import json
import copy

class NexusV9_DeltaSync:
    """V9 PRO - Transmits only modified data - 100% Real"""

    def __init__(self):
        self.state = {}
        self.stats = {"total_syncs": 0, "zero_packets": 0, "bytes_saved": 0}

    def sync(self, client_id: str, new_data: dict) -> dict:
        old_data = self.state.get(client_id, {})

        # REAL DELTA - Added + Modified
        delta = {k: v for k, v in new_data.items() if old_data.get(k) != v}

        # REAL DELTA - Deleted keys (ye tera wala miss karta hai)
        for k in old_data:
            if k not in new_data:
                delta[k] = None  # None = Deleted

        # Deep copy - Bug fix
        self.state[client_id] = copy.deepcopy(new_data)

        # Stats
        self.stats["total_syncs"] += 1
        if not delta:
            self.stats["zero_packets"] += 1
        else:
            # Kitna bachaya
            full_size = len(json.dumps(new_data).encode())
            delta_size = len(json.dumps(delta).encode())
            self.stats["bytes_saved"] += (full_size - delta_size)

        if delta:
            print(f"[v9] Delta: {delta} | Saved {full_size - delta_size} bytes")
        else:
            print(f"[v9] Delta: {{}} -> 0 bytes dispatched (100% saved)")

        return delta

# ========== TERA TEST CASE ==========
v9 = NexusV9_DeltaSync()

print("1. First sync - Full data:")
v9.sync("user_1", {"cart": 2, "status": "active"})

print("\n2. Second sync - Same data:")
v9.sync("user_1", {"cart": 2, "status": "active"})

print("\n3. Third sync - Cart changed:")
v9.sync("user_1", {"cart": 3, "status": "active"})

print("\n4. Fourth sync - Status deleted:")
v9.sync("user_1", {"cart": 3})

print(f"\nStats: {v9.stats}")
