# Plan de Entrega 4 - Salud-Tech

## 1. Introducción
Este documento describe la organización y justificación de la Entrega 4 del proyecto **Salud-Tech**, en cumplimiento con los requisitos establecidos en la guía de entrega.

## 2. Alcance de la Entrega
La Entrega 4 se centrará en la implementación de los servicios esenciales de **Salud-Tech**, asegurando que:
- Se utilicen **comandos y eventos** para la comunicación entre servicios.
- Se implemente **Apache Pulsar** como broker de eventos.
- Se desarrolle al menos **un microservicio en Python** con Flask y SQLAlchemy.
- Se maneje **versionamiento de esquemas** para los eventos.
- Se implementen **bases de datos en al menos 3 de los 4 servicios**.
- Se justifique la **topología de administración de datos** utilizada (descentralizada o híbrida).

## 3. Microservicios Implementados
Se han desarrollado los siguientes microservicios en **Salud-Tech**:

### **1. Procesamiento de Datos Médicos**
- **Tópico comando:** `procesar_datos_medicos`
- **Tópico eventos:** `datos_procesados`, `error_procesamiento`
- **Base de datos:** PostgreSQL con modelo CRUD.
- **Formato de eventos:** Avro + Schema Registry de Apache Pulsar.
- **Justificación:** Este microservicio gestiona la transformación y almacenamiento de datos médicos.

### **2. Notificaciones**
- **Tópico comando:** `enviar_notificacion`
- **Tópico eventos:** `notificacion_enviada`, `notificacion_fallida`
- **Base de datos:** NoSQL (MongoDB) con modelo CRUD.
- **Formato de eventos:** JSON.
- **Justificación:** Responsable de notificar a los usuarios sobre el estado de sus datos y eventos del sistema.

### **3. Integración con Sistemas Externos (Sidecar)**
- **Tópico comando:** `sincronizar_datos_externos`
- **Tópico eventos:** `datos_sincronizados`, `error_sincronizacion`
- **Base de datos:** NoSQL (Cassandra) para alta disponibilidad.
- **Formato de eventos:** JSON con versionamiento manual.
- **Justificación:** Responsable de la integración con fuentes de datos externas y sincronización de información.

### **4. UI WebSocket Server**
- **Tópico comando:** `actualizar_interfaz`
- **Tópico eventos:** `interfaz_actualizada`, `error_interfaz`
- **Base de datos:** No aplica, ya que es un servicio orientado a la visualización en tiempo real.
- **Formato de eventos:** JSON.
- **Justificación:** Proporciona una interfaz de usuario en tiempo real con notificaciones y actualizaciones en vivo.

## 4. Comunicación Asíncrona con Apache Pulsar
Se utilizará **Apache Pulsar** como broker de eventos para garantizar la independencia y escalabilidad de los microservicios.

## 5. Administración de Datos
Se ha optado por **una arquitectura híbrida**:
- **Procesamiento de Datos y Notificaciones** compartirán la misma base de datos relacional (PostgreSQL) con esquemas separados.
- **Integración con Sistemas Externos y UI WebSocket** operarán con bases de datos NoSQL para escalabilidad y tolerancia a fallos.

## 6. Despliegue y Repositorio
- **Repositorio público:** Se proporcionará un link a GitHub sin credenciales sensibles.
- **README detallado:** Explicaciones sobre estructura, despliegue y pruebas.
- **Video de presentación:** Archivo de máximo 45 minutos mostrando la arquitectura, servicios y pruebas.

## 7. Atributos de Calidad Evaluados
Se medirán los siguientes escenarios:
1. **Escalabilidad:** Se incrementará la carga en el servicio de procesamiento de datos y se analizará el tiempo de respuesta.
2. **Resiliencia:** Se degradará un nodo de Apache Pulsar para verificar que los servicios sigan operando.
3. **Integridad de Datos:** Se simulará una falla en la integración con sistemas externos para validar la consistencia en la sincronización de datos.

## 8. Conclusión
Esta entrega se enfocará en establecer una infraestructura de comunicación basada en eventos y microservicios, asegurando alineación con los principios de **DDD** y criterios de calidad definidos en el enunciado.

