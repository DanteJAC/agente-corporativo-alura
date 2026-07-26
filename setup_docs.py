import os
import csv
import json

base_dir = "docs"
folders = ["Envios", "Atencion_Cliente", "Siniestros", "Recursos_Humanos", "Operaciones"]
for folder in folders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

# 1. Política de envíos - Markdown
pol_envios = """# Política de Envíos y Entregas - Logística Global Express
## 1. Tiempos de Entrega
- **Envío Estándar (Nacional)**: Entregas en 3 a 5 días hábiles. Costo base: $5.00 USD.
- **Envío Exprés (Nacional)**: Entrega garantizada en 24 horas para ciudades principales. Costo base: $12.00 USD.
- **Envío Same-Day (Mismo Día)**: Solo disponible en zonas metropolitanas si el pedido se recibe antes de las 11:00 AM.
- **Envíos Internacionales**: De 7 a 15 días hábiles, sujeto a retenciones aduanales.

## 2. Restricciones de Carga
No transportamos:
- Materiales altamente inflamables, explosivos o corrosivos.
- Alimentos perecederos que requieran cadena de frío ininterrumpida (a menos que se contrate el servicio "Cold-Chain").
- Joyería de alto valor, efectivo o títulos de valor al portador.
Todo paquete debe estar correctamente embalado en cajas de cartón corrugado doble. El seguro no cubrirá daños si el embalaje es deficiente.

## 3. Intentos de Entrega
Nuestros mensajeros realizarán un máximo de **dos (2) intentos de entrega**. Si el cliente no se encuentra en el domicilio en el segundo intento, el paquete será enviado al Centro de Distribución Local (CEDIS), donde permanecerá por 5 días hábiles antes de ser devuelto al remitente original.
"""
with open(os.path.join(base_dir, "Envios", "politica_envios.md"), "w", encoding="utf-8") as f:
    f.write(pol_envios)

# 2. Procedimiento de rastreo de pedidos - HTML
rastreo_html = """
<html>
<body>
    <h1>Procedimiento de Rastreo y Seguimiento de Paquetes</h1>
    <p>Para rastrear un paquete, el cliente debe ingresar al portal web <strong>www.logisticaglobal.com/tracking</strong> e ingresar su <strong>Código de Seguimiento (Tracking ID)</strong> de 12 a 15 dígitos alfanuméricos.</p>
    <h2>Estados del Envío:</h2>
    <ul>
        <li><strong>Recibido en Origen:</strong> El paquete fue entregado en la sucursal o recolectado.</li>
        <li><strong>En Tránsito:</strong> El paquete viaja entre centros de distribución nacionales o internacionales.</li>
        <li><strong>Proceso Aduanal:</strong> (Solo envíos internacionales) El paquete está siendo revisado por las autoridades aduaneras.</li>
        <li><strong>En Reparto:</strong> El mensajero tiene el paquete y será entregado el día de hoy antes de las 20:00 hrs.</li>
        <li><strong>Intento Fallido:</strong> El mensajero llegó al domicilio pero no hubo quien recibiera. Se realizará otro intento.</li>
        <li><strong>Entregado:</strong> El paquete fue entregado exitosamente. Se requiere firma electrónica.</li>
    </ul>
    <p><em>Soporte:</em> Si el tracking no se actualiza por más de 48 horas hábiles, el cliente debe abrir un ticket de investigación urgente.</p>
</body>
</html>
"""
with open(os.path.join(base_dir, "Envios", "procedimiento_rastreo.html"), "w", encoding="utf-8") as f:
    f.write(rastreo_html)

# 3. Política de reembolsos y siniestros - CSV
siniestros_csv = [
    ["Tipo_Seguro", "Costo_Adicional", "Porcentaje_Cobertura_Robo", "Monto_Maximo_Danio", "Tiempo_Resolucion_Dias"],
    ["Básico (Incluido)", "$0.00", "50%", "$50.00 USD", "30"],
    ["Protección Total", "$5.00 USD", "100%", "$1,500.00 USD", "15"],
    ["Carga Pesada / Industrial", "$25.00 USD", "100%", "$10,000.00 USD", "20"],
    ["Electrónicos Frágiles", "$15.00 USD", "80%", "$3,000.00 USD", "15"]
]
with open(os.path.join(base_dir, "Siniestros", "politica_siniestros.csv"), "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(siniestros_csv)

# 4. Preguntas Frecuentes - JSON
faq_json = {
    "faq": [
        {"pregunta": "¿Qué pasa si no estoy en casa cuando llegue el paquete?", "respuesta": "Realizamos 2 intentos de entrega. Luego, el paquete irá al CEDIS por 5 días hábiles. Si no lo recoges, volverá al remitente."},
        {"pregunta": "¿Puedo cambiar la dirección de entrega una vez enviado?", "respuesta": "Sí, a través de la app móvil, pero solo si el paquete no está en estatus 'En Reparto'. El cambio de dirección tiene un costo administrativo de $2.00 USD y retrasa la entrega 24 horas."},
        {"pregunta": "¿Cuánto cuesta enviar un paquete de 10 kg?", "respuesta": "Depende de la distancia. Un paquete estándar de 10 kg a nivel nacional cuesta aproximadamente $15.00 USD."},
        {"pregunta": "¿Qué hago si mi paquete llega dañado?", "respuesta": "No firmes de conformidad. Toma fotografías del empaque y del producto, y comunícate con atención al cliente antes de 24 horas para iniciar un reclamo."}
    ]
}
with open(os.path.join(base_dir, "Atencion_Cliente", "faq.json"), "w", encoding="utf-8") as f:
    json.dump(faq_json, f, indent=4, ensure_ascii=False)

# 5. Proceso de reclamos - Markdown
proceso_reclamos = """# Manual de Atención al Cliente: Reclamos y Quejas
## 1. Iniciación del Reclamo
Todo reclamo por pérdida total, daño físico o retraso excesivo debe ser iniciado dentro de los **7 días calendario** posteriores a la fecha de entrega o fecha estimada de entrega.
No se aceptarán reclamos fuera de este período sin excepción.

## 2. Pasos para el Cliente
1. Enviar un correo electrónico a **reclamos@logisticaglobal.com** indicando el número de guía (tracking ID).
2. Adjuntar evidencia fotográfica clara de los 4 lados de la caja y del producto dañado.
3. Adjuntar la factura de compra original para validar el valor declarado.

## 3. Flujo Interno (SLA de Resolución)
1. **Atención Inicial**: Un agente revisará el caso y asignará un ticket en el sistema Zendesk (Tiempo máximo: 24 horas).
2. **Investigación Operativa**: El supervisor de ruta entrevistará al mensajero encargado y revisará el GPS (Tiempo máximo: 3 días hábiles).
3. **Dictamen Legal y Financiero**: Se evaluará si el cliente pagó seguro y si el embalaje cumplía con las normas (Tiempo: 2 días).
4. **Reembolso**: Si procede, se depositará el monto correspondiente a la cuenta bancaria del cliente en un máximo de 15 días hábiles.

## 4. Canales de Contacto Oficial
- **Teléfono Nacional**: 01-800-LOGISTICA (01-800-564-4784)
- **Horario**: Lunes a Sábado, 8:00 AM a 8:00 PM.
- **Chatbot Web**: Disponible 24/7 en la página principal.
"""
with open(os.path.join(base_dir, "Atencion_Cliente", "proceso_reclamos.md"), "w", encoding="utf-8") as f:
    f.write(proceso_reclamos)

# 6. Políticas de Recursos Humanos (RRHH) - Markdown
politica_rrhh = """# Manual del Empleado - Recursos Humanos (Logística Global)
## 1. Vacaciones
Todos los empleados tienen derecho a días de vacaciones pagados de acuerdo a su antigüedad:
- **De 1 a 3 años de servicio**: 12 días hábiles de vacaciones al año.
- **De 4 a 5 años de servicio**: 15 días hábiles de vacaciones al año.
- **Más de 5 años**: 20 días hábiles de vacaciones al año.
Para solicitar vacaciones, el empleado debe notificar a su jefe directo con al menos 15 días de anticipación mediante el portal de HR (Workday).

## 2. Beneficios
- Seguro Médico de Gastos Mayores (Cobertura familiar para empleados con contrato indefinido).
- Bono de productividad mensual para el área de operaciones y conductores (basado en entregas exitosas).
- Descuento del 50% en envíos personales.

## 3. Horarios
- **Personal Administrativo**: Lunes a Viernes de 9:00 AM a 6:00 PM.
- **Personal Operativo (Mensajeros y Almacén)**: Turnos rotativos de 8 horas, 6 días a la semana con 1 día de descanso variable.
"""
with open(os.path.join(base_dir, "Recursos_Humanos", "politicas_empleados.md"), "w", encoding="utf-8") as f:
    f.write(politica_rrhh)

print("Documentos ampliados de Logística y RRHH generados exitosamente.")

