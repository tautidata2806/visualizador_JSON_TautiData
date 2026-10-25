from pathlib import Path
import hashlib
import json
import tomllib
import pandas as pd
import streamlit as st
from tautidata.json_tools import parse_json, sections, to_table, csv_bytes, excel_bytes

ROOT = Path(__file__).parent
st.set_page_config(page_title='JSON Explorer · TautiData', page_icon='🔮', layout='wide')
st.markdown('''<style>
.stApp {background: #f7f8fc;}
.block-container {padding-top: 4rem; max-width: 1440px;}
h1,h2,h3 {color: #24113d; letter-spacing: -.035em;}
[data-testid="stSidebar"] {background: #eeeaf7;}
[data-testid="stMetric"] {background: white; border: 1px solid #e5dff0; border-radius: 16px; padding: 18px;}
.eyebrow {color: #7945c7; font-weight: 700; font-size: .8rem; letter-spacing: .16em;}
.intro {color: #6b657b; font-size: 1.1rem;}
.step {background: white; border: 1px solid #e5dff0; border-radius: 14px; padding: 20px; margin-bottom: 16px;}
.step b {color: #7833c5;}
</style>''', unsafe_allow_html=True)
with st.sidebar:
    st.image(str(ROOT / 'assets/logo.png'), width=220)
    st.divider()
    st.markdown('### Tu espacio de datos')
    source = st.radio('Origen del JSON', ['Subir archivo', 'Pegar JSON', 'Probar ejemplo'])
    raw, filename = None, 'datos'
    if source == 'Subir archivo':
        uploaded = st.file_uploader('Selecciona tu archivo', type=['json'], max_upload_size=50)
        if uploaded is not None:
            raw, filename = uploaded.getvalue(), Path(uploaded.name).stem
    elif source == 'Pegar JSON':
        pasted = st.text_area('Pega el contenido', height=230, placeholder='[{"nombre": "Ana", "ventas": 250}]')
        if pasted.strip():
            raw = pasted.encode('utf-8')
    else:
        raw, filename = (ROOT / 'examples' / 'ventas.json').read_bytes(), 'ejemplo_tautidata'
    st.divider()
    st.caption('JSON Explorer · TautiData')
    contact = tomllib.loads((ROOT / 'config' / 'contact.toml').read_text(encoding='utf-8-sig'))
    st.markdown('#### Contacto')
    for field in ('name', 'phone', 'email'):
        if contact.get(field):
            st.text(contact[field])
st.markdown('<div class="eyebrow">TAUTIDATA / HERRAMIENTAS</div>', unsafe_allow_html=True)
st.title('Tus datos, más claros.')
st.markdown('<p class="intro">Explora tu JSON, encuentra lo que necesitas y llévalo a una tabla lista para trabajar.</p>', unsafe_allow_html=True)
if raw is None:
    left, right = st.columns([1.6, 1], gap='large')
    with left:
        st.markdown('## De JSON a ideas, en un momento.')
        st.write('Carga tu archivo desde el panel izquierdo o selecciona **Probar ejemplo** para explorar las vistas.')
        for title, body in [('01 · Carga', 'Tu archivo o el contenido de una respuesta de API.'), ('02 · Explora', 'Una tabla para analizar y un árbol para entender la estructura.'), ('03 · Descarga', 'Exporta tu selección a Excel o CSV con un clic.')]:
            st.markdown(f'<div class="step"><b>{title}</b><p>{body}</p></div>', unsafe_allow_html=True)
    with right:
        st.image(str(ROOT / 'assets/welcome.png'), width=340)
    st.stop()
try:
    data = parse_json(raw)
    choices = sections(data)
except (ValueError, RecursionError) as exc:
    st.error(str(exc) if not isinstance(exc, RecursionError) else 'Demasiados niveles de anidación.')
    st.stop()
identity = hashlib.sha256(raw).hexdigest()[:12]
st.success(f'{filename} · JSON válido · {len(raw)/1024:,.1f} KB')
selection = st.selectbox('Sección que quieres explorar', list(choices), key=f'section_{identity}')
selected = choices[selection]
try:
    frame = to_table(selected)
except (ValueError, RecursionError) as exc:
    st.error(f'No fue posible crear la tabla: {exc}')
    st.stop()
a, b, c, d = st.columns(4)
a.metric('Registros', f'{len(frame):,}')
b.metric('Columnas', len(frame.columns))
c.metric('Celdas vacías', int(frame.isna().sum().sum()))
d.metric('Secciones', len(choices))
table, tree, code, profile = st.tabs(['Tabla', 'Árbol', 'Código JSON', 'Resumen de columnas'])
with table:
    widget_key = f'{identity}_{selection}'
    search = st.text_input('Buscar en todas las columnas', placeholder='Escribe un nombre, valor o palabra…', key=f'search_{widget_key}')
    columns = st.multiselect('Columnas visibles y exportables', list(frame.columns), default=list(frame.columns), key=f'cols_{widget_key}')
    filtered = frame
    if search:
        mask = frame.astype(str).apply(lambda col: col.str.contains(search, case=False, regex=False)).any(axis=1)
        filtered = frame.loc[mask]
    filtered = filtered.loc[:, columns]
    st.caption(f'{len(filtered):,} de {len(frame):,} registros · La descarga respeta la búsqueda y las columnas elegidas.')
    if not columns:
        st.info('Selecciona al menos una columna para ver y exportar la tabla.')
    else:
        st.dataframe(filtered, width='stretch', hide_index=True, height=430)
        x, y = st.columns(2)
        with x:
            st.download_button('↓ Descargar CSV', csv_bytes(filtered), f'{filename}.csv', 'text/csv', width='stretch')
        with y:
            if st.button('Preparar Excel', type='primary', width='stretch'):
                try:
                    st.download_button('↓ Descargar Excel', excel_bytes(filtered), f'{filename}.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', on_click='ignore', width='stretch')
                except (ValueError, ImportError) as exc:
                    st.error(f'No se pudo generar Excel: {exc}')
        st.caption('Los objetos se despliegan en columnas; las listas dentro de celdas se conservan como JSON. CSV usa ; como separador y UTF-8 con BOM.')
with tree:
    st.caption('Estructura de la sección seleccionada. Despliega los nodos para explorar.')
    st.json(selected, expanded=2)
with code:
    formatted = json.dumps(selected, ensure_ascii=False, indent=2)
    st.download_button('↓ Descargar esta sección como JSON', formatted, f'{filename}_seccion.json', 'application/json')
    if len(formatted) < 500000:
        st.code(formatted, language='json', line_numbers=True)
    else:
        st.info('El código es grande. Descárgalo completo o utiliza el árbol.')
with profile:
    summary = pd.DataFrame([{'Columna': name, 'Tipo': ', '.join(sorted({type(v).__name__ for v in frame[name] if v is not None and not (isinstance(v, float) and pd.isna(v))})), 'Valores presentes': int(frame[name].notna().sum()), 'Vacíos': int(frame[name].isna().sum())} for name in frame.columns])
    st.dataframe(summary, hide_index=True, width='stretch')

