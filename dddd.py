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
run = True
packets = []

def send():
    while run:
        now = time.time()
        for i in range(len(packets) - 1, -1, -1):
            if now >= packets[i][0]:
                try:
                    packets[i][1].send(packets[i][2])
                except:
                    pass
                packets.pop(i)
        time.sleep(0.01)

def main():
    with pydivert.WinDivert(ip) as w:
        while run:
            try:
                pkt = w.recv()
            except:
                break
            
            if not lag:
                w.send(pkt)
                continue
            
            if pkt.is_inbound:
                if random.random() < drop:
                    continue
                packets.append((time.time() + ms / 1000, w, pkt))
            else:
                if random.random() <= throttle:
                    w.send(pkt)

def click(x, y, button, pressed):
    global lag
    if pressed and button == mouse.Button.x1:
        lag = not lag

threading.Thread(target=main, daemon=True).start()
threading.Thread(target=send, daemon=True).start()
mouse.Listener(on_click=click).start()
print("XButton1 = lag yo shit")
while True:

    time.sleep(1)
