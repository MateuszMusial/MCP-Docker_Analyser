#!/usr/bin/env python3
"""
This is a simple Python application that simulates a healthy app by printing a message every 10 seconds.
It can be used to demonstrate the concept of a healthy application in a containerized environment."""

import time
import random


EVENTS = [
    ("[INFO] ", "Processed request in {ms}ms"),
    ("[INFO] ", "Database connection pool: {n}/10 active"),
    ("[DEBUG]", "Cache hit ratio: {pct}%"),
    ("[WARN] ", "Response time slightly elevated: {ms}ms"),
]


def main():
    print(f" [INFO] [{time.strftime('%Y-%m-%d %H:%M:%S')}]: healthy_app started!", flush=True)
    while True:
        time.sleep(random.uniform(5, 15))
        template, msg = random.choice(EVENTS)
        filled = msg.format(ms=random.randint(12, 340), n=random.randint(1, 9), pct=random.randint(70, 99))
        line = f"{template} [{time.strftime('%Y-%m-%d %H:%M:%S')}]: {filled}"
        print(line, flush=True)


if __name__ == "__main__":
    main()
