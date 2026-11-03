"""RMI dengan Pyro5 - CLIENT.

Contoh:
  python rmi/client.py --sizes 200 400 600 800 1000
  python rmi/client.py --text "Halo dari client"
  python rmi/client.py --sizes 200 --count 5
"""
import argparse
import random
import string
import time

import Pyro5.api


def make_data(kb):
    return "".join(random.choices(string.ascii_letters + string.digits, k=kb * 1024))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=9090)
    ap.add_argument("--sizes", type=int, nargs="*", default=[])
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--text")
    args = ap.parse_args()

    proxy = Pyro5.api.Proxy(f"PYRO:uts.data@{args.host}:{args.port}")
    payloads = []
    if args.text:
        payloads.append(("teks", args.text))
    for kb in args.sizes:
        payloads.append((f"{kb} KB", make_data(kb)))

    t_all = time.perf_counter()
    for label, data in payloads:
        for i in range(1, args.count + 1):
            t0 = time.perf_counter()
            hasil = proxy.terima(data)  # BLOCKING sampai method remote selesai
            dt = time.perf_counter() - t0
            print(f"[rmi-client] {label} #{i}: waktu sampai return={dt:.4f}s, hasil={hasil}")
    print(f"[rmi-client] total waktu = {time.perf_counter() - t_all:.4f}s")


if __name__ == "__main__":
    main()