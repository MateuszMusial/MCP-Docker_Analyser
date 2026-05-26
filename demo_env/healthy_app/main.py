#!/usr/bin/env python3
import time


if __name__ == "__main__":
    while True:
        time.sleep(10)
        print(f"[INFO]--[{time.strftime('%Y-%m-%d %H:%M:%S')}]: Hello from healthy_app!", flush=True)
        