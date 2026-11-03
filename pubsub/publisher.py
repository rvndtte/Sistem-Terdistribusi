import argparse
import os
import sys
import time

import paho.mqtt.client as mqtt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.generator import generate

parser = argparse.ArgumentParser(description="MQTT publisher")
parser.add_argument("--host", default="localhost", help="alamat broker")
parser.add_argument("--port", type=int, default=1883)
parser.add_argument("--topic", default="uts/data")
parser.add_argument("--size", type=int, default=200, help="ukuran data (KB): 200/400/600/800/1000")
parser.add_argument("--qos", type=int, default=1, choices=[0, 1])
parser.add_argument("--repeat", type=int, default=1, help="jumlah pengiriman (5 untuk uji sync/async)")
parser.add_argument("--interval", type=float, default=0, help="jeda (detik) antar pengiriman")
parser.add_argument("--text", help="kirim teks ini saja (untuk uji marshaling), abaikan --size")
args = parser.parse_args()

payload = args.text if args.text else generate(args.size)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(args.host, args.port)
client.loop_start()

print(f"Publish ke {args.host}:{args.port} topik '{args.topic}', "
      f"{len(payload) / 1024:.1f} KB, QoS {args.qos}, {args.repeat}x")
mulai = time.time()
for i in range(1, args.repeat + 1):
    t0 = time.time()
    info = client.publish(args.topic, payload, qos=args.qos)
    info.wait_for_publish()  # QoS 1: menunggu PUBACK dari broker
    print(f"[{time.strftime('%H:%M:%S')}] kirim #{i} selesai, {time.time() - t0:.3f} detik "
          f"(+{time.time() - mulai:.3f}s sejak mulai)")
    if args.interval and i < args.repeat:
        time.sleep(args.interval)

print(f"Total waktu: {time.time() - mulai:.3f} detik")
client.loop_stop()
client.disconnect()
