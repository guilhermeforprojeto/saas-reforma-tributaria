#!/usr/bin/env bash
# Envia exemplos/operacao.json para a calculadora local e mostra o estado de cada item.
# Uso: bash exemplos/calcular.sh [URL_BASE]   (padrão: http://localhost:8080/api/calculadora)
set -euo pipefail
BASE="${1:-http://localhost:8080/api/calculadora}"
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Versão da calculadora:"
curl -fsS "$BASE/dados-abertos/versao" || echo "(endpoint de versão indisponível)"
echo

echo "Cálculo com observabilidade (erros por item, sem derrubar a operação):"
curl -fsS -X POST "$BASE/observabilidade/regime-geral" \
  -H 'Content-Type: application/json' \
  -d @"$DIR/operacao.json" \
| python3 -c '
import json, sys
r = json.load(sys.stdin)
for o in r.get("objetos", []):
    print("item", o.get("nObj"), o.get("estadoItem"))
    for e in o.get("erros", []):
        print("   ", e.get("code"), e.get("detail"))
tot = r.get("total", {}).get("tribCalc", {}).get("IBSCBSTot", {})
print("CBS total:", tot.get("gCBS", {}).get("vCBS"), "| IBS total:", tot.get("gIBS", {}).get("vIBS"))
'
