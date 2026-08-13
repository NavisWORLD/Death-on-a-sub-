from __future__ import annotations

import multiprocessing
import os
import sys


def _prepare_gui_runtime() -> None:
    multiprocessing.freeze_support()
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")


def run() -> int:
    _prepare_gui_runtime()
    from heartlight.home_app import main

    return main()


if __name__ == "__main__":
    raise SystemExit(run())
