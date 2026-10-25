# Visualizador JSON · TautiData

Una herramienta sencilla para leer archivos JSON sin perderse entre llaves y corchetes. Cargas tu archivo, exploras los datos y descargas lo que necesitas en Excel o CSV.

Está hecha con Python y Streamlit.

[Abrir el visualizador](https://visualizadorjsontautidata-orep8viddqs8dzgzrqk8f3.streamlit.app/)

## ¿Qué puedes hacer?

- Subir un JSON de hasta **50 MB** o pegar su contenido.
- Ver los datos como tabla, árbol o código.
- Elegir una sección del archivo, buscar valores y seleccionar columnas.
- Descargar la tabla filtrada en Excel o CSV, o guardar una sección como JSON.

Si no tienes un archivo a mano, selecciona **Probar ejemplo** en el panel lateral.

## Para ejecutarlo en tu computador

Necesitas Python 3.12 o superior. Abre una terminal en la carpeta del proyecto y ejecuta estos comandos en Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run visualizador_json_TautiData.py
```

Luego abre el enlace que aparece en la terminal. Para las siguientes veces, puedes usar `iniciar.bat`.

## Cómo está organizado

La aplicación empieza en `visualizador_json_TautiData.py`. El código que transforma y exporta los datos está en `tautidata/`.

Las imágenes están en `assets/`, el archivo de ejemplo en `examples/` y los datos de contacto en `config/contact.toml`. El tema y el límite de carga se configuran en `.streamlit/config.toml`.

## Un par de detalles

Las listas dentro de una celda se conservan como texto JSON. Si quieres trabajar con una lista como tabla, selecciónala desde el menú de secciones cuando esté disponible.

Además del tamaño del archivo, hay límites de filas, columnas y profundidad para evitar que la aplicación se quede sin memoria. Al usar la versión web, los archivos se procesan en el servidor; el código de la aplicación no los guarda en disco.

Para publicar tu propia versión, consulta la [guía de publicación](docs/PUBLICACION.md). Allí también están los detalles de estos límites y del manejo de los archivos.

## Pruebas

Si modificas el código, puedes comprobar que lo principal siga funcionando con:

```powershell
python -B -m unittest discover -s tests -v
```

---

**David Fellipe Tautiva** · TautiData  
[tautidata2806@gmail.com](mailto:tautidata2806@gmail.com)
