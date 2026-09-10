import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, color_hex):
    """Establece el color de fondo de una celda en tabla Word."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Ajusta el espaciado interno (padding) de una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout_box(doc, title, text, border_color="4f46e5", bg_color="f1f5f9"):
    """Crea una caja de aviso destacada tipo Callout."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    # Borde izquierdo grueso
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"📌 {title}\n")
    run_t.font.name = "Segoe UI"
    run_t.font.size = Pt(10)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

    run_b = p.add_run(text)
    run_b.font.name = "Segoe UI"
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    doc.add_paragraph() # espacio

def build_document():
    doc = docx.Document()

    # Configuración de página (Márgenes 2.5 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Paleta de Colores
    COLOR_PRIMARY = RGBColor(0x1e, 0x3a, 0x8a)   # Azul Marino Institucional
    COLOR_SECONDARY = RGBColor(0x43, 0x38, 0xca) # Índigo
    COLOR_TEXT = RGBColor(0x1e, 0x29, 0x3b)      # Gris Oscuro Lectura
    COLOR_GRAY = RGBColor(0x64, 0x74, 0x8b)      # Gris Medio

    # =========================================================================
    # PORTADA FORMAL (5 PUNTOS)
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("INSTITUCIÓN DE EDUCACIÓN SUPERIOR\nFACULTAD DE INGENIERÍA, CIENCIAS Y TECNOLOGÍA\nESCUELA DE INFORMÁTICA Y TELECOMUNICACIONES\n")
    r_inst.font.name = "Segoe UI"
    r_inst.font.size = Pt(10)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_GRAY

    doc.add_paragraph().paragraph_format.space_after = Pt(40)

    # Título Principal
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("INFORME TÉCNICO DE INGENIERÍA DE SOFTWARE\nETAPA 2: ESPECIFICACIÓN DE REQUERIMIENTOS, MODELADO UML Y DISEÑO DE SISTEMA\n\n")
    r_t1.font.name = "Segoe UI"
    r_t1.font.size = Pt(18)
    r_t1.font.bold = True
    r_t1.font.color.rgb = COLOR_PRIMARY

    r_t2 = p_title.add_run("TalentHub HR: Sistema Integral de Gestión de Personas, Liquidaciones y Finiquitos en Chile con Base de Datos NoSQL y Control de Acceso RBAC")
    r_t2.font.name = "Segoe UI"
    r_t2.font.size = Pt(13)
    r_t2.font.italic = True
    r_t2.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph().paragraph_format.space_after = Pt(100)

    # Cuadro de Antecedentes
    tbl_ant = doc.add_table(rows=6, cols=2)
    tbl_ant.alignment = WD_TABLE_ALIGNMENT.CENTER
    ant_data = [
        ("Asignatura / Módulo:", "Taller de Ingeniería de Software / Proyecto de Título"),
        ("Proyecto:", "TalentHub HR - Plataforma Web, Consola CLI y Desktop GUI"),
        ("Integrantes / Autores:", "Equipo de Desarrollo de Ingeniería de Software"),
        ("Docente Guía / Evaluador:", "Profesor de Cátedra / Comisión Evaluadora"),
        ("Fecha de Entrega:", "Septiembre de 2026"),
        ("Ciudad y Sede:", "Santiago de Chile")
    ]
    for row_idx, (label, val) in enumerate(ant_data):
        c_lbl = tbl_ant.cell(row_idx, 0)
        c_val = tbl_ant.cell(row_idx, 1)
        c_lbl.width = Inches(2.2)
        c_val.width = Inches(4.3)
        
        p0 = c_lbl.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_PRIMARY

        p1 = c_val.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # =========================================================================
    # ÍNDICE GENERAL & TABLA DE CONTENIDOS
    # =========================================================================
    p_toc = doc.add_paragraph()
    r_toc = p_toc.add_run("TABLA DE CONTENIDOS")
    r_toc.font.name = "Segoe UI"
    r_toc.font.size = Pt(14)
    r_toc.font.bold = True
    r_toc.font.color.rgb = COLOR_PRIMARY

    toc_items = [
        "1. INTRODUCCIÓN Y CONTINUIDAD DEL PROYECTO",
        "   1.1 Síntesis Ejecutiva del Informe 1",
        "   1.2 Contextualización de la Segunda Etapa",
        "   1.3 Propósito y Objetivos del Informe",
        "2. METODOLOGÍA, CICLO DE VIDA Y PLANIFICACIÓN",
        "   2.1 Selección y Justificación de la Metodología Ágil (Scrum)",
        "   2.2 Definición del Ciclo de Vida del Software (Iterativo e Incremental)",
        "   2.3 Estructura de Roles y Organización del Equipo de Trabajo",
        "   2.4 Planificación Temporal, Desglose WBS y Carta Gantt",
        "3. LEVANTAMIENTO Y VALIDACIÓN DE REQUERIMIENTOS",
        "   3.1 Técnicas de Levantamiento y Co-Creación Aplicadas",
        "   3.2 Identificación de Fuentes y Stakeholders Participantes",
        "   3.3 Especificación de Requerimientos Funcionales (RF01 - RF15)",
        "   3.4 Especificación de Requerimientos No Funcionales (RNF01 - RNF08)",
        "   3.5 Validación con Usuarios y Documentación de Ajustes",
        "4. CALIDAD Y TRAZABILIDAD DE REQUERIMIENTOS",
        "   4.1 Criterios y Estándar de Calidad Aplicados (ISO/IEC/IEEE 29148)",
        "   4.2 Matriz de Trazabilidad de Requerimientos (RTM)",
        "5. DIAGRAMA DE CASOS DE USO Y ESPECIFICACIONES FORMALES",
        "   5.1 Diagrama de Casos de Uso del Sistema (UML 2.5)",
        "   5.2 Especificaciones Formales de Casos de Uso Principales (CU-01 a CU-05)",
        "6. DIAGRAMA DE CLASES DEL SISTEMA",
        "   6.1 Modelo de Clases Estructural (UML 2.5)",
        "   6.2 Diccionario de Clases, Responsabilidades y Relaciones",
        "7. MOCKUPS Y DISEÑO DE INTERFAZ DE USUARIO",
        "   7.1 Arquitectura de Información y Flujos de Navegación",
        "   7.2 Especificación de Pantallas Clave del Sistema (Pantallas 1 a 6)",
        "8. CONCLUSIONES Y PROYECCIÓN DEL PROYECTO",
        "9. REFERENCIAS BIBLIOGRÁFICAS Y NORMATIVAS"
    ]

    for item in toc_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(1)
        p_item.paragraph_format.space_after = Pt(1)
        r = p_item.add_run(item)
        r.font.name = "Segoe UI"
        r.font.size = Pt(9.5)
        if item.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            r.font.bold = True
            r.font.color.rgb = COLOR_PRIMARY
        else:
            r.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # Función auxiliar para títulos de sección
    def add_sec_title(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title_text)
        r.font.name = "Segoe UI"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        return p

    def add_subsec_title(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title_text)
        r.font.name = "Segoe UI"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = COLOR_SECONDARY
        return p

    def add_p(text, bold_prefix=None, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Segoe UI"
            rb.font.size = Pt(10)
            rb.font.bold = True
            rb.font.color.rgb = COLOR_TEXT
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.size = Pt(10)
        r.font.italic = italic
        r.font.color.rgb = COLOR_TEXT
        return p

    # =========================================================================
    # SECCIÓN 1: INTRODUCCIÓN Y CONTINUIDAD DEL PROYECTO (5 PUNTOS)
    # =========================================================================
    add_sec_title("1. INTRODUCCIÓN Y CONTINUIDAD DEL PROYECTO")

    add_subsec_title("1.1 Síntesis Ejecutiva del Informe 1")
    add_p("En la primera etapa del proyecto se analizó en profundidad la problemática que enfrentan las pequeñas, medianas y grandes empresas en Chile respecto a la administración del capital humano. Tradicionalmente, la gestión de colaboradores se realiza de forma fragmentada mediante planillas de cálculo descentralizadas, memorandos impresos y sistemas contables aislados. Esta falta de integración provoca errores recurrentes en los cálculos previsionales y tributarios, desactualización en los expedientes de personal y demoras críticas en la tramitación de permisos y finiquitos legales, exponiendo a las organizaciones a severas multas de la Dirección del Trabajo (DT) e insatisfacción de los colaboradores.")
    add_p("Frente a este escenario, se concibió TalentHub HR como una solución integral, intuitiva y centralizada, orientada a digitalizar de extremo a extremo el ciclo de vida del colaborador en la organización, desde su contratación inicial y evaluaciones periódicas hasta el término de su relación laboral.")

    add_subsec_title("1.2 Contextualización de la Segunda Etapa")
    add_p("La presente segunda etapa consolida el paso desde la conceptualización de necesidades hacia la ingeniería formal de software y el diseño arquitectónico detallado. Durante esta fase se formalizaron las técnicas de levantamiento y co-creación con actores del área de personas, se especificaron rigurosamente los requerimientos funcionales y no funcionales conforme a estándares de calidad reconocidos internacionalmente (ISO/IEC/IEEE 29148), y se estructuraron los modelos visuales en UML 2.5 (Casos de Uso y Diagrama de Clases).")
    add_p("Asimismo, se incorporó un robusto sistema de Control de Acceso Basado en Roles (RBAC), distinguiendo taxativamente entre el perfil de Administrador General (con facultades plenas de gestión y modificación de remuneraciones) y el perfil del Colaborador (con acceso al Portal Privado de Desempeño, Liquidaciones y Solicitudes, manteniendo su remuneración en estricto modo Solo Lectura).")

    add_subsec_title("1.3 Propósito y Objetivos del Informe")
    add_p("El propósito primordial de este documento es proporcionar una guía técnica exhaustiva, verificable y trazable que siente las bases para la fase de construcción, certificación y pruebas del software. El informe detalla la metodología ágil empleada, la planificación temporal, la matriz de trazabilidad de requerimientos, las especificaciones formales de casos de uso y la arquitectura de interfaces de usuario.")

    add_callout_box(doc, "Propósito Clave de la Etapa 2", 
                    "Asegurar la total correspondencia entre la legislación laboral vigente de Chile (Código del Trabajo, Superintendencia de Pensiones y SII) y la arquitectura de software NoSQL, garantizando trazabilidad completa desde la necesidad del usuario hasta el diseño de clases e interfaces.")

    # =========================================================================
    # SECCIÓN 2: METODOLOGÍA, CICLO DE VIDA Y PLANIFICACIÓN (15 PUNTOS)
    # =========================================================================
    add_sec_title("2. METODOLOGÍA, CICLO DE VIDA Y PLANIFICACIÓN")

    add_subsec_title("2.1 Selección y Justificación de la Metodología Ágil (Scrum)")
    add_p("Para el desarrollo de TalentHub HR se seleccionó el marco ágil Scrum adaptado a ciclos de entrega continua. La elección se fundamenta en los siguientes criterios técnicos:")
    add_p("• Adaptabilidad a la Normativa Laboral: Las normativas tributarias (SII) y de seguridad social (tasas AFP, topes imponibles en UF/UTM) presentan actualizaciones periódicas que requieren una arquitectura flexible y retroalimentación constante.\n• Prototipado y Validación Temprana: Scrum permite iteraciones cortas (Sprints de 2 semanas) con entregables funcionales (Incrementos de Producto) que los administradores de RRHH pueden validar interactivamente.\n• Mitigación de Riesgos Arquitectónicos: La coexistencia de tres capas de cliente (Web React, Desktop GUI Tkinter y Consola Python CLI) sobre un mismo repositorio documental NoSQL requiere validaciones continuas de integración.")

    add_subsec_title("2.2 Definición del Ciclo de Vida del Software")
    add_p("Se definió un Ciclo de Vida Iterativo e Incremental. Cada ciclo abarca fases de Análisis y Refinamiento, Diseño Técnico UML, Implementación de Código, Pruebas de Calidad (QA) y Demostración al Stakeholder (Sprint Review).")

    add_subsec_title("2.3 Estructura de Roles y Organización del Equipo de Trabajo")
    add_p("El equipo de proyecto está compuesto por los siguientes roles definidos formalmente:")
    
    # Tabla de Roles
    tbl_roles = doc.add_table(rows=6, cols=3)
    tbl_roles.alignment = WD_TABLE_ALIGNMENT.CENTER
    roles_headers = ["Rol Scrum / Proyecto", "Responsabilidades Principales", "Dedicación Estimada"]
    for i, h in enumerate(roles_headers):
        c = tbl_roles.cell(0, i)
        set_cell_background(c, "1e3a8a")
        set_cell_margins(c, 100, 100, 120, 120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    roles_rows = [
        ("Product Owner (PO)", "Define la visión del producto, prioriza el Product Backlog y valida el cumplimiento legal y normativo.", "20 hrs / semana"),
        ("Scrum Master (SM)", "Facilita las ceremonias ágiles, elimina impedimentos técnicos y monitorea el cumplimiento de la Carta Gantt.", "15 hrs / semana"),
        ("Lead Developer Full-Stack", "Diseño arquitectónico, desarrollo del motor NoSQL, APIs REST y clientes Web/Python.", "40 hrs / semana"),
        ("QA & Test Automation", "Diseño y ejecución de casos de prueba unitarios, de integración, rendimiento y seguridad RBAC.", "30 hrs / semana"),
        ("Asesor Legal & Laboral RRHH", "Verificación de fórmulas de cálculo (Art. 50, 159, 161, 163) y redacción de finiquitos notariales.", "10 hrs / semana")
    ]
    for row_idx, r_data in enumerate(roles_rows, 1):
        for col_idx, text in enumerate(r_data):
            c = tbl_roles.cell(row_idx, col_idx)
            set_cell_background(c, "f8fafc" if row_idx % 2 == 1 else "ffffff")
            set_cell_margins(c, 80, 80, 100, 100)
            p = c.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Segoe UI"
            r.font.size = Pt(9)
            r.font.color.rgb = COLOR_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_subsec_title("2.4 Planificación Temporal, Desglose WBS y Carta Gantt")
    add_p("El proyecto se planificó para un horizonte temporal de 8 semanas, estructurado en 4 Sprints quincenales, asegurando un dimensionamiento realista de recursos y alcance:")
    add_p("• Sprint 1 (Semanas 1-2): Levantamiento, arquitectura de base de datos NoSQL, CRUD de Colaboradores y Departamentos.\n• Sprint 2 (Semanas 3-4): Módulo de Vacaciones/Permisos, Evaluaciones de Desempeño 360° y Sistema de Autenticación RBAC.\n• Sprint 3 (Semanas 5-6): Motor Legal de Liquidaciones de Sueldo (Chile) y Gestor de Finiquitos (Art. 159 vs 161).\n• Sprint 4 (Semanas 7-8): Portal del Colaborador (Solo Lectura), Clientes Python (CLI / Desktop GUI), Pruebas QA y Despliegue.")

    if os.path.exists("diagramas_informe/figura1_carta_gantt.png"):
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("diagramas_informe/figura1_carta_gantt.png", width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Carta Gantt y Cronograma de Trabajo por Sprints (TalentHub HR)")
        r_cap.font.name = "Segoe UI"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_GRAY

    # =========================================================================
    # SECCIÓN 3: LEVANTAMIENTO Y VALIDACIÓN DE REQUERIMIENTOS (20 PUNTOS)
    # =========================================================================
    add_sec_title("3. LEVANTAMIENTO Y VALIDACIÓN DE REQUERIMIENTOS")

    add_subsec_title("3.1 Técnicas de Levantamiento y Co-Creación Aplicadas")
    add_p("Para capturar fielmente las necesidades del negocio se implementó un enfoque metodológico mixto:")
    add_p("1. Entrevistas Semiestructuradas: Realizadas a Directores de RRHH, Analistas de Nómina y Contadores Generales de empresas de servicios en Santiago de Chile.\n2. Talleres de Co-Creación & User Story Mapping: Sesiones colaborativas con usuarios finales para mapear el viaje del empleado (Employee Journey) y priorizar funcionalidades.\n3. Análisis Normativo y Documental: Estudio riguroso del Código del Trabajo de Chile, Ley N° 19.728 (Seguro de Cesantía), Ley N° 21.561 (40 Horas), tablas del SII (Impuesto Único de Segunda Categoría) e instructivos de la Dirección del Trabajo (DT).")

    add_subsec_title("3.2 Identificación de Fuentes y Stakeholders Participantes")
    add_p("Se identificaron 4 grupos de interés clave: (1) Administradores de RRHH, responsables de la nómina y dotación; (2) Colaboradores / Trabajadores, usuarios del portal de autoservicio; (3) Gerencia General / Finanzas, interesados en métricas de masa salarial y costos; y (4) Entidades Fiscalizadoras (DT, SII, Previred), que dictan el marco legal de cumplimiento.")

    add_subsec_title("3.3 Especificación de Requerimientos Funcionales (RF)")
    add_p("A continuación se presenta la tabla formal de Requerimientos Funcionales, estructurados bajo el estándar IEEE 830 / ISO 29148 y priorizados mediante la técnica MoSCoW (Must, Should, Could, Won't):")

    tbl_rf = doc.add_table(rows=16, cols=4)
    tbl_rf.alignment = WD_TABLE_ALIGNMENT.CENTER
    rf_headers = ["ID RF", "Nombre del Requerimiento", "Descripción Funcional", "Prioridad"]
    for i, h in enumerate(rf_headers):
        c = tbl_rf.cell(0, i)
        set_cell_background(c, "1e3a8a")
        set_cell_margins(c, 100, 100, 100, 100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    rf_data = [
        ("RF-01", "Autenticación y Roles RBAC", "El sistema debe autenticar usuarios mediante usuario/correo y contraseña, asignando perfil de Administrador o Trabajador.", "Must"),
        ("RF-02", "Gestión de Colaboradores (CRUD)", "El sistema debe permitir crear, listar, buscar, modificar y dar de baja colaboradores con su ficha integral 360°.", "Must"),
        ("RF-03", "Gestión de Departamentos", "El sistema debe administrar áreas funcionales y calcular automáticamente la masa salarial y plantilla por departamento.", "Must"),
        ("RF-04", "Solicitud y Aprobación de Permisos", "El sistema debe permitir solicitar vacaciones con cálculo de días y facultar a RRHH para aprobar o rechazar con notas.", "Must"),
        ("RF-05", "Evaluaciones de Desempeño 360°", "El sistema debe registrar revisiones periódicas con calificación de 1 a 5 estrellas en 5 competencias, fortalezas y metas.", "Must"),
        ("RF-06", "Cálculo de Haberes Imponibles", "El sistema debe calcular Sueldo Base, Gratificación Legal Art. 50 (25% tope 4.75 IMM/12), Horas extras 50% y bonos.", "Must"),
        ("RF-07", "Deducciones Previsionales Chile", "El sistema debe descontar AFP (tasas vigentes con tope 84.3 UF), Salud (Fonasa 7% / Isapre) y AFC (0.6% indefinido).", "Must"),
        ("RF-08", "Cálculo Impuesto Único SII (IUSC)", "El sistema debe calcular el Impuesto Único de Segunda Categoría según los tramos progresivos oficiales en UTM del SII.", "Must"),
        ("RF-09", "Costo Empresa y Aportes Patronales", "El sistema debe calcular aportes patronales: SIS (1.49%), Mutual de Seguridad (0.93%) y AFC Empleador (2.4%/3.0%).", "Should"),
        ("RF-10", "Diferenciación Legal de Finiquitos", "El sistema debe calcular finiquitos diferenciando entre Renuncia Voluntaria (Art. 159) y Despido por Necesidades (Art. 161).", "Must"),
        ("RF-11", "Generación de Documento Legal DT", "El sistema debe generar el texto oficial del finiquito con formato formal de la Dirección del Trabajo listo para notaría.", "Must"),
        ("RF-12", "Portal Privado del Colaborador", "El sistema debe proveer una vista exclusiva para que el trabajador consulte su desempeño, liquidaciones y permisos.", "Must"),
        ("RF-13", "Protección de Sueldos (Solo Lectura)", "El sistema debe bloquear estrictamente la edición o alteración de sueldos para usuarios con rol de Colaborador.", "Must"),
        ("RF-14", "Persistencia NoSQL y Exportación", "El sistema debe almacenar datos en colecciones documentales JSON y permitir exportar reportes en formatos CSV y TXT.", "Must"),
        ("RF-15", "Envío de Liquidación por Correo", "El sistema debe permitir enviar el comprobante formal de liquidación de sueldo directamente al correo electrónico del colaborador.", "Must")
    ]

    for row_idx, r_item in enumerate(rf_data, 1):
        for col_idx, text in enumerate(r_item):
            c = tbl_rf.cell(row_idx, col_idx)
            set_cell_background(c, "f8fafc" if row_idx % 2 == 1 else "ffffff")
            set_cell_margins(c, 70, 70, 80, 80)
            p = c.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            elif col_idx == 3:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x16, 0xa3, 0x4a) if text == "Must" else RGBColor(0x02, 0x84, 0xc7)
            else:
                r.font.color.rgb = COLOR_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_subsec_title("3.4 Especificación de Requerimientos No Funcionales (RNF)")
    
    tbl_rnf = doc.add_table(rows=9, cols=4)
    tbl_rnf.alignment = WD_TABLE_ALIGNMENT.CENTER
    rnf_headers = ["ID RNF", "Categoría / Atributo", "Especificación Técnica", "Métrica de Verificación"]
    for i, h in enumerate(rnf_headers):
        c = tbl_rnf.cell(0, i)
        set_cell_background(c, "1e3a8a")
        set_cell_margins(c, 100, 100, 100, 100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    rnf_data = [
        ("RNF-01", "Rendimiento & Latencia", "Las operaciones de consulta y cálculo previsional deben responder en menos de 300 ms.", "< 300 ms bajo carga normal"),
        ("RNF-02", "Seguridad & Control RBAC", "Las rutas y componentes deben validar permisos antes de ejecutar acciones de mutación de datos.", "0 accesos no autorizados a sueldos"),
        ("RNF-03", "Persistencia NoSQL Atómica", "Las escrituras en los archivos de base de datos JSON deben ser atómicas para evitar corrupción.", "100% integridad documental"),
        ("RNF-04", "Portabilidad Multiplataforma", "El sistema debe ejecutarse de forma homogénea en Windows, Linux y navegadores modernos.", "Compatible Web, CLI y Desktop GUI"),
        ("RNF-05", "Usabilidad & Accesibilidad", "La interfaz debe ser intuitiva, con soporte de modo claro/oscuro y retroalimentación inmediata.", "SUS (System Usability Scale) > 85"),
        ("RNF-06", "Conformidad Legal (Chile)", "Los cálculos deben respetar taxativamente topes imponibles (UF) y tramos progresivos (UTM).", "0 discrepancias con simulador SII/DT"),
        ("RNF-07", "Disponibilidad & Autonomía", "Las versiones de escritorio en Python deben ser autónomas y operar sin dependencias externas complejas.", "Arranque en 1 clic (ejecutar.bat)"),
        ("RNF-08", "Mantenibilidad & Modularidad", "Arquitectura desacoplada en controladores, rutas, contextos y utilidades reutilizables.", "Cobertura de funciones legales pura")
    ]

    for row_idx, r_item in enumerate(rnf_data, 1):
        for col_idx, text in enumerate(r_item):
            c = tbl_rnf.cell(row_idx, col_idx)
            set_cell_background(c, "f8fafc" if row_idx % 2 == 1 else "ffffff")
            set_cell_margins(c, 70, 70, 80, 80)
            p = c.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            else:
                r.font.color.rgb = COLOR_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_subsec_title("3.5 Validación con Usuarios y Documentación de Ajustes")
    add_p("Durante las sesiones de validación del prototipo con usuarios expertos se identificaron y documentaron los siguientes ajustes clave:")
    add_p("• Ajuste 1 (Control de Sueldos): Los colaboradores manifestaron la necesidad de consultar su sueldo y liquidación, pero RRHH requería que ningún colaborador pudiera editar su remuneración. Se implementó el modo Solo Lectura en el Portal del Colaborador (RF-13).\n• Ajuste 2 (Tope de Gratificación Art. 50): Se refinó el cálculo mensual automático asegurando que el 25% del sueldo base esté topado estrictamente por (4.75 IMM / 12), conforme a la ley chilena.\n• Ajuste 3 (Descuento AFC en Finiquitos Art. 161): Se incorporó el campo opcional para deducir el aporte acumulado del empleador a la cuenta individual de cesantía conforme al Artículo 13 de la Ley 19.728.")

    # =========================================================================
    # SECCIÓN 4: CALIDAD Y TRAZABILIDAD DE REQUERIMIENTOS (10 PUNTOS)
    # =========================================================================
    add_sec_title("4. CALIDAD Y TRAZABILIDAD DE REQUERIMIENTOS")

    add_subsec_title("4.1 Criterios y Estándar de Calidad Aplicados (ISO/IEC/IEEE 29148)")
    add_p("Para garantizar la calidad de la ingeniería de software, cada requerimiento fue evaluado bajo los 6 criterios del estándar internacional ISO/IEC/IEEE 29148:")
    add_p("• Claridad: Lenguaje no ambiguo, comprensible tanto por desarrolladores como por especialistas de RRHH.\n• Consistencia: Inexistencia de conflictos normativos entre haberes, descuentos y causales legales.\n• Completitud: Definición de entradas, salidas, condiciones de error y valores predeterminados.\n• Factibilidad: Implementabilidad técnica con base de datos NoSQL y motores de cálculo en JS/Python.\n• Verificabilidad: Existencia de criterios de aceptación cuantificables para pruebas de software.\n• Trazabilidad: Vinculación unívoca desde la necesidad hasta el diseño y caso de prueba.")

    add_subsec_title("4.2 Matriz de Trazabilidad de Requerimientos (RTM)")
    add_p("La siguiente Matriz de Trazabilidad asegura la coherencia de extremo a extremo entre los Requerimientos Funcionales, los Casos de Uso, las Pantallas de la Interfaz y las Clases UML del Sistema:")

    tbl_rtm = doc.add_table(rows=12, cols=5)
    tbl_rtm.alignment = WD_TABLE_ALIGNMENT.CENTER
    rtm_headers = ["ID RF", "Caso de Uso (CU)", "Mockup / Pantalla", "Clase UML / Módulo", "Criterio de Verificación"]
    for i, h in enumerate(rtm_headers):
        c = tbl_rtm.cell(0, i)
        set_cell_background(c, "1e3a8a")
        set_cell_margins(c, 100, 100, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    rtm_data = [
        ("RF-01", "CU-01 Iniciar Sesión", "Pantalla 1: Login RBAC", "User, AuthController", "Login exitoso y asignación de rol correcto."),
        ("RF-02", "CU-02 Gestionar Colaborador", "Pantalla 3: Expediente 360", "Employee, EmployeeList", "CRUD completo persistente en NoSQL."),
        ("RF-03", "CU-03 Administrar Deptos", "Pantalla 2: Dashboard", "Department, DeptManager", "Cálculo dinámico de headcount y masa salarial."),
        ("RF-04", "CU-05 Solicitar Permiso", "Pantalla 6: Portal Colaborador", "LeaveRequest, LeaveManager", "Aprobación/Rechazo cambia estado a Aprobado."),
        ("RF-05", "CU-07 Evaluar Desempeño", "Pantalla 6: Portal Colaborador", "Evaluation, EvalManager", "Promedio ponderado 1-5 estrellas almacenado."),
        ("RF-06", "CU-04 Liquidar Sueldo Chile", "Pantalla 4: Liquidación Chile", "PayslipChile, legal_chile.py", "Suma correcta de imponibles y gratificación Art. 50."),
        ("RF-07", "CU-04 Liquidar Sueldo Chile", "Pantalla 4: Liquidación Chile", "PayslipChile, legal_chile.py", "Deducciones de AFP y Salud según tasas vigentes."),
        ("RF-08", "CU-04 Liquidar Sueldo Chile", "Pantalla 4: Liquidación Chile", "PayslipChile, legal_chile.py", "Aplicación exacta de tramos progresivos SII en UTM."),
        ("RF-10", "CU-05 Emitir Finiquito", "Pantalla 5: Finiquitos DT", "SettlementChile, SettlementMgr", "Art. 159 no calcula años; Art. 161 sí calcula años."),
        ("RF-13", "CU-08 Portal Privado", "Pantalla 6: Portal Colaborador", "WorkerPortal, WorkerUser", "Trabajador visualiza sueldo sin opción de editar."),
        ("RF-15", "CU-04 Liquidar Sueldo Chile", "Pantalla 4 & Pantalla 6", "EmailController, WorkerPortal", "Despacho por correo electrónico del colaborador con confirmación visual.")
    ]

    for row_idx, r_item in enumerate(rtm_data, 1):
        for col_idx, text in enumerate(r_item):
            c = tbl_rtm.cell(row_idx, col_idx)
            set_cell_background(c, "f8fafc" if row_idx % 2 == 1 else "ffffff")
            set_cell_margins(c, 60, 60, 70, 70)
            p = c.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            else:
                r.font.color.rgb = COLOR_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # SECCIÓN 5: DIAGRAMA DE CASOS DE USO Y ESPECIFICACIONES FORMALES (15 PUNTOS)
    # =========================================================================
    add_sec_title("5. DIAGRAMA DE CASOS DE USO Y ESPECIFICACIONES FORMALES")

    add_subsec_title("5.1 Diagrama de Casos de Uso del Sistema (UML 2.5)")
    add_p("El diagrama modela las interacciones entre los actores del sistema y los casos de uso principales, reflejando el límite del sistema TalentHub HR y las dependencias entre paquetes:")

    if os.path.exists("diagramas_informe/figura2_casos_de_uso.png"):
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("diagramas_informe/figura2_casos_de_uso.png", width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 2: Diagrama de Casos de Uso UML del Sistema TalentHub HR")
        r_cap.font.name = "Segoe UI"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_GRAY

    add_subsec_title("5.2 Especificaciones Formales de Casos de Uso Principales")

    # Función para renderizar plantilla de Caso de Uso
    def add_use_case_spec(cu_id, cu_name, actor, purpose, precond, main_flow, alt_flows, postcond, rules):
        p_cu = doc.add_paragraph()
        p_cu.paragraph_format.space_before = Pt(8)
        p_cu.paragraph_format.space_after = Pt(2)
        r_cu = p_cu.add_run(f"Especificación Formal: {cu_id} - {cu_name}")
        r_cu.font.name = "Segoe UI"
        r_cu.font.size = Pt(10)
        r_cu.font.bold = True
        r_cu.font.color.rgb = COLOR_PRIMARY

        tbl = doc.add_table(rows=7, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        fields = [
            ("Actor(es) Principal(es):", actor),
            ("Propósito / Objetivo:", purpose),
            ("Precondiciones:", precond),
            ("Flujo Principal de Eventos:", main_flow),
            ("Flujos Alternativos / Excepciones:", alt_flows),
            ("Postcondiciones:", postcond),
            ("Reglas de Negocio / Legales:", rules)
        ]
        for row_idx, (f_name, f_val) in enumerate(fields):
            c0 = tbl.cell(row_idx, 0)
            c1 = tbl.cell(row_idx, 1)
            c0.width = Inches(2.0)
            c1.width = Inches(4.5)
            set_cell_background(c0, "f1f5f9")
            set_cell_background(c1, "ffffff")
            set_cell_margins(c0, 60, 60, 80, 80)
            set_cell_margins(c1, 60, 60, 80, 80)

            p0 = c0.paragraphs[0]
            r0 = p0.add_run(f_name)
            r0.font.name = "Segoe UI"
            r0.font.size = Pt(8.5)
            r0.font.bold = True
            r0.font.color.rgb = COLOR_SECONDARY

            p1 = c1.paragraphs[0]
            r1 = p1.add_run(f_val)
            r1.font.name = "Segoe UI"
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = COLOR_TEXT
        
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # CU-01
    add_use_case_spec(
        "CU-01", "Iniciar Sesión con Control de Roles (RBAC)",
        "Administrador RRHH, Trabajador / Colaborador",
        "Autenticar la identidad del usuario y otorgar permisos correspondientes a su perfil.",
        "El usuario debe existir en la base de datos NoSQL con credenciales válidas.",
        "1. El usuario ingresa a la pantalla de inicio de sesión.\n2. Ingresa su identificador (usuario o correo) y contraseña.\n3. Presiona 'Acceder a la Plataforma'.\n4. El sistema valida las credenciales y el rol asignado.\n5. Si el rol es 'admin', despliega el panel administrativo completo.\n6. Si el rol es 'worker', despliega el Portal del Colaborador (modo protegido).",
        "4a. Credenciales incorrectas: El sistema muestra mensaje de error y permite reintentar.\n4b. Usuario inactivo: El sistema deniega el acceso informando su estado.",
        "Sesión activa con token/estado en memoria y control de vistas según permisos.",
        "RN-01: Contraseñas no vacías; RN-02: Los trabajadores tienen permisos de solo lectura sobre sueldos."
    )

    # CU-02
    add_use_case_spec(
        "CU-02", "Gestionar Expediente 360° de Colaboradores",
        "Administrador RRHH",
        "Administrar el ciclo de vida de los colaboradores (Alta, consulta, modificación y expediente 360).",
        "El Administrador debe tener una sesión activa con permisos de gestión.",
        "1. El Administrador selecciona 'Colaboradores' en el menú.\n2. El sistema despliega la lista con buscador y filtros.\n3. Para dar de alta: Selecciona 'Nuevo Colaborador', completa formulario con datos personales, cargo, depto y sueldo base, y guarda.\n4. Para consultar: Selecciona 'Expediente 360°' para ver ficha, historial de ausencias y desempeño.\n5. Para editar: Modifica datos contractuales o remuneración.",
        "3a. Correo ya registrado: El sistema impide duplicidad y notifica al usuario.\n3b. Campos obligatorios vacíos: El sistema resalta campos requeridos.",
        "Colaborador registrado/actualizado en la colección NoSQL 'employees.json'.",
        "RN-03: El RUT debe cumplir formato chileno; RN-04: Solo el Administrador puede modificar sueldos."
    )

    # CU-03
    add_use_case_spec(
        "CU-03", "Calcular y Emitir Liquidación de Sueldo (Chile)",
        "Administrador RRHH, Trabajador (Solo Consulta)",
        "Calcular la remuneración mensual aplicando la normativa previsional y tributaria chilena.",
        "El colaborador debe estar activo y poseer sueldo base definido.",
        "1. El usuario accede al módulo 'Liquidación de Sueldo' (o el colaborador a 'Mis Liquidaciones').\n2. Selecciona un colaborador o ingresa parámetros manualmente.\n3. El sistema calcula automáticamente Gratificación Art. 50, horas extras 50% y haberes no imponibles.\n4. El sistema calcula descuentos legales: AFP según tabla de comisiones, Fonasa (7%) o Isapre, AFC (0.6%) e Impuesto Único de Segunda Categoría (SII en UTM).\n5. El sistema presenta el desglose formal y el Alcance Líquido a Transferir.\n6. El usuario o colaborador puede imprimir, exportar o enviar directamente el comprobante oficial a su correo electrónico institucional registrado (RF-15).",
        "4a. Renta excede tope imponible: El sistema trunca la base de cálculo al tope legal (84.3 UF para AFP/Salud y 126.6 UF para AFC).",
        "Liquidación calculada y comprobante oficial emitido.",
        "RN-05: Gratificación Art. 50 topada al 25% de 4.75 IMM / 12; RN-06: Descuentos de salud respetan el 7% mínimo legal."
    )

    # CU-04
    add_use_case_spec(
        "CU-04", "Simular y Emitir Finiquito Legal (Renuncia vs Despido)",
        "Administrador RRHH",
        "Calcular indemnizaciones y haberes finales según la causal del Código del Trabajo.",
        "El colaborador debe estar registrado en el sistema con fecha de contratación válida.",
        "1. El Administrador accede al módulo 'Finiquitos Laborales'.\n2. Selecciona al colaborador y la causal legal (Art. 159 N° 2 Renuncia o Art. 161 Necesidades).\n3. Ingresa fecha de cese y días de vacaciones ya tomadas.\n4. Si es Art. 161: Indica si medió aviso previo de 30 días y aporte empleador AFC acumulado.\n5. El sistema calcula días trabajados, feriado proporcional y, si aplica, años de servicio (Art. 163).\n6. El sistema genera el Documento Legal de la Dirección del Trabajo (DT) y actualiza al trabajador a 'Inactivo'.",
        "2a. Renuncia Voluntaria (Art. 159): El sistema NO liquida indemnización por años ni aviso previo.",
        "Finiquito persistido en 'settlements.json' y colaborador pasa a estado Inactivo.",
        "RN-07: Años de servicio se calculan con 1 mes por año y fracción superior a 6 meses (tope 11 años y 90 UF)."
    )

    # CU-05
    add_use_case_spec(
        "CU-05", "Solicitar y Autorizar Vacaciones / Permisos",
        "Trabajador / Colaborador (Solicitante), Administrador RRHH (Autorizador)",
        "Gestionar el flujo de ausencias laborales desde la solicitud hasta la resolución formal.",
        "El trabajador debe estar activo y poseer saldo de días devengados.",
        "1. El Colaborador accede a 'Mis Vacaciones' y selecciona 'Solicitar Permiso'.\n2. Ingresa tipo de ausencia, fechas de inicio y término, y motivo.\n3. El sistema calcula días hábiles y registra la solicitud en estado 'Pendiente'.\n4. El Administrador visualiza la solicitud en su panel y selecciona 'Aprobar' o 'Rechazar' con comentarios.\n5. El sistema actualiza el estado y notifica al colaborador en su portal.",
        "4a. Rechazo: El Administrador debe ingresar una justificación obligatoria.",
        "Solicitud actualizada en 'leaves.json' reflejada en el expediente 360°.",
        "RN-08: Todo trabajador acumula legalmente 1.25 días hábiles de vacaciones por mes trabajado."
    )

    # =========================================================================
    # SECCIÓN 6: DIAGRAMA DE CLASES DEL SISTEMA (15 PUNTOS)
    # =========================================================================
    add_sec_title("6. DIAGRAMA DE CLASES DEL SISTEMA")

    add_subsec_title("6.1 Modelo de Clases Estructural (UML 2.5)")
    add_p("El siguiente diagrama modela las entidades del dominio, su comportamiento (métodos), atributos encapsulados y relaciones de asociación, composición y herencia:")

    if os.path.exists("diagramas_informe/figura3_diagrama_clases.png"):
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("diagramas_informe/figura3_diagrama_clases.png", width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 3: Diagrama de Clases UML del Sistema TalentHub HR")
        r_cap.font.name = "Segoe UI"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_GRAY

    add_subsec_title("6.2 Diccionario de Clases, Responsabilidades y Relaciones")
    add_p("• User (Clase Abstracta): Modela la identidad base, credenciales y rol (Admin vs Worker). Permite la autenticación y resolución de permisos.\n• Employee: Representa al colaborador en la organización. Encapsula datos personales, cargo, remuneración base y estado laboral. Posee métodos para calcular antigüedad y emitir expediente 360°.\n• Department: Modela las áreas funcionales de la empresa. Calcula dinámicamente la plantilla y masa salarial total sumando los sueldos de sus colaboradores asignados.\n• PayslipChile: Modela la liquidación de sueldo bajo legislación chilena. Contiene la lógica pura de haberes imponibles/no imponibles, descuentos previsionales (AFP, Fonasa/Isapre, AFC) e IUSC del SII.\n• SettlementChile: Modela el finiquito de contrato de trabajo. Calcula indemnizaciones legales por despido Art. 161, feriado proporcional y genera el documento oficial de la DT.\n• LeaveRequest: Modela las ausencias y vacaciones, controlando el ciclo de vida de la solicitud (Pendiente, Aprobado, Rechazado).\n• Evaluation: Modela las revisiones de desempeño, almacenando calificaciones en 5 competencias con escala de estrellas y planes de desarrollo.")

    # =========================================================================
    # SECCIÓN 7: MOCKUPS Y DISEÑO DE INTERFAZ DE USUARIO (10 PUNTOS)
    # =========================================================================
    add_sec_title("7. MOCKUPS Y DISEÑO DE INTERFAZ DE USUARIO")

    add_subsec_title("7.1 Arquitectura de Información y Capas del Sistema")
    add_p("TalentHub HR se diseñó bajo un modelo desacoplado de tres capas que garantiza alta disponibilidad, mantenibilidad e interoperabilidad:")

    if os.path.exists("diagramas_informe/figura4_arquitectura.png"):
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("diagramas_informe/figura4_arquitectura.png", width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 4: Arquitectura Multiplataforma Desacoplada del Sistema")
        r_cap.font.name = "Segoe UI"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_GRAY

    add_subsec_title("7.2 Especificación Detallada de Pantallas Clave")

    screens_data = [
        ("Pantalla 1: Inicio de Sesión & Selector Rápido de Roles (RBAC)",
         "Todos los usuarios (Administradores y Trabajadores).",
         "Autenticar y canalizar al usuario según sus privilegios de acceso.",
         "Formulario con campos de usuario y contraseña, alertas dinámicas de error, y botones de Acceso Rápido en 1 Clic para cuentas demo (Admin vs Trabajadores).",
         "RF-01, RNF-02",
         "Al autenticar como Admin redirige a la vista completa; como Trabajador redirige al Portal del Colaborador."),
        
        ("Pantalla 2: Panel de Control (Dashboard) & Métricas de RRHH",
         "Administrador RRHH, Gerencia General.",
         "Monitorear en tiempo real los indicadores clave (KPIs), dotación y masa salarial de la empresa.",
         "Tarjetas métricas (Total colaboradores, activos, en permiso, masa salarial mensual, desempeño promedio), gráfico de barras por departamento y tabla de solicitudes pendientes.",
         "RF-02, RF-03, RF-04",
         "Acceso rápido a revisar solicitudes de vacaciones pendientes con 1 clic."),
        
        ("Pantalla 3: Gestión de Colaboradores & Expediente 360°",
         "Administrador RRHH.",
         "Administrar la plantilla completa y consultar el historial integral de cada colaborador.",
         "Tabla interactiva con buscador en vivo, filtros por estado/área, botones de Alta, Edición con modificación de sueldo, Baja y Modal de Expediente 360° (ficha, ausencias y evaluaciones).",
         "RF-02, RF-14",
         "Exportación de la nómina completa a formato CSV / Excel."),
        
        ("Pantalla 4: Calculadora Legal de Liquidación de Sueldo (Chile)",
         "Administrador RRHH.",
         "Simular y emitir liquidaciones con todos los descuentos legales de Chile y envío por correo.",
         "Selector de colaboradores para precarga de sueldo, inputs de gratificación Art. 50, horas extras, selector de AFPs con comisiones, Fonasa/Isapre, AFC, desglose de IUSC, botón de impresión y botón de Envío por Correo.",
         "RF-06, RF-07, RF-08, RF-09, RF-15",
         "Generación de comprobante digital formal para impresión con formato Dirección del Trabajo y despacho por email institucional."),
        
        ("Pantalla 5: Gestor de Finiquitos Laborales (Renuncia vs Despido)",
         "Administrador RRHH.",
         "Calcular indemnizaciones legales y emitir el documento oficial de término de contrato.",
         "Selector de causal (Art. 159 N° 2 Renuncia vs Art. 161 Despido), inputs de vacaciones tomadas y aviso previo, visualizador de desglose de indemnizaciones y botón de emisión notarial DT.",
         "RF-10, RF-11",
         "Persistencia en NoSQL y actualización automática del colaborador a estado 'Inactivo'."),
        
        ("Pantalla 6: Portal Privado del Colaborador (Worker Portal)",
         "Trabajador / Colaborador autenticado.",
         "Permitir al colaborador consultar su desempeño, liquidaciones de sueldo, solicitar vacaciones y enviarse la liquidación a su correo personal.",
         "Pestañas: (1) Mi Ficha con Sueldo Solo Lectura protegido; (2) Mi Historial de Desempeño con estrellas y feedback; (3) Mis Liquidaciones con botón 'Enviar a Mi Correo'; (4) Mis Vacaciones con formulario de solicitud.",
         "RF-04, RF-05, RF-12, RF-13, RF-15",
         "El colaborador no puede editar sueldos ni acceder a información de otros empleados; puede despachar su liquidación a su correo.")
    ]

    for title, user_t, prop, comp, rfs, nav in screens_data:
        p_sc = doc.add_paragraph()
        p_sc.paragraph_format.space_before = Pt(8)
        p_sc.paragraph_format.space_after = Pt(2)
        r_sc = p_sc.add_run(f"📋 {title}")
        r_sc.font.name = "Segoe UI"
        r_sc.font.size = Pt(10)
        r_sc.font.bold = True
        r_sc.font.color.rgb = COLOR_PRIMARY

        tbl_sc = doc.add_table(rows=5, cols=2)
        tbl_sc.alignment = WD_TABLE_ALIGNMENT.CENTER
        sc_fields = [
            ("Usuario Destino:", user_t),
            ("Propósito Funcional:", prop),
            ("Componentes & Elementos:", comp),
            ("Requerimientos Trazables:", rfs),
            ("Navegación & Acciones:", nav)
        ]
        for row_idx, (lbl, val) in enumerate(sc_fields):
            c0 = tbl_sc.cell(row_idx, 0)
            c1 = tbl_sc.cell(row_idx, 1)
            c0.width = Inches(2.0)
            c1.width = Inches(4.5)
            set_cell_background(c0, "f8fafc")
            set_cell_background(c1, "ffffff")
            set_cell_margins(c0, 50, 50, 70, 70)
            set_cell_margins(c1, 50, 50, 70, 70)

            p0 = c0.paragraphs[0]
            r0 = p0.add_run(lbl)
            r0.font.name = "Segoe UI"
            r0.font.size = Pt(8.5)
            r0.font.bold = True
            r0.font.color.rgb = COLOR_SECONDARY

            p1 = c1.paragraphs[0]
            r1 = p1.add_run(val)
            r1.font.name = "Segoe UI"
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = COLOR_TEXT

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # SECCIÓN 8: CONCLUSIONES Y TRABAJO FUTURO (3 PUNTOS)
    # =========================================================================
    add_sec_title("8. CONCLUSIONES Y PROYECCIÓN DEL PROYECTO")

    add_subsec_title("8.1 Síntesis de Decisiones y Aprendizajes de la Etapa")
    add_p("El desarrollo de la Etapa 2 de TalentHub HR permitió consolidar una arquitectura de software robusta, desacoplada y formalmente alineada con la realidad laboral y tributaria de Chile. La adopción de la metodología Scrum facilitó la iteración rápida de las reglas de negocio, logrando un modelado conceptual y estructural (Casos de Uso y Diagrama de Clases UML 2.5) que resuelve de forma elegante la complejidad del cálculo de remuneraciones y finiquitos.")
    add_p("Asimismo, la implementación del esquema de Control de Acceso Basado en Roles (RBAC) demostró ser un factor crítico de éxito, garantizando la confidencialidad de la información salarial corporativa mientras empodera al colaborador mediante un portal de autoservicio transparente.")

    add_subsec_title("8.2 Proyección hacia la Construcción y Certificación")
    add_p("El nivel de detalle y trazabilidad alcanzado en este informe técnico establece un puente sólido hacia la etapa final de pruebas automatizadas, pruebas de estrés y certificación del prototipo. La coexistencia verificada de la plataforma Web (React + Express) junto con las versiones autónomas de escritorio en Python (CLI y GUI Tkinter) sobre el motor NoSQL documental asegura que TalentHub HR es una solución versátil, lista para su despliegue operativo en empresas y PyMEs a lo largo del país.")

    # =========================================================================
    # SECCIÓN 9: REFERENCIAS BIBLIOGRÁFICAS & NORMATIVAS (2 PUNTOS)
    # =========================================================================
    add_sec_title("9. REFERENCIAS BIBLIOGRÁFICAS Y NORMATIVAS")

    refs = [
        "1. Código del Trabajo de la República de Chile (Edición Oficial 2026). Artículos 41 a 50 (Remuneraciones y Gratificación Legal), Artículos 67 a 76 (Feriado Anual y Proporcional), Artículos 159 a 177 (Terminación del Contrato de Trabajo y Finiquito).",
        "2. Dirección del Trabajo de Chile (DT). Dictámenes y Manuales Oficiales para la Ratificación de Finiquitos Laborales y Liquidaciones de Sueldo Electrónicas.",
        "3. Servicio de Impuestos Internos de Chile (SII). Tabla de Cálculo del Impuesto Único de Segunda Categoría (Art. 43 N° 1 LIR) y valores oficiales de la Unidad Tributaria Mensual (UTM).",
        "4. Superintendencia de Pensiones de Chile (SP). Régimen de Cotizaciones Obligatorias de AFPs, Seguro de Invalidez y Sobrevivencia (SIS) y Topes Imponibles en Unidades de Fomento (UF).",
        "5. Ley N° 19.728 que Establece un Seguro de Cesantía para los Trabajadores (AFC Chile). Artículo 13 relativo a la imputación de aportes del empleador al finiquito por necesidades de la empresa.",
        "6. IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018. Systems and software engineering — Life cycle processes — Requirements engineering.",
        "7. Object Management Group (OMG). Unified Modeling Language (UML) Specification, Version 2.5.1 (2017).",
        "8. Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.",
        "9. Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education."
    ]

    for ref in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(2)
        p_r.paragraph_format.space_after = Pt(3)
        p_r.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p_r.add_run(ref)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        r.font.color.rgb = COLOR_TEXT

    # Guardar en el escritorio
    output_path = r"C:\Users\19093075-0\Desktop\INFORME_ETAPA_2_TALENTHUB_HR.docx"
    try:
        doc.save(output_path)
        print("DOCUMENTO WORD GENERADO EXITOSAMENTE EN: " + output_path)
    except PermissionError:
        fallback_path = r"C:\Users\19093075-0\Desktop\INFORME_ETAPA_2_TALENTHUB_HR_ACTUALIZADO.docx"
        doc.save(fallback_path)
        print("DOCUMENTO WORD GENERADO EXITOSAMENTE EN COPIA ACTUALIZADA: " + fallback_path)

if __name__ == "__main__":
    build_document()
