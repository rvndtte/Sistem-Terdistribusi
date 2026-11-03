import argparse
import random
import string

UKURAN_UJI_KB = [200, 400, 600, 800, 1000]


def generate(size_kb, seed=42):
    """Hasilkan teks acak (ASCII) berukuran tepat size_kb KB (1 KB = 1024 byte)."""
    rng = random.Random(seed)
    huruf = string.ascii_letters + string.digits
    return "".join(rng.choices(huruf, k=size_kb * 1024))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generator data uji")
    parser.add_argument("size_kb", type=int, nargs="?", help="ukuran data (KB)")
    parser.add_argument("--simpan", action="store_true", help="simpan ke file data_<ukuran>kb.txt")
    args = parser.parse_args()

    for kb in [args.size_kb] if args.size_kb else UKURAN_UJI_KB:
        data = generate(kb)
        print(f"{kb} KB -> {len(data.encode())} byte")
        if args.simpan:
            with open(f"data_{kb}kb.txt", "w") as f:
                f.write(data)
