import argparse
import time

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser(description="MQTT subscriber")
parser.add_argument("--host", default="localhost", help="alamat broker")
parser.add_argument("--port", type=int, default=1883)
parser.add_argument("--topic", default="uts/data")
parser.add_argument("--qos", type=int, default=1, choices=[0, 1])
parser.add_argument("--delay", type=float, default=0, help="sleep (detik) setiap pesan diterima")
args = parser.parse_args()

jumlah = 0


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Terhubung ke broker {args.host}:{args.port} ({reason_code})")
    client.subscribe(args.topic, qos=args.qos)
    print(f"Subscribe topik '{args.topic}' QoS {args.qos}, delay {args.delay}s. Ctrl+C untuk berhenti.")


def on_message(client, userdata, msg):
    global jumlah
    jumlah += 1
    print(f"[{time.strftime('%H:%M:%S')}] pesan #{jumlah} diterima: "
          f"{len(msg.payload) / 1024:.0f} KB (QoS {msg.qos})")
    if args.delay:
        time.sleep(args.delay)  # simulasi subscriber lambat
        print(f"[{time.strftime('%H:%M:%S')}] selesai memproses pesan #{jumlah}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(args.host, args.port)
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nBerhenti.")
