import subprocess
import sys
from pathlib import Path

SPEC_PATH = Path('main.spec')


def main() -> None:
    package()


def package() -> None:
    subprocess.check_call([sys.executable, '-m', 'PyInstaller', SPEC_PATH, '--clean', '--noconfirm'])


if __name__ == '__main__':
    main()
