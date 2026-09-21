#!/usr/bin/env python3
"""Temporary end-to-end write test for the OpenKeychain signing bridge.

Committed, pushed to main, verified on GitHub, then removed in a follow-up
commit. If you are reading this on GitHub, the cleanup commit has not landed.
"""


def main() -> int:
    print("hermes push test: signing via okc-gpg -> OpenKeychain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
