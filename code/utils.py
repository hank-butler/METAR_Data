import re
from pathlib import Path
import pandas as pd


def create_map(map_file=None, latitude=None, longitude=None, zoom=4):
    '''
    Function to take in geojson file and create a map using Folium with coordinate to center.
    
    Zoom is defaulted to 4 based on trial and error.
    
    =======
    ACCEPTS
    =======
    map_file should be a .geojson file
    latitude and longitude should be coordinates from a pandas dataframe
    
    =======
    RETURNS
    =======
    A folium map centered at coordinates and added to map with a geojson file.
    
    =======
    RAISES
    =======
    ValueError if map_file, latitude, longitude aren't correct data types
    ModuleNotFoundError if json and Folium aren't imported before invoking
    
    '''
    import folium
    import json
    
    if map_file:
        json_map = json.load(open(map_file))

        folium_map = folium.Map(location=[latitude, longitude],
                          zoom_start = zoom)

        folium.GeoJson(json_map).add_to(folium_map)
        
    else:
        folium_map = folium.Map(location=[latitude, longitude],
                          zoom_start = zoom)

    return folium_map

# regex helpers
_wind_re = re.compile(r'^(?P<dir>\d{3}|VRB)(?P<spd>\d{2,3})(?:G(?P<gst>\d{2,3}))?KT$')
_vis_re = re.compile(r'^(?P<vis>(?:\d+\s)?\d?/?\d)SM$')
_sky_re = re.compile(r'^(?P<cov>FEW|SCT|BKN|OVC|CLR|SKC)(?P<ht>\d{3})?$')
_td_re = re.compile(r'^(?P<t>M?\d{1,2})/(?P<d>M?\d{1,2})$')
_alt_re = re.compile(r'^A(?P<alt>\d{4})$')
_tprec_re = re.compile(r'^T(?P<ts>0|1)(?P<t>\d{3})(?P<ds>0|1)(?P<d>\d{3})$')


def _md_to_c(s):
    if s is None:
        return None
    return -float(s[1]) if s.startswith("M") else float(s)

def _inHg_from_A(aaaa):
    return float(aaaa[:2] + "." + aaaa[2:])

def _c_from_Tgroup(sign, val):
    v = float(val)/10.0
    return -v if sign == '1' else v

def parse_metar_line(line):
    line = line.strip()

    if not line or line.startswith("#"):
        return None
    
    parts = line.split()

    if len(parts) < 5:
        return None
    
    out = {
        "date": parts[0],
        "time": parts[1],
        "station": parts[2],
        "ddhhmmZ": parts[3],
        "is_auto": False,
        "wind_dir": None,
        "wind_spd_kt": None,
        "wind_gst_kt": None,
        "visibility_raw": None,
        "visibility_sm": None,
        "sky_layers": [],
        "ceiling_ft": None,
        "temp_c": None,
        "dewpoint_c": None,
        "altimter_inHg": None,
        "remarks": None,
        "precise_temp_c": None,
        "precise_dew_c": None,
        }
    
    i = 4

    if i < len(parts) and parts[i] == "AUTO":
        out["is_auto"] = True
        i += 1

    while i < len(parts):
        tok = parts[i]
        if tok == "RMK":
            i += 1
            break

        m = _wind_re.match(tok)
        if m:
            out["wind_dir"] = m["dir"]
            out["wind_spd_kt"] = int(m["spd"])
            out["wind_gst_kt"] = int(m["gst"]) if m["gst"] else None
            i += 1
            continue

        m = _vis_re.match(tok)
        if m:
            raw = m['vis']
            out["visibility_raw"] = raw

            try:
                if " " in raw:
                    a, b = raw.split()
                    num = float(a) + eval(b)
                elif "/" in raw:
                    num = eval(raw)
                else:
                    num = float(raw)
            except Exception:
                num = None

            out['visibility_sm'] = num
            i += 1
            continue

        m = _sky_re.match(tok)
        if m:
            cov = m['cov']
            ht = int(m['ht']) * 100 if m['ht'] else None
            out['sky_layers'].append({"cov": cov, "base_ft": ht})
            i += 1
            continue

        m = _td_re.match(tok)
        if m:
            out["temp_c"] = _md_to_c(m['t'])
            out['dewpoint_c'] = _md_to_c(m['d'])
            i += 1
            continue

        m = _alt_re.match(tok)

        if m:
            out['altimter_inHg'] = _inHg_from_A(m['alt'])
            i += 1
            continue

    if i <= len(parts) - 1:
        remarks_tokens = parts[i:]
        out['remarks'] = " ".join(remarks_tokens).strip() or None

        for tk in remarks_tokens:
            m = _tprec_re.match(tk)
            if m:
                out['precise_temp_c'] = _c_from_Tgroup(m['ts'], m['t'])
                out['precise_dew_c'] = _c_from_Tgroup(m['ds'], m['d'])
                break
    bkn_ovc = [l['base_ft'] for l in out['sky_layers'] if l['cov'] in ('BKN', 'OVC') and l['base_ft']]

    out['ceiling_ft'] = min(bkn_ovc) if bkn_ovc else None

    return out

def parse_metar_file(path, encoding="utf-8"):
    rows = []

    for ln in Path(path).read_text(encoding=encoding).splitlines():
        rec = parse_metar_line(ln)
        if rec:
            rows.append(rec)

    return pd.DataFrame(rows)