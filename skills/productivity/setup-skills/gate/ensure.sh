#!/bin/bash
# Mounts the gate's toolchain. Idempotent: decides by a seal, `.installed`,
# holding the hash of the package-lock.json the tree was installed from.
# A lock that moves (git pull, cold start — the same event) moves the hash.
#
# Exit 0 = the gate is mounted. Exit 1 = it is not, and stdout says why in one
# line. It emits no verdict and writes no report: that is gate.sh's job.
set -u

GATE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$GATE_DIR" || { echo "gate: no se pudo entrar en $GATE_DIR"; exit 1; }

[ -f package-lock.json ] || { echo "gate: falta package-lock.json en $GATE_DIR"; exit 1; }
command -v npm > /dev/null || { echo "gate: falta npm en el PATH"; exit 1; }

if command -v shasum > /dev/null; then
  HASH="$(shasum -a 256 package-lock.json | awk '{ print $1 }')"
elif command -v sha256sum > /dev/null; then
  HASH="$(sha256sum package-lock.json | awk '{ print $1 }')"
else
  echo "gate: no hay shasum ni sha256sum para sellar la instalacion"; exit 1
fi

if [ -d node_modules ] && [ -f .installed ] && [ "$(cat .installed)" = "$HASH" ]; then
  exit 0
fi

# --omit=peer en las dos operaciones: sin el, npm autoinstala el peer y mete un
# vitest propio en el gate, que correria los tests del proyecto con una version
# que el proyecto no eligio.
if ! npm ci --omit=peer --no-audit --no-fund > /dev/null 2> ensure.err; then
  echo "gate: 'npm ci --omit=peer' fallo — ver $GATE_DIR/ensure.err"
  exit 1
fi

rm -f ensure.err
printf '%s\n' "$HASH" > .installed
