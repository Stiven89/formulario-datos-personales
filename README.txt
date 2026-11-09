# Generador de formulario de datos personales

Aplicación Streamlit que toma los datos de un formulario web, los inserta en las casillas vacías de la plantilla Word original y entrega un PDF.

## Archivos

- `app.py`: aplicación web.
- `Formulario_Datos_Personales.docx`: plantilla original (no modificar ni renombrar).
- `requirements.txt`: dependencias Python.
- `packages.txt`: paquetes del sistema necesarios para convertir Word a PDF en Streamlit Community Cloud.

## Probar en Windows

1. Instala Python 3.10 o superior.
2. Abre PowerShell en esta carpeta.
3. Ejecuta:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

4. Instala LibreOffice para Windows desde https://www.libreoffice.org/download/download-libreoffice/
5. Si `soffice` no se reconoce, agrega la carpeta de LibreOffice al PATH o reinicia PowerShell.
6. Ejecuta:

```powershell
streamlit run app.py
```

Se abrirá la aplicación en `http://localhost:8501`.

## Publicar gratis en Streamlit Community Cloud

1. Crea un repositorio público en GitHub.
2. Sube los cuatro archivos de este proyecto: `app.py`, `requirements.txt`, `packages.txt` y `Formulario_Datos_Personales.docx`.
3. Entra a https://share.streamlit.io/ e inicia sesión con GitHub.
4. Selecciona **Create app**.
5. Elige el repositorio, la rama `main` y el archivo principal `app.py`.
6. Pulsa **Deploy**. Streamlit instalará las dependencias y publicará un enlace para compartir.

## Privacidad

Esta versión no guarda los datos en una base de datos ni en archivos permanentes: genera el PDF durante la sesión y lo entrega para descargar. Aun así, evita introducir datos sensibles que no sean necesarios y comparte el enlace solo con las personas que deban usar el formulario.
