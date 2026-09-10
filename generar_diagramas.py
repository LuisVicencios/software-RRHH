import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs("diagramas_informe", exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8

def generate_gantt_chart():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    tasks = [
        "Sprint 1: Levantamiento & Arquitectura NoSQL",
        "Sprint 1: CRUD Empleados & Departamentos",
        "Sprint 2: Vacaciones & Evaluaciones 360",
        "Sprint 2: Sistema de Login & Roles RBAC",
        "Sprint 3: Motor Liquidacion de Sueldo Chile",
        "Sprint 3: Gestor de Finiquitos (Art. 159 / 161)",
        "Sprint 4: Portal del Colaborador (Solo Lectura)",
        "Sprint 4: Version Consola CLI & Desktop GUI",
        "Sprint 4: Pruebas de Calidad, QA & Despliegue"
    ]
    start_days = [1, 5, 12, 16, 22, 27, 34, 38, 44]
    durations =  [6, 7,  6,  7,  7,  8,  6,  7,  7]
    colors = ['#4f46e5', '#4f46e5', '#0ea5e9', '#0ea5e9', '#10b981', '#10b981', '#f59e0b', '#8b5cf6', '#64748b']

    y_pos = np.arange(len(tasks))
    ax.barh(y_pos, durations, left=start_days, color=colors, height=0.55, edgecolor='none', alpha=0.9)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(tasks, fontsize=9, fontweight='bold', color='#1e293b')
    ax.invert_yaxis()
    ax.set_xlabel('Dias del Proyecto (Semanas 1 a 8)', fontsize=10, fontweight='bold', color='#334155', labelpad=10)
    ax.set_title('Figura 1: Carta Gantt del Proyecto TalentHub HR (Ciclo de Vida Scrum)', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
    
    for sprint_day in [1, 14, 28, 42, 52]:
        ax.axvline(x=sprint_day, color='#94a3b8', linestyle='--', linewidth=0.8, alpha=0.7)
    
    ax.text(7, -0.7, 'Sprint 1', ha='center', fontsize=8, fontweight='bold', color='#4f46e5')
    ax.text(21, -0.7, 'Sprint 2', ha='center', fontsize=8, fontweight='bold', color='#0ea5e9')
    ax.text(35, -0.7, 'Sprint 3', ha='center', fontsize=8, fontweight='bold', color='#10b981')
    ax.text(47, -0.7, 'Sprint 4', ha='center', fontsize=8, fontweight='bold', color='#8b5cf6')

    ax.grid(axis='x', linestyle=':', alpha=0.6)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig("diagramas_informe/figura1_carta_gantt.png", bbox_inches='tight')
    plt.close()
    print("Carta Gantt generada.")

def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    sys_rect = patches.FancyBboxPatch((2.6, 0.5), 6.8, 9.0, boxstyle="round,pad=0.2", fc="#f8fafc", ec="#4f46e5", lw=2, linestyle='-')
    ax.add_patch(sys_rect)
    ax.text(6.0, 9.2, "Sistema TalentHub HR (Limite del Sistema)", ha='center', fontsize=12, fontweight='bold', color='#4f46e5')

    # Actores
    # Admin
    ax.plot(1.2, 7.0, 'o', markersize=14, color='#312e81', fillstyle='full')
    ax.plot([1.2, 1.2], [6.2, 6.8], color='#312e81', lw=2)
    ax.plot([0.8, 1.6], [6.5, 6.5], color='#312e81', lw=2)
    ax.plot([1.2, 0.9], [6.2, 5.6], color='#312e81', lw=2)
    ax.plot([1.2, 1.5], [6.2, 5.6], color='#312e81', lw=2)
    ax.text(1.2, 5.2, "Administrador\nRRHH", ha='center', fontsize=9, fontweight='bold', color='#1e293b')

    # Colaborador
    ax.plot(1.2, 2.5, 'o', markersize=14, color='#0ea5e9', fillstyle='full')
    ax.plot([1.2, 1.2], [1.7, 2.3], color='#0ea5e9', lw=2)
    ax.plot([0.8, 1.6], [2.0, 2.0], color='#0ea5e9', lw=2)
    ax.plot([1.2, 0.9], [1.7, 1.1], color='#0ea5e9', lw=2)
    ax.plot([1.2, 1.5], [1.7, 1.1], color='#0ea5e9', lw=2)
    ax.text(1.2, 0.7, "Trabajador /\nColaborador", ha='center', fontsize=9, fontweight='bold', color='#1e293b')

    # Externo
    ax.plot(10.8, 4.5, 'o', markersize=14, color='#10b981', fillstyle='full')
    ax.plot([10.8, 10.8], [3.7, 4.3], color='#10b981', lw=2)
    ax.plot([10.4, 11.2], [4.0, 4.0], color='#10b981', lw=2)
    ax.plot([10.8, 10.5], [3.7, 3.1], color='#10b981', lw=2)
    ax.plot([10.8, 11.1], [3.7, 3.1], color='#10b981', lw=2)
    ax.text(10.8, 2.7, "<<Sistema Externo>>\nDT / SII / AFPs", ha='center', fontsize=8, fontweight='bold', color='#1e293b')

    use_cases = [
        (6.0, 8.4, "CU-01: Iniciar Sesion con Roles (RBAC)", "#e0e7ff", "#4338ca"),
        (6.0, 7.3, "CU-02: Gestionar Colaboradores & Ficha 360", "#e0e7ff", "#4338ca"),
        (6.0, 6.2, "CU-03: Administrar Departamentos & Estructura", "#e0e7ff", "#4338ca"),
        (6.0, 5.1, "CU-04: Calcular Liquidacion de Sueldo (Chile)", "#dcfce7", "#15803d"),
        (6.0, 4.0, "CU-05: Emitir Finiquito (Renuncia vs Despido)", "#dcfce7", "#15803d"),
        (6.0, 2.9, "CU-06: Gestionar Solicitudes de Vacaciones", "#e0f2fe", "#0369a1"),
        (6.0, 1.8, "CU-07: Registrar Evaluaciones de Desempeno", "#fef3c7", "#b45309"),
        (6.0, 0.9, "CU-08: Consultar Portal Privado (Solo Lectura)", "#e0f2fe", "#0369a1")
    ]

    for x, y, text, fc, ec in use_cases:
        oval = patches.FancyBboxPatch((x-2.2, y-0.35), 4.4, 0.7, boxstyle="round,pad=0.2", fc=fc, ec=ec, lw=1.5)
        ax.add_patch(oval)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='#0f172a')

    for uy in [8.4, 7.3, 6.2, 5.1, 4.0, 2.9, 1.8]:
        ax.plot([1.6, 3.8], [6.5, uy], color='#4f46e5', lw=1.2, linestyle='-')

    for uy in [8.4, 2.9, 0.9]:
        ax.plot([1.6, 3.8], [2.0, uy], color='#0ea5e9', lw=1.2, linestyle='-')

    ax.plot([8.2, 10.4], [5.1, 4.2], color='#10b981', lw=1.2, linestyle='--')
    ax.plot([8.2, 10.4], [4.0, 4.2], color='#10b981', lw=1.2, linestyle='--')

    ax.set_title('Figura 2: Diagrama de Casos de Uso UML del Sistema TalentHub HR', fontsize=12, fontweight='bold', color='#0f172a', pad=10)
    plt.tight_layout()
    plt.savefig("diagramas_informe/figura2_casos_de_uso.png", bbox_inches='tight')
    plt.close()
    print("Diagrama de Casos de Uso generado.")

def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(13, 8.5), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    def draw_class(x, y, w, h, title, attributes, methods, bg="#ffffff", header_bg="#4f46e5"):
        rect = patches.Rectangle((x, y), w, h, fc=bg, ec='#334155', lw=1.2)
        ax.add_patch(rect)
        h_rect = patches.Rectangle((x, y + h - 0.6), w, 0.6, fc=header_bg, ec='#334155', lw=1.2)
        ax.add_patch(h_rect)
        ax.text(x + w/2, y + h - 0.3, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')

        attr_y = y + h - 0.8
        for attr in attributes:
            ax.text(x + 0.15, attr_y, attr, fontsize=7.2, color='#1e293b')
            attr_y -= 0.28

        div_y = y + h - 0.6 - (len(attributes) * 0.28) - 0.1
        ax.plot([x, x + w], [div_y, div_y], color='#94a3b8', lw=0.8)

        meth_y = div_y - 0.25
        for meth in methods:
            ax.text(x + 0.15, meth_y, meth, fontsize=7.2, color='#0f172a', fontstyle='italic')
            meth_y -= 0.28

    draw_class(0.5, 6.0, 3.2, 2.8, "User (Abstract)",
               ["- id: String", "- username: String", "- passwordHash: String", "- role: RoleType", "- email: String"],
               ["+ login(pass): Boolean", "+ logout(): Void", "+ getPermissions(): List"],
               bg="#f8fafc", header_bg="#312e81")

    draw_class(4.5, 4.8, 3.8, 4.2, "Employee",
               ["- id: String", "- firstName: String", "- lastName: String", "- rutOrId: String", "- position: String", "- salary: Integer", "- contractType: String", "- hireDate: Date", "- status: EmployeeStatus"],
               ["+ calculateTenure(): Tenure", "+ updateSalary(amount): Void", "+ getDossier360(): Dossier", "+ setInactive(): Void"],
               bg="#ffffff", header_bg="#4f46e5")

    draw_class(9.2, 6.2, 3.3, 2.6, "Department",
               ["- id: String", "- name: String", "- code: String", "- manager: String", "- budget: Integer"],
               ["+ getHeadcount(): Int", "+ getTotalPayroll(): Int", "+ addEmployee(emp): Void"],
               bg="#ffffff", header_bg="#0ea5e9")

    draw_class(0.5, 1.2, 3.6, 3.8, "PayslipChile",
               ["- id: String", "- period: String", "- baseSalary: Integer", "- gratification: Integer", "- afpAmount: Integer", "- healthAmount: Integer", "- afcAmount: Integer", "- taxAmount: Integer", "- netSalary: Integer"],
               ["+ computeImponible(): Int", "+ computeDiscounts(): Int", "+ generateDigitalReceipt(): String", "+ printOfficialDocument(): Void"],
               bg="#ffffff", header_bg="#10b981")

    draw_class(4.8, 0.8, 3.6, 3.6, "SettlementChile",
               ["- id: String", "- causeCode: CauseCode", "- terminationDate: Date", "- workedDaysAmount: Int", "- vacationAmount: Int", "- yearsOfServiceAmount: Int", "- noticeAmount: Int", "- totalLiquido: Int"],
               ["+ calculateLegalSeverance(): Int", "+ computeProportionalHoliday(): Int", "+ exportDTLegalDoc(): File"],
               bg="#ffffff", header_bg="#16a34a")

    draw_class(9.2, 1.5, 3.3, 3.4, "LeaveRequest",
               ["- id: String", "- type: LeaveType", "- startDate: Date", "- endDate: Date", "- daysCount: Int", "- status: RequestStatus", "- reviewNotes: String"],
               ["+ submitRequest(): Void", "+ approve(notes): Void", "+ reject(notes): Void"],
               bg="#ffffff", header_bg="#d97706")

    # Conectores
    ax.plot([3.7, 4.5], [7.2, 7.2], color='#334155', lw=1.2)
    ax.text(3.9, 7.35, "1", fontsize=8, fontweight='bold')
    ax.text(4.3, 7.35, "1", fontsize=8, fontweight='bold')

    ax.plot([8.3, 9.2], [7.2, 7.2], color='#334155', lw=1.2)
    ax.text(8.4, 7.35, "1..*", fontsize=8, fontweight='bold')
    ax.text(9.0, 7.35, "1", fontsize=8, fontweight='bold')

    ax.plot([5.2, 2.3], [4.8, 5.0], color='#334155', lw=1.2)

    ax.plot([6.4, 6.4], [4.8, 4.4], color='#334155', lw=1.2)
    ax.text(6.55, 4.5, "1", fontsize=8, fontweight='bold')
    ax.text(6.55, 4.35, "0..1", fontsize=8, fontweight='bold')

    ax.plot([8.3, 9.8], [5.4, 4.9], color='#334155', lw=1.2)

    ax.set_title('Figura 3: Diagrama de Clases UML del Sistema TalentHub HR', fontsize=12, fontweight='bold', color='#0f172a', pad=10)
    plt.tight_layout()
    plt.savefig("diagramas_informe/figura3_diagrama_clases.png", bbox_inches='tight')
    plt.close()
    print("Diagrama de Clases generado.")

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis('off')

    p_rect = patches.FancyBboxPatch((0.5, 4.5), 10.0, 2.0, boxstyle="round,pad=0.2", fc="#e0e7ff", ec="#4338ca", lw=1.5)
    ax.add_patch(p_rect)
    ax.text(1.0, 6.1, "CAPA DE PRESENTACION & CLIENTES", fontsize=10, fontweight='bold', color='#312e81')

    c1 = patches.FancyBboxPatch((0.8, 4.8), 2.8, 1.0, boxstyle="round,pad=0.1", fc="white", ec="#4338ca", lw=1)
    ax.add_patch(c1)
    ax.text(2.2, 5.3, "Web App (React 18)\nTailwind + Vite", ha='center', va='center', fontsize=8, fontweight='bold')

    c2 = patches.FancyBboxPatch((4.1, 4.8), 2.8, 1.0, boxstyle="round,pad=0.1", fc="white", ec="#4338ca", lw=1)
    ax.add_patch(c2)
    ax.text(5.5, 5.3, "Desktop GUI (Python)\nTkinter / ttk Window", ha='center', va='center', fontsize=8, fontweight='bold')

    c3 = patches.FancyBboxPatch((7.4, 4.8), 2.8, 1.0, boxstyle="round,pad=0.1", fc="white", ec="#4338ca", lw=1)
    ax.add_patch(c3)
    ax.text(8.8, 5.3, "Console CLI (Python)\nInteractive Terminal", ha='center', va='center', fontsize=8, fontweight='bold')

    b_rect = patches.FancyBboxPatch((0.5, 2.2), 10.0, 1.8, boxstyle="round,pad=0.2", fc="#dcfce7", ec="#15803d", lw=1.5)
    ax.add_patch(b_rect)
    ax.text(1.0, 3.6, "CAPA DE SERVICIOS & MOTOR LEGAL (CHILE)", fontsize=10, fontweight='bold', color='#14532d')

    m1 = patches.FancyBboxPatch((0.8, 2.5), 2.1, 0.8, boxstyle="round,pad=0.1", fc="white", ec="#15803d", lw=1)
    ax.add_patch(m1)
    ax.text(1.85, 2.9, "Auth & RBAC\nToken / Session", ha='center', va='center', fontsize=7.5, fontweight='bold')

    m2 = patches.FancyBboxPatch((3.2, 2.5), 2.1, 0.8, boxstyle="round,pad=0.1", fc="white", ec="#15803d", lw=1)
    ax.add_patch(m2)
    ax.text(4.25, 2.9, "Liquidaciones\nAFP / Fonasa / IUSC", ha='center', va='center', fontsize=7.5, fontweight='bold')

    m3 = patches.FancyBboxPatch((5.6, 2.5), 2.1, 0.8, boxstyle="round,pad=0.1", fc="white", ec="#15803d", lw=1)
    ax.add_patch(m3)
    ax.text(6.65, 2.9, "Finiquitos DT\nArt. 159 vs 161", ha='center', va='center', fontsize=7.5, fontweight='bold')

    m4 = patches.FancyBboxPatch((8.0, 2.5), 2.2, 0.8, boxstyle="round,pad=0.1", fc="white", ec="#15803d", lw=1)
    ax.add_patch(m4)
    ax.text(9.1, 2.9, "CRUD & 360\nLeaves / Evaluations", ha='center', va='center', fontsize=7.5, fontweight='bold')

    d_rect = patches.FancyBboxPatch((0.5, 0.2), 10.0, 1.5, boxstyle="round,pad=0.2", fc="#fef3c7", ec="#b45309", lw=1.5)
    ax.add_patch(d_rect)
    ax.text(1.0, 1.3, "CAPA DE PERSISTENCIA DOCUMENTAL (NoSQL)", fontsize=10, fontweight='bold', color='#78350f')

    db_box = patches.FancyBboxPatch((2.5, 0.4), 6.0, 0.7, boxstyle="round,pad=0.1", fc="white", ec="#b45309", lw=1)
    ax.add_patch(db_box)
    ax.text(5.5, 0.75, "Colecciones JSON: employees.db - departments.db - leaves.db - settlements.db", ha='center', va='center', fontsize=8, fontweight='bold')

    ax.annotate('', xy=(5.5, 4.0), xytext=(5.5, 4.5), arrowprops=dict(arrowstyle="<->", color="#334155", lw=2))
    ax.annotate('', xy=(5.5, 1.7), xytext=(5.5, 2.2), arrowprops=dict(arrowstyle="<->", color="#334155", lw=2))

    ax.set_title('Figura 4: Arquitectura Multiplataforma Desacoplada del Sistema TalentHub HR', fontsize=12, fontweight='bold', color='#0f172a', pad=10)
    plt.tight_layout()
    plt.savefig("diagramas_informe/figura4_arquitectura.png", bbox_inches='tight')
    plt.close()
    print("Diagrama de Arquitectura generado.")

if __name__ == "__main__":
    generate_gantt_chart()
    generate_use_case_diagram()
    generate_class_diagram()
    generate_architecture_diagram()
