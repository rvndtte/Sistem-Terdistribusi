#!/bin/bash
# Capture traffic MQTT di loopback untuk uji marshaling, lalu tampilkan isinya.
# Jalankan: sudo -v && bash pubsub/capture_marshaling.sh
cd "$(dirname "$0")/.." || exit 1
PY=./uts-st/bin/python
PCAP=hasil/marshaling_mqtt.pcapng
TEKS="Halo dari publisher"

sudo -n true 2>/dev/null || { echo "Jalankan 'sudo -v' dulu."; exit 1; }

sudo dumpcap -i lo -f "tcp port 1883" -w - > "$PCAP" &
sleep 2

$PY -u pubsub/subscriber.py > hasil/marshaling_subscriber.log 2>&1 &
SUB=$!
sleep 1
$PY pubsub/publisher.py --text "$TEKS" --qos 0 > /dev/null
$PY pubsub/publisher.py --text "$TEKS" --qos 1 > /dev/null
sleep 1

kill $SUB 2>/dev/null
sudo pkill -INT -x dumpcap
sleep 1
[ -s "$PCAP" ] || { echo "GAGAL: file capture kosong (lihat pesan dumpcap di atas)."; exit 1; }

echo; echo "===== Ringkasan paket MQTT ====="
tshark -r "$PCAP" -Y mqtt
echo; echo "===== Detail paket PUBLISH (QoS 1) ====="
tshark -r "$PCAP" -Y "mqtt.msgtype == 3 && mqtt.qos == 1" -V -x | grep -vE "^\s*$"
echo; echo "===== Detail paket PUBACK ====="
tshark -r "$PCAP" -Y "mqtt.msgtype == 4" -V | grep -E "Frame Number|Transmission Control|Source Port|Destination Port|MQ Telemetry|Header Flags|Msg Len|Message Identifier"
echo; echo "File capture: $PCAP"
