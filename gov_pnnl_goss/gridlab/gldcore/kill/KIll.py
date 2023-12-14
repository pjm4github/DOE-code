import sys
import os
import signal


def main():
    if len(sys.argv) != 3:
        print("Syntax: python kill.py -[<signum>|<signame>] <pid>")
        sys.exit(1)

    signal_str = sys.argv[1]
    pid_str = sys.argv[2]

    if signal_str.startswith("-"):
        signal_str = signal_str[1:]  # Remove the leading "-"

    try:
        pid = int(pid_str)
    except ValueError:
        print(f"kill: invalid PID '{pid_str}'")
        sys.exit(1)

    if signal_str.isdigit():
        sig = int(signal_str)
    else:
        # Lookup the signal by name
        signame = signal_str.upper()
        if hasattr(signal, signame):
            sig = getattr(signal, signame)
        else:
            print(f"kill: signal {signal_str} is not recognized")
            sys.exit(1)

    try:
        os.kill(pid, sig)
    except ProcessLookupError:
        print(f"kill: process with PID {pid} not found")
        sys.exit(1)

    print()


if __name__ == "__main__":
    main()
