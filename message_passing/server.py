"""Message passing (socket TCP) - SERVER.
Protokol: [4 byte panjang big-endian][payload]. Server membalas "ACK" setelah
selesai memproses pesan (sinkron: client menunggu balasan ini).

Contoh: python message_passing/server.py --port 5000 --delay 1
"""
import argparse
import socket
import struct
import time


def recv_exact(conn, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = conn.recv(min(65536, n - len(buf)))
        if not chunk:
            raise ConnectionError("koneksi terputus")
        buf.extend(chunk)
    return bytes(buf)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--delay", type=float, default=0, help="sleep (detik) sebelum ACK")
    args = ap.parse_args()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.host, args.port))
    srv.listen(5)
    print(f"[server] listen di {args.host}:{args.port}, delay={args.delay}s")

    while True:
        conn, addr = srv.accept()
        print(f"[server] koneksi dari {addr}")
        try:
            while True:
                header = conn.recv(4)
                if not header:
                    break
                if len(header) < 4:
                    header += recv_exact(conn, 4 - len(header))
                size = struct.unpack("!I", header)[0]
                data = recv_exact(conn, size)
                t = time.strftime("%H:%M:%S")
                print(f"[server] {t} terima {len(data)} byte ({len(data)/1024:.0f} KB)")
                if args.delay:
                    time.sleep(args.delay)
                conn.sendall(b"ACK")
        except ConnectionError as e:
            print(f"[server] {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    main()