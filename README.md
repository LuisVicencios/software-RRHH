# 🏢 TalentHub HR - Plataforma Integral de Recursos Humanos (RRHH)

Sistema web profesional, moderno e intuitivo de Recursos Humanos con arquitectura desacoplada (**Frontend React + Tailwind CSS** y **Backend Node.js Express REST API**) con persistencia en **Base de Datos NoSQL** basada en documentos JSON (NeDB / compatible con MongoDB Atlas).

---

## ✨ Características Principales

1. **Dashboard & Analítica de RRHH (KPIs en tiempo real)**
   - Conteo de colaboradores totales, activos, en permiso y en prueba.
   - Gráficos interactivos de distribución por departamento y modalidad de trabajo (Presencial, Híbrido, Remoto).
   - Acceso rápido a aprobación de vacaciones y recordatorios de próximos cumpleaños.

2. **Gestión de Colaboradores (CRUD Completo)**
   - Alta, edición, filtrado y eliminación con confirmación.
   - Vista en Cuadrícula (Cards) y Vista en Tabla.
   - Búsqueda en vivo por nombre, cargo, correo o RUT/ID.
   - **Expediente 360°**: Visualización de ficha laboral, habilidades, historial de vacaciones, evaluaciones y recibo de sueldo.
   - Exportación de la plantilla a formato **CSV / Excel**.

3. **Estructura Organizacional & Departamentos (CRUD Completo)**
   - Creación y edición de departamentos, asignación de líder, presupuesto y color identificador.
   - Conteo en tiempo real de plantilla asignada y cálculo de masa salarial por área.

4. **Vacaciones & Permisos (CRUD & Workflow de Aprobación)**
   - Solicitud de vacaciones, licencias médicas, días personales y capacitaciones.
   - Cálculo automático de días de ausencia.
   - Flujo de revisión con 1-clic para **Aprobar / Rechazar** con comentarios del evaluador.

5. **Evaluaciones de Desempeño (CRUD Completo)**
   - Puntuación 1 a 5 estrellas en 5 competencias clave (Técnica, Trabajo en equipo, Puntualidad, Liderazgo, Cumplimiento de metas).
   - Registro de fortalezas, oportunidades de mejora y objetivos del siguiente periodo.

6. **Nóminas & Recibos de Sueldo**
   - Resumen financiero de sueldo bruto, cotizaciones previsionales (Salud 7%, AFP 10%, Seguro de Cesantía) y líquido a pagar.
   - Generación e impresión directa de **Recibo de Sueldo Digital**.

7. **Base de Datos NoSQL Persistente**
   - Colecciones de documentos JSON persistentes en disco (`server/data/*.db`).
   - Botón interactivo en la barra superior para **Restaurar Datos de Demostración** con 1 clic.
   - Soporte para conexión a MongoDB Atlas mediante variable de entorno `MONGODB_URI`.

---

## 🚀 Cómo Iniciar el Proyecto

### 1. Iniciar el Backend (Servidor NoSQL en Puerto 5000)
Abre una terminal y ejecuta:
```bash
cd server
npm run dev
```

### 2. Iniciar el Frontend (Aplicación Web en Puerto 5173)
Abre otra terminal y ejecuta:
```bash
cd client
npm run dev
```

Luego abre tu navegador en **`http://localhost:5173`**.

---

## 🛠️ Tecnologías Utilizadas

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React Icons, Recharts, Canvas-Confetti.
- **Backend**: Node.js, Express, CORS, Morgan, NeDB-Promises (NoSQL Document Store).
- **Base de Datos**: NoSQL Document Database con persistencia local en `server/data/`.
