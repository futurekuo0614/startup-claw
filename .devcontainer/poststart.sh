#!/usr/bin/env bash
# Run on every Codespace start — keeps Ollama daemon warm so python main.py
# doesn't pay the cold-start penalty on the first inference call.

if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "[startup-claw] Ollama already running"
else
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    echo "[startup-claw] Ollama daemon started (pid $!)"
fi
