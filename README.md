# TautiData · JSON Explorer

Visor de JSON en Python y Streamlit: carga de archivos o texto, tabla con búsqueda y selección de columnas, árbol, código y resumen. Exporta a Excel, CSV o JSON.

## Ejecutar

Requiere Python 3.12 o superior. Desde esta carpeta en Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run visualizador_json_TautiData.py
```

También puedes abrir `iniciar.bat`. Usa la URL que indique la consola: normalmente http://localhost:8501; si el puerto está ocupado, Streamlit puede elegir otro.

## Estructura del repositorio

```text
visualizador_de_JSON/
├── visualizador_json_TautiData.py  # Interfaz y punto de entrada
├── tautidata/                    # Transformación, validación y exportación
│   ├── __init__.py
│   └── json_tools.py
├── assets/                       # Logo e ilustración utilizados
├── config/contact.toml           # Nombre y correo públicos
├── examples/ventas.json          # Ejemplo ficticio
├── .streamlit/config.toml        # Tema y ajustes del servidor
├── tests/test_app.py             # Pruebas del procesamiento y la interfaz
├── docs/PUBLICACION.md           # Despliegue, privacidad y límites
├── requirements.txt             # Versiones directas verificadas localmente
├── iniciar.bat                   # Inicio rápido en Windows
├── .gitignore
└── README.md
```

Los cachés generados por Python y los entornos virtuales no forman parte del repositorio. No guardes archivos de clientes en el proyecto; si necesitas archivos privados para pruebas locales, usa `private/`, excluida de Git. No se incluyen archivos privados de ejemplo.

## Uso

1. Carga un JSON UTF-8 de hasta 20 MB, pega su contenido o elige **Probar ejemplo**.
2. Selecciona la sección: por ejemplo `$["ventas"]`.
3. Busca y selecciona columnas; la exportación respeta esos filtros.
4. Pulsa **Preparar Excel** y luego **Descargar Excel**, o descarga CSV directamente.

Los objetos anidados usan columnas con rutas como `["cliente"]["nombre"]` para evitar colisiones entre claves. Las listas dentro de celdas se conservan como texto JSON y no multiplican filas. Excel exporta una hoja por descarga. Ordenar la tabla visualmente no cambia el orden de exportación.

Se limitan documentos a 50 niveles y 200.000 valores, y tablas a 50.000 filas, 500 columnas y 1.000.000 de celdas. Los límites son preventivos y no garantizan disponibilidad bajo tráfico elevado. Excel conserva enteros de 16 o más dígitos como texto; los decimales utilizan la precisión habitual de Python. Las celdas demasiado largas para Excel producen un mensaje en lugar de truncarse.

## Contacto público

Edita `config/contact.toml`. Actualmente muestra **David Fellipe Tautiva** y **tautidata2806@gmail.com**, sin celular. No coloques credenciales en este archivo.

## Publicar y proteger los datos

Consulta [la guía de publicación y privacidad](docs/PUBLICACION.md). Explica cómo conectar GitHub con Streamlit Cloud, verificar acceso y HTTPS, gestionar secretos y distinguir una demo pública de un servicio para archivos confidenciales.

Esta versión procesa los archivos en el servidor cuando está publicada. No tiene autenticación propia ni se ha desplegado en internet.

## Pruebas

```powershell
python -B -m unittest discover -s tests -v
```

Mantén las pruebas en Git: verifican validación, límites, exportaciones y navegación. Ejecuta el comando después de cambios o actualizaciones de dependencias.
