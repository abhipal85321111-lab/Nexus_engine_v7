import struct
import numpy as np
import time

class NexusV7_RealEngine:
    """V7.2 PRO - Real 50k ingest - Zero JSON, Zero Python Loop - FIXED"""
    PACKET_FMT = "!I B f"
    PACKET_SIZE = 9
    
    def ingest_50k(self, binary_stream: bytes):
        count = len(binary_stream) // self.PACKET_SIZE
        start = time.perf_counter()
        
        # FIXED: Explicit offsets = No numpy padding, 100% 9 bytes match
        dt = np.dtype({
            'names': ['id', 'type', 'value'],
            'formats': ['>u4', 'u1', '>f4'],
            'offsets': [0, 4, 5], # 0,4,5 = Exactly 9 bytes, no padding
            'itemsize': 9
        })
        
        arr = np.frombuffer(binary_stream, dtype=dt).copy()
        
        # REAL VECTORIZED - C level me 50k *2
        arr['value'] *= 2
        
        duration = time.perf_counter() - start
        
        print(f"[V7.2 FIXED] Ingested {count} BINARY packets")
        print(f"Size: {len(binary_stream)/1024:.0f}KB | Time: {duration*1000:.2f}ms")
        print(f"Throughput: {count/duration:,.0f} pkt/sec | Zero Python Loop")
        print(f"Sample: ID={arr[0]['id']} -> {arr[-1]['id']} | Value*2={arr[0]['value']:.2f}")
        return arr

# ========== REAL TEST ==========
print(f"--- V7.2 PRO TEST ---")
PACKET_FMT = "!I B f"
packets = b''.join([struct.pack(PACKET_FMT, i, 1, 99.99) for i in range(50000)])
print(f"Packed: 50k * 9B = {len(packets)/1024:.0f}KB (JSON = ~1.5MB)")
v7 = NexusV7_RealEngine()
result = v7.ingest_50k(packets)
