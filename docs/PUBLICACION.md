# Publicación y privacidad

## Ruta recomendada: GitHub + Streamlit Community Cloud

Para este visor de portafolio, empieza con datos de ejemplo o archivos no confidenciales. El código vive en GitHub y la aplicación corre en Streamlit; GitHub Pages no ejecuta Python.

1. Crea un repositorio en GitHub. Puedes empezar privado. Revisa los archivos antes de subirlos: el `.gitignore` no elimina secretos ya incluidos en el historial.
2. Sube los archivos del proyecto, incluidos `.streamlit/config.toml`, `config/contact.toml`, `assets/`, `tautidata/` y `examples/`. No subas JSON reales de clientes.
3. En https://share.streamlit.io conecta GitHub y selecciona repositorio y rama.
4. Archivo principal: `visualizador_json_TautiData.py`. Usa Python 3.12 o superior; las pruebas locales se realizaron con 3.14.
5. La plataforma instala `requirements.txt`. Esta aplicación no necesita claves ni secretos para funcionar.
6. Configura explícitamente quién puede acceder a la app. Un repositorio privado no debe tomarse como garantía suficiente de acceso privado a la aplicación: revisa la configuración de compartición y verifica desde una ventana sin sesión.
7. Prueba el enlace HTTPS con el ejemplo, un JSON inválido, un archivo real no sensible y descargas CSV/Excel. Comprueba el nombre y correo públicos.
8. Comparte la URL solo después de estas verificaciones.

Documentación oficial:
- [Desplegar](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Modelo de seguridad y acceso privado](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/trust-and-security)
- [Gestión de secretos](https://docs.streamlit.io/deploy/concepts/secrets)

## Qué protege esta versión

- Límite de 50 MB también en el procesamiento de texto pegado.
- Rechazo de claves duplicadas, números no finitos y documentos con más de 50 niveles o 200.000 valores.
- Tablas limitadas a 50.000 filas, 500 columnas y 1.000.000 de celdas antes de crear el DataFrame.
- El JSON se interpreta como datos: no se ejecuta con `eval`, ni se inserta en HTML sin escapar.
- Excel no interpreta textos como fórmulas ni enlaces; CSV neutraliza prefijos peligrosos. La protección de CSV modifica esos textos; JSON conserva el contenido estructurado, aunque no el formato original.
- Sin base de datos, escritura de cargas en disco, caché compartida de archivos ni registro explícito de su contenido en el código de la aplicación.
- CORS y protección XSRF activadas; detalles de errores inesperados ocultos en la interfaz. Esto no impide que el servidor genere registros técnicos.
- Telemetría de uso de Streamlit desactivada. Esto no desactiva los registros operativos del proveedor.
- Versiones directas fijadas para reducir variaciones al desplegar. Las dependencias transitivas no están bloqueadas y requieren revisión periódica.

## Límites y decisiones antes de abrirla al público

No existe una garantía de seguridad absoluta. Estas medidas son una base técnica, no una auditoría de seguridad ni una certificación de cumplimiento legal.

Los archivos llegan al servidor y se mantienen temporalmente en memoria para procesar la sesión y las descargas. No se promete borrado inmediato al cerrar una pestaña, ni ausencia de registros o persistencia a nivel de infraestructura. El proveedor, su región, términos y retención deben revisarse para el tipo de datos que vayas a permitir.

Una app pública no tiene autenticación incorporada ni límites por usuario/IP. Los límites por archivo reducen consumo, pero no evitan abuso por muchas solicitudes simultáneas. Para cargas de clientes, información personal o documentos confidenciales, usa acceso privado con usuarios autorizados y revisa las condiciones del proveedor; para un servicio de producción, añade control de acceso, límites de tráfico y monitorización en la infraestructura elegida. Si necesitas que ningún JSON salga del equipo, usa la versión local o cambia el procesamiento al navegador.

Antes de un lanzamiento público, publica un aviso de privacidad accesible con responsable, finalidad, proveedor, tratamiento, retención y contacto reales. El bloque de contacto no reemplaza ese aviso. No declares que los datos nunca salen del equipo cuando la aplicación funciona en un servidor. La decisión de dónde mostrar ese aviso queda pendiente para el despliegue; se retiró el párrafo del panel por solicitud del propietario.

## Mantenimiento

- Revisa actualizaciones y avisos de seguridad de Streamlit, pandas, XlsxWriter y dependencias transitivas; actualiza versiones y vuelve a probar.
- Puedes realizar un análisis de dependencias instalando `pip-audit` en el entorno de desarrollo y ejecutando `python -m pip_audit -r requirements.txt`. Este análisis no se ha realizado como parte de esta revisión y no sustituye una auditoría completa.
- Nunca pegues claves en archivos versionados. Si futuras funciones las requieren, usa Secrets de Streamlit Cloud; localmente `.streamlit/secrets.toml`, ignorado por Git.
- Ante una filtración, restringe el acceso, rota credenciales afectadas y revisa el historial del repositorio. Borrar solo el archivo actual no elimina su historial.

Estado: preparado localmente; no se ha creado ni publicado un repositorio remoto ni una aplicación en la nube.
