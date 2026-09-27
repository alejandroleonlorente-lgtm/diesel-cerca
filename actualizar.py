"""Descarga los precios del Ministerio (MITECO) y genera data/diesel.json.

Se ejecuta solo en GitHub Actions cada hora. Guarda los precios de diésel
(Gasóleo A) y gasolina 95 E5 de todas las gasolineras públicas de España y calcula
la variación respecto al último precio del día anterior.
"""
import json
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

URL = ("https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/"
       "PreciosCarburantes/EstacionesTerrestres/")
DATA = Path(__file__).resolve().parent / "data"
SALIDA = DATA / "diesel.json"
HISTORICO = DATA / "historico2.json"  # v2: diésel + gasolina 95


def descargar():
    req = urllib.request.Request(URL, headers={
        "User-Agent": "Mozilla/5.0 (DieselCerca; uso personal)",
        "Accept": "application/json",
    })
    ultimo = None
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8-sig"))
        except Exception as e:  # noqa: BLE001
            ultimo = e
            time.sleep(10 * (intento + 1))
    raise SystemExit(f"No se pudo descargar la API: {ultimo}")


def num(s):
    if s in (None, ""):
        return None
    try:
        v = float(str(s).replace(",", "."))
    except ValueError:
        return None
    return v if v > 0 else None


def coord(s):
    try:
        return float(str(s).replace(",", "."))
    except (TypeError, ValueError):
        return None


def main():
    datos = descargar()
    hoy = datetime.now(ZoneInfo("Europe/Madrid")).date().isoformat()

    try:
        historico = json.loads(HISTORICO.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        historico = {}
    dias_previos = sorted(d for d in historico if d < hoy)
    ayer = historico.get(dias_previos[-1], {}) if dias_previos else {}

    estaciones, snapshot = [], {}
    for e in datos.get("ListaEESSPrecio", []):
        if e.get("Tipo Venta") and e.get("Tipo Venta") != "P":
            continue  # cooperativas y venta restringida
        a, p = num(e.get("Precio Gasoleo A")), num(e.get("Precio Gasolina 95 E5"))
        lat, lon = coord(e.get("Latitud")), coord(e.get("Longitud (WGS84)"))
        if (a is None and p is None) or lat is None or lon is None:
            continue
        i = e.get("IDEESS")
        prev = ayer.get(i, [None, None])
        da = round(a - prev[0], 3) if a is not None and prev[0] is not None else None
        dp = round(p - prev[1], 3) if p is not None and prev[1] is not None else None
        estaciones.append([
            i, round(lat, 5), round(lon, 5), a, p, da, dp,
            (e.get("Rótulo") or "").strip(), (e.get("Dirección") or "").strip(),
            (e.get("Localidad") or "").strip(), (e.get("Horario") or "").strip(),
        ])
        snapshot[i] = [a, p]

    if len(estaciones) < 1000:
        raise SystemExit(f"Respuesta sospechosa: solo {len(estaciones)} estaciones")

    historico[hoy] = snapshot
    historico = {d: historico[d] for d in sorted(historico)[-2:]}

    DATA.mkdir(exist_ok=True)
    SALIDA.write_text(json.dumps({
        "v": 2,
        "actualizado": datos.get("Fecha"),
        "estaciones": estaciones,
    }, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    HISTORICO.write_text(json.dumps(historico, separators=(",", ":")), encoding="utf-8")
    print(f"{len(estaciones)} estaciones · {datos.get('Fecha')}")


if __name__ == "__main__":
    main()
