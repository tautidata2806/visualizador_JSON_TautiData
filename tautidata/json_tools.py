import io
import json
import csv
import math
import pandas as pd

MAX_DEPTH = 50
MAX_NODES = 200_000
MAX_ROWS = 50_000
MAX_COLUMNS = 500
MAX_CELLS = 1_000_000


def validate_structure(data):
    stack = [(data, 0)]
    count = 0
    while stack:
        value, depth = stack.pop()
        count += 1
        if count > MAX_NODES or depth > MAX_DEPTH:
            raise ValueError('El JSON supera el límite de 200.000 valores o 50 niveles. Divide el archivo.')
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError('El JSON contiene un número fuera del rango admitido.')
        children = value.values() if isinstance(value, dict) else value if isinstance(value, list) else ()
        if isinstance(value, (dict, list)) and count + len(stack) + len(value) > MAX_NODES:
            raise ValueError('El JSON supera el límite de 200.000 valores. Divide el archivo.')
        stack.extend((child, depth + 1) for child in children)


def parse_json(raw):
    if len(raw) > 20 * 1024 * 1024:
        raise ValueError('El archivo supera los 20 MB.')
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise ValueError('Guarda el archivo con codificación UTF-8.') from exc
    def invalid(value):
        raise ValueError('El JSON contiene un valor numérico no válido.')
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('El JSON contiene claves repetidas en un objeto. Corrígelas para evitar pérdida de datos.')
            result[key] = value
        return result
    try:
        data = json.loads(text, parse_constant=invalid, object_pairs_hook=unique_object)
    except json.JSONDecodeError as exc:
        raise ValueError(f'JSON inválido: {exc.msg}. Línea {exc.lineno}, columna {exc.colno}.') from exc
    validate_structure(data)
    return data


def sections(data):
    result = {'$ · Documento completo': data}
    def visit(value, path, depth):
        if depth > 50 or not isinstance(value, dict):
            return
        for key, child in value.items():
            if len(result) >= 500:
                return
            if isinstance(child, (dict, list)):
                name = f'{path}[{json.dumps(key, ensure_ascii=False)}]'
                result[name] = child
                visit(child, name, depth + 1)
    visit(data, '$', 0)
    return result


def to_table(data):
    validate_structure(data)
    def flatten(value, path=''):
        result = {}
        if isinstance(value, dict) and value:
            for key, child in value.items():
                result.update(flatten(child, path + '[' + json.dumps(key, ensure_ascii=False) + ']'))
        else:
            result[path or 'valor'] = json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value
        return result
    rows = data if isinstance(data, list) else [data]
    if len(rows) > MAX_ROWS:
        raise ValueError('La sección supera las 50.000 filas. Divide el archivo.')
    records, columns = [], set()
    for row in rows:
        record = flatten(row)
        columns.update(record)
        if len(columns) > MAX_COLUMNS or len(rows) * len(columns) > MAX_CELLS:
            raise ValueError('La tabla supera 500 columnas o 1.000.000 de celdas. Selecciona una sección más pequeña.')
        records.append(record)
    return pd.DataFrame(records, dtype=object)


def csv_bytes(frame):
    def safe(value):
        if isinstance(value, str) and (value.startswith(('\t', '\r', '\n')) or value.lstrip().startswith(('=', '+', '-', '@'))):
            return "'" + value
        return value
    result = frame.map(safe)
    result.columns = [safe(str(name)) for name in result.columns]
    return result.to_csv(index=False, sep=';', quoting=csv.QUOTE_ALL).encode('utf-8-sig')


def excel_bytes(frame):
    if len(frame) > 1048575 or len(frame.columns) > 16384:
        raise ValueError('La tabla supera los límites de Excel. Usa CSV.')
    if any(isinstance(value, str) and len(value) > 32767 for value in frame.to_numpy().flat):
        raise ValueError('Una celda supera los 32.767 caracteres de Excel. Usa CSV o JSON.')
    output = io.BytesIO()
    export = frame.map(lambda v: str(v) if isinstance(v, int) and not isinstance(v, bool) and abs(v) >= 10**15 else v)
    with pd.ExcelWriter(output, engine='xlsxwriter', engine_kwargs={'options': {'strings_to_formulas': False, 'strings_to_urls': False}}) as writer:
        export.to_excel(writer, sheet_name='Datos', index=False)
        sheet = writer.sheets['Datos']
        header = writer.book.add_format({'bold': True, 'bg_color': '#7434BB', 'font_color': 'white', 'text_wrap': True})
        for i, name in enumerate(export.columns):
            sheet.write_string(0, i, str(name), header)
            sheet.set_column(i, i, 26)
        sheet.freeze_panes(1, 0)
        if len(export.columns):
            sheet.autofilter(0, 0, len(export), len(export.columns)-1)
    return output.getvalue()
