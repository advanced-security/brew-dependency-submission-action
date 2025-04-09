#!/bin/bash
set -e

export VENDOR="$(pwd)/vendor"
echo "[+] Vendor path: $VENDOR"

echo "[+] Delete all folders in vendor"
rm -rf "$VENDOR/*/"

if [ -f $PWD/Pipfile ]; then
    echo "[+] Install all dependencies (pipenv)"
    pipenv clean && pipenv install
    pipenv run pip freeze > "$VENDOR/requirements.txt"
    pip install -r "$VENDOR/requirements.txt" --target=$VENDOR --upgrade

elif [ -f $PWD/requirements.txt ]; then
    echo "[+] Install all dependencies (pip -> requirements)"
    pip install -r $PWD/requirements.txt --target=$VENDOR

elif [ -f $PWD/uv.lock ]; then
    echo "[+] Install all dependencies (uv -> requirements)"
 
    uv pip freeze > "$VENDOR/requirements.txt"
    pip install -r "$VENDOR/requirements.txt" --target=$VENDOR --upgrade

else 
    echo "[!] Unsupported Python installer, please update the 'vendor/update.sh' script"
    exit 1
fi


echo "[+] Clean up vendor folder"
rm -rf $VENDOR/*dist-info && \
    rm -rf $VENDOR/requirements.txt

echo "[+] Completed vendor update"
