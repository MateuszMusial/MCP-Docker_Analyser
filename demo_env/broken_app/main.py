#!/usr/bin/env python3
"""
Python application that simulates a broken app by attempting to connect to a non-existent database and crashing after several failed attempts.
It can be used to demonstrate the concept of an unhealthy application in a containerized environment.
"""
import time
import sys


RETRY_LIMIT = 5


def try_connect_db():
    """
    Simulates a database connection attempt that always fails.
    """
    raise ConnectionRefusedError("Connection refused (host=db, port=5432)")

def main():
    attempt = 0
    while attempt < RETRY_LIMIT:
        try:
            try_connect_db()
        except ConnectionRefusedError as e:
            attempt += 1
            print(f"[ERROR] [{time.strftime('%Y-%m-%d %H:%M:%S')}]: DB connection failed ({attempt}/{RETRY_LIMIT}): {e}", 
                  file=sys.stderr, flush=True)
            time.sleep(5)

    print(f"[CRITICAL] [{time.strftime('%Y-%m-%d %H:%M:%S')}]: Too many failures — exiting", file=sys.stderr, flush=True)
    sys.exit(1)

if __name__ == "__main__":
    main()
