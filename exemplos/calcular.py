"""Exemplo mínimo de integração com a Calculadora de Tributos da Receita Federal.

Uso:  python exemplos/calcular.py [URL_BASE]
Requer: pip install requests
"""
import json
import sys
from pathlib import Path

import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080/api/calculadora"
ESTADOS_OK = {"CALCULADO", "CALCULO_SIMULADO"}


def calcular(operacao: dict) -> dict:
    """Calcula item a item; a resposta é 200 mesmo com itens em erro."""
    r = requests.post(f"{BASE}/observabilidade/regime-geral", json=operacao, timeout=30)
    r.raise_for_status()
    if r.headers.get("x-warning-dados-simulados"):
        print("Aviso:", r.headers["x-warning-dados-simulados"])
    return r.json()


def main() -> None:
    operacao = json.loads((Path(__file__).parent / "operacao.json").read_text(encoding="utf-8"))
    resultado = calcular(operacao)
    for obj in resultado.get("objetos", []):
        estado = obj["estadoItem"]
        marca = "ok " if estado in ESTADOS_OK else "ERRO"
        print(f"[{marca}] item {obj['nObj']}: {estado}")
        for erro in obj.get("erros", []):
            print(f"        {erro['code']} {erro['title']}: {erro['detail']}")
    total = resultado.get("total", {}).get("tribCalc", {}).get("IBSCBSTot", {})
    print("Base IBS/CBS:", total.get("vBCIBSCBS"))
    print("CBS:", total.get("gCBS", {}).get("vCBS"), "| IBS:", total.get("gIBS", {}).get("vIBS"))


if __name__ == "__main__":
    main()
