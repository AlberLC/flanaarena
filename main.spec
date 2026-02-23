import os
import zipfile
from pathlib import Path

from flanaarena import constants
from flanaarena.utils import system

DIST_RESOURCES_PATH = constants.APP_PATH / constants.PYINSTALLER_INTERNAL_NAME / 'resources'
CONFIG_PATH = DIST_RESOURCES_PATH / 'config.json'

EXCLUDED_DIRECTORY_PATHS = set()
EXCLUDED_FILE_PATHS = {constants.CONFIG_PATH}


def get_datas() -> list[tuple[Path, Path]]:
    datas = []

    for root_name, directory_names, file_names in os.walk(constants.RESOURCES_PATH):
        root_path = Path(root_name)
        if root_path in EXCLUDED_DIRECTORY_PATHS:
            directory_names.clear()
            continue

        for file_name in file_names:
            file_path = Path(root_path, file_name)

            if file_path in EXCLUDED_FILE_PATHS:
                continue

            datas.append((file_path, root_path.relative_to(constants.SOURCE_PATH)))

    return datas


def zip_app() -> None:
    with zipfile.ZipFile(constants.APPS_PATH.with_suffix('.zip'), 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for path in constants.APPS_PATH.rglob('*'):
            if path.is_file():
                zip_file.write(path, path.relative_to(constants.DIST_PATH))


savable_data = system.read_savable_files((CONFIG_PATH,))

# ---------------------------------------------
# -------------------- APP --------------------
# ---------------------------------------------
a = Analysis(
    ['flanaarena\\main.py'],
    pathex=[],
    binaries=[],
    datas=get_datas(),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],  # Keep it consistent with the above (optimize=) so that Python preserves the correct flag at runtime even if it is never going to be used
    exclude_binaries=True,
    name='FlanaArena',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='flanaarena/resources/images/logo.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FlanaArena',
)

# -------------------------------------------------
# -------------------- UPDATER --------------------
# -------------------------------------------------
a = Analysis(
    ['flanaarena/updater_main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],  # Keep it consistent with the above (optimize=) so that Python preserves the correct flag at runtime even if it is never going to be used
    exclude_binaries=True,
    name='Updater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='flanaarena/resources/images/logo.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Updater',
)

# -------------------------------------------------
# -------------------- COMBINE --------------------
# -------------------------------------------------
import shutil

from flanaarena import constants

TEMPORARY_PATH = constants.DIST_PATH / f'{constants.APP_NAME}_'

shutil.move(constants.DIST_PATH / constants.APP_NAME, TEMPORARY_PATH / constants.APP_NAME)
shutil.move(constants.DIST_PATH / constants.UPDATER_APP_NAME, TEMPORARY_PATH / constants.UPDATER_APP_NAME)
TEMPORARY_PATH.rename(constants.APPS_PATH)

# -------------------------------------------------
# -------------------- PREPARE --------------------
# -------------------------------------------------
zip_app()
system.write_savable_files(savable_data)
