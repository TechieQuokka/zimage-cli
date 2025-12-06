#!/usr/bin/env python3
"""
Z-Image Turbo Generator
Entry point for CLI
"""

import sys
from pathlib import Path

# Add package to path for direct script execution
sys.path.insert(0, str(Path(__file__).parent))

from cli import CLI


def main() -> int:
    return CLI().run()


if __name__ == "__main__":
    sys.exit(main())
