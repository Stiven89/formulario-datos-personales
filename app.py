import streamlit as st
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from pathlib import Path
import tempfile
import subprocess

st.set_page_config(
    page_title="Formulario de datos personales",
    page_icon="📄",
    layout="centered"
)

PLANTILLA = Path(__file__).parent / "Formulario_Datos_Personales.docx"

def escribir_en_celda(celda, valor):
    """Escribe dentro de una celda vacía sin reconstruir la tabla ni su diseño."""
    parrafo = celda.paragraphs[0]
    parrafo.clear()
    run = parrafo.add_run(str(valor).strip())
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(45, 55, 65)
    celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def generar_documento(datos):
    documento = Document(PLANTILLA)
    tablas = documento.tables

    # Nombre y apellido: tres casillas
    escribir_en_celda(tablas[0].cell(0, 0), datos["primer_nombre"])
    escribir_en_celda(tablas[0].cell(0, 1), datos["segundo_nombre"])
    escribir_en_celda(tablas[0].cell(0, 2), datos["apellido"])

    # Dirección: casilla de Calle y casilla de Número
    escribir_en_celda(tablas[2].cell(0, 0), datos["calle"])
    escribir_en_celda(tablas[4].cell(0, 0), datos["numero"])

    # Ciudad y provincia
    escribir_en_celda(tablas[6].cell(0, 0), datos["ciudad"])
    escribir_en_celda(tablas[6].cell(0, 1), datos["provincia"])

    # Código postal
    escribir_en_celda(tablas[8].cell(0, 0), datos["codigo_postal"])

    # Parte inferior: correo, espacio, código de área y teléfono
    escribir_en_celda(tablas[10].cell(0, 0), datos["correo"])
    escribir_en_celda(tablas[10].cell(0, 2), datos["codigo_area"])
    escribir_en_celda(tablas[10].cell(0, 3), datos["telefono"])

    return documento

def convertir_a_pdf(ruta_docx, carpeta_salida):
    resultado = subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(carpeta_salida),
            str(ruta_docx)
        ],
        capture_output=True,
        text=True,
        timeout=60
    )
    ruta_pdf = carpeta_salida / (ruta_docx.stem + ".pdf")
    if resultado.returncode != 0 or not ruta_pdf.exists():
        raise RuntimeError(
            "No se pudo convertir el documento a PDF. "
            f"Detalle: {resultado.stderr or resultado.stdout}"
        )
    return ruta_pdf.read_bytes()

st.title("Formulario de datos personales")
st.write("Completa los campos y genera tu documento PDF. Los datos no se guardan en esta aplicación.")

with st.form("formulario_datos"):
    st.subheader("Nombre y apellido")
    col1, col2, col3 = st.columns(3)
    with col1:
        primer_nombre = st.text_input("Primer nombre *")
    with col2:
        segundo_nombre = st.text_input("Segundo nombre")
    with col3:
        apellido = st.text_input("Apellido *")

    st.subheader("Dirección")
    calle = st.text_input("Calle")
    numero = st.text_input("Número")

    col4, col5 = st.columns(2)
    with col4:
        ciudad = st.text_input("Ciudad")
    with col5:
        provincia = st.text_input("Provincia")

    codigo_postal = st.text_input("Código postal")

    st.subheader("Contacto")
    correo = st.text_input("Correo electrónico (uso frecuente)")
    col6, col7 = st.columns(2)
    with col6:
        codigo_area = st.text_input("Código de área")
    with col7:
        telefono = st.text_input("Teléfono celular")

    enviar = st.form_submit_button("Generar PDF", type="primary", use_container_width=True)

if enviar:
    if not primer_nombre.strip() or not apellido.strip():
        st.error("Por favor, completa al menos el primer nombre y el apellido.")
    elif not PLANTILLA.exists():
        st.error("No se encontró la plantilla Word. Verifica que esté junto a app.py.")
    else:
        datos = {
            "primer_nombre": primer_nombre,
            "segundo_nombre": segundo_nombre,
            "apellido": apellido,
            "calle": calle,
            "numero": numero,
            "ciudad": ciudad,
            "provincia": provincia,
            "codigo_postal": codigo_postal,
            "correo": correo,
            "codigo_area": codigo_area,
            "telefono": telefono,
        }
        try:
            with st.spinner("Generando tu documento..."):
                documento = generar_documento(datos)
                with tempfile.TemporaryDirectory() as tmp:
                    carpeta = Path(tmp)
                    ruta_docx = carpeta / "Formulario_Datos_Personales_Completado.docx"
                    documento.save(ruta_docx)
                    contenido_pdf = convertir_a_pdf(ruta_docx, carpeta)

            st.success("¡Tu documento está listo!")
            st.download_button(
                label="⬇️ Descargar formulario en PDF",
                data=contenido_pdf,
                file_name="Formulario_Datos_Personales.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as error:
            st.error(f"Ocurrió un problema al generar el PDF: {error}")

st.caption("Aplicación de diligenciamiento. No almacena los datos ingresados.")
