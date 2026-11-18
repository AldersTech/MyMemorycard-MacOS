#!/bin/sh
# Build self-contained mymc executables with PyInstaller.
#
#   dist/MyMemorycard.app - the Qt GUI as a double-clickable macOS app
#   dist/mymc       - the command line tool as one file
#
# Neither needs Python installed on the machine that runs it.
# Run from the project root:  sh tools/build_standalone.sh
set -e
cd "$(dirname "$0")/.."

PY=.venv/bin/python
[ -x "$PY" ] || python3 -m venv .venv
"$PY" -m pip install -q -e ".[gui]" pyinstaller

WORK="$PWD/build/pyinstaller"
mkdir -p "$WORK"

# Small launcher scripts: PyInstaller needs a file to start from.
cat > "$WORK/mymc_gui.py" <<'EOF'
import sys
from mymc.cli import main_gui
sys.exit(main_gui())
EOF
cat > "$WORK/mymc_cli.py" <<'EOF'
import sys
from mymc.cli import main
sys.exit(main())
EOF

# Render the app icon with the project's own drawing code.
"$PY" - "$WORK" <<'EOF'
import os, sys
sys.argv = sys.argv[:1] + ["--output", sys.argv[1]]
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, "tools")
import make_app
make_app.build_icns(sys.argv[2])
EOF

# Qt modules the GUI never imports; leaving them out keeps the app small.
EXCLUDES=""
for m in QtWebEngineCore QtWebEngineWidgets QtWebEngineQuick Qt3DCore Qt3DRender \
         QtQuick QtQml QtQuick3D QtMultimedia QtCharts QtDataVisualization \
         QtPdf QtBluetooth QtPositioning QtSensors QtSerialPort QtSql QtTest; do
    EXCLUDES="$EXCLUDES --exclude-module PySide6.$m"
done

# GUI: a windowed .app bundle
"$PY" -m PyInstaller --noconfirm --clean --windowed \
    --name MyMemorycard --icon "$WORK/mymc.icns" \
    --osx-bundle-identifier org.publicdomain.mymc \
    --exclude-module tkinter $EXCLUDES \
    --workpath "$WORK/gui" --specpath "$WORK" --distpath dist \
    "$WORK/mymc_gui.py"

# Add file associations and the version to the app's Info.plist.
"$PY" - <<'EOF'
import plistlib, sys
sys.path.insert(0, "tools"); sys.path.insert(0, "src")
import make_app
from mymc import __version__
path = "dist/MyMemorycard.app/Contents/Info.plist"
with open(path, "rb") as f:
    info = plistlib.load(f)
info.update({
    "CFBundleName": "MyMemorycard",
    "CFBundleDisplayName": "MyMemorycard",
    "CFBundleDocumentTypes": make_app.document_types(),
    "CFBundleVersion": __version__,
    "CFBundleShortVersionString": __version__,
    "NSRequiresAquaSystemAppearance": False,
    "LSMinimumSystemVersion": "11.0",
})
with open(path, "wb") as f:
    plistlib.dump(info, f)
EOF

# CLI: one self-contained file, no Qt (it isn't needed for the command line)
"$PY" -m PyInstaller --noconfirm --clean --onefile \
    --name mymc --exclude-module PySide6 --exclude-module tkinter \
    --workpath "$WORK/cli" --specpath "$WORK" --distpath dist/cli \
    "$WORK/mymc_cli.py"
mv dist/cli/mymc dist/mymc-cli && rmdir dist/cli

# Ad-hoc sign so macOS will launch the edited bundle on this Mac.
codesign --force --deep --sign - dist/MyMemorycard.app >/dev/null 2>&1 || true

echo
echo "Built:"
echo "  dist/MyMemorycard.app   (double-click, or drag into /Applications)"
echo "  dist/mymc-cli   (run: ./dist/mymc-cli Mcd001.ps2 dir)"
