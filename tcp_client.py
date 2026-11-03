"""Message passing (socket TCP) - CLIENT.

Contoh:
  python tcp_client.py --sizes 200 400 600 800 1000        # uji ukuran data
  python tcp_client.py --text "Halo dari client"            # uji marshaling
  python tcp_client.py --sizes 200 --count 5                # uji sync (server pakai --delay)
"""
import argparse
import random
import socket
import string
import struct
import time


def make_data(kb):
    return "".join(random.choices(string.ascii_letters + string.digits, k=kb * 1024)).encode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--sizes", type=int, nargs="*", default=[], help="ukuran data dalam KB")
    ap.add_argument("--count", type=int, default=1, help="jumlah pengiriman per ukuran")
    ap.add_argument("--text", help="kirim teks pendek (untuk marshaling)")
    args = ap.parse_args()

    s = socket.create_connection((args.host, args.port))
    payloads = []
    if args.text:
        payloads.append(("teks", args.text.encode()))
    for kb in args.sizes:
        payloads.append((f"{kb} KB", make_data(kb)))

    t_all = time.perf_counter()
    for label, data in payloads:
        for i in range(1, args.count + 1):
            t0 = time.perf_counter()
            s.sendall(struct.pack("!I", len(data)) + data)
            t_send = time.perf_counter() - t0
            reply = s.recv(3)  # BLOCKING: menunggu ACK dari server
            t_ack = time.perf_counter() - t0
            print(f"[client] {label} #{i}: kirim={t_send:.4f}s, sampai ACK={t_ack:.4f}s, balasan={reply!r}")
    print(f"[client] total waktu = {time.perf_counter() - t_all:.4f}s")
    s.close()


if __name__ == "__main__":
    main()