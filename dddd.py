import pydivert
import threading
import time
import random
from pynput import mouse

ms = 4800
drop = 1.0
throttle = 0.25
ip = "ip"
lag = False
packets = []

def main():
    with pydivert.WinDivert(ip) as w:
        while True:
            try: pkt = w.recv()
            except: break
            if not lag:
                try: w.send(pkt)
                except: pass
                continue
            if pkt.is_inbound:
                if random.random() >= drop: packets.append((time.time() + ms / 1000, w, pkt))
            elif random.random() <= throttle:
                try: w.send(pkt)
                except: pass

def send():
    while True:
        now = time.time()
        packets[:] = [(t, w, p) for t, w, p in packets if now < t or not (lambda: w.send(p) or True)()]
        time.sleep(0.01)

threading.Thread(target=main, daemon=True).start()
threading.Thread(target=send, daemon=True).start()
mouse.Listener(on_click=lambda x, y, b, p: globals().update(lag=not lag) if p and b == mouse.Button.x1 else None).start()
print("XButton1 = lag yo shit")
while True: time.sleep(1)
