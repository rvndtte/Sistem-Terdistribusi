"""RMI dengan Pyro5 - SERVER.
Contoh: python rmi_server.py --host 0.0.0.0 --port 9090 --delay 1
URI objek: PYRO:uts.data@<host>:9090
"""
import argparse
import time

import Pyro5.api


@Pyro5.api.expose
class DataService:
    def __init__(self, delay=0):
        self.delay = delay

    def terima(self, data):
        t = time.strftime("%H:%M:%S")
        print(f"[rmi-server] {t} terima {len(data)} karakter ({len(data)/1024:.0f} KB)")
        if self.delay:
            time.sleep(self.delay)
        return f"OK {len(data)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=9090)
    ap.add_argument("--delay", type=float, default=0)
    args = ap.parse_args()

    daemon = Pyro5.api.Daemon(host=args.host, port=args.port)
    uri = daemon.register(DataService(args.delay), objectId="uts.data")
    print(f"[rmi-server] siap. URI: {uri}  delay={args.delay}s")
    daemon.requestLoop()


if __name__ == "__main__":
    main()