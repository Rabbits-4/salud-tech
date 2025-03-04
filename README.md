# Salud-Tech: Plataforma de Gestión de Salud

## Descripción
**Salud-Tech** es una plataforma basada en microservicios para la gestión de datos de salud. Implementa principios de **Domain-Driven Design (DDD)** y arquitectura basada en eventos para garantizar escalabilidad, modularidad e integración con diversos servicios.

## Características Principales
- **Arquitectura basada en eventos** para procesamiento de datos médicos.
- **Microservicios desacoplados** con comunicación mediante mensajería.
- **Integración con sistemas externos** mediante gRPC y REST API.
- **Estrategias de versionamiento** y persistencia optimizada.
- **Despliegue automatizado** mediante Docker y Docker Compose.
- **Framework de pruebas unitarias** para validación de servicios.

## Estructura del Proyecto
```
├── .github/                 # Configuración de GitHub Workflows y PR Templates
├── src/                     # Código fuente del proyecto
│   ├── notificaciones/      # Microservicio para gestión de notificaciones
│   ├── salud_tech/         # Core del sistema
│   │   ├── api/             # Endpoints y controladores
│   │   ├── config/          # Configuración del sistema
│   │   ├── modulos/         # Módulos de dominio
│   │   ├── seedwork/        # Componentes reutilizables (entidades, repositorios, etc.)
│   ├── sidecar/             # Adaptador para comunicación con AeroAlpes
│   ├── ui/                  # Interfaz de usuario
├── tests/                   # Pruebas unitarias
├── docker-compose.yml       # Configuración de servicios en contenedores
├── requirements.txt         # Dependencias del proyecto
├── Makefile                 # Comandos de automatización
└── README.md                # Documentación del proyecto
```

## Requisitos Previos
- **Python 3.10+**
- **Docker y Docker Compose**
- **Pip y Virtualenv**

## Instalación y Configuración
1. Clonar el repositorio:
   ```sh
   git clone https://github.com/tu_usuario/salud-tech.git
   cd salud-tech
   ```
2. Crear y activar un entorno virtual:
   ```sh
   python -m venv myenv
   source myenv/bin/activate  # En Windows: myenv\Scripts\activate
   ```
3. Instalar dependencias:
   ```sh
   pip install -r requirements.txt
   ```
4. Levantar los servicios con Docker:
   ```sh
   docker-compose up --build
   ```

## Uso
### Ejecutar Aplicaciones
#### API Principal
```sh
python src/salud_tech/api/procesamiento.py
```
La API estará disponible en `http://localhost:8000`

#### Microservicio Notificaciones
```sh
python src/notificaciones/main.py
```

#### UI Websocket Server
```sh
python src/ui/main.py
```

#### Sidecar/Adaptador
Ejecutar servidor:
```sh
python src/sidecar/main.py
```
Ejecutar cliente:
```sh
python src/sidecar/cliente.py
```
Compilar gRPC:
```sh
python -m grpc_tools.protoc -Iprotos --python_out=./pb2py --pyi_out=./pb2py --grpc_python_out=./pb2py protos/vuelos.proto
```

## Pruebas
Ejecutar pruebas unitarias:
```sh
coverage run -m pytest
```
Ver reporte de cobertura:
```sh
coverage report
```

## Despliegue con Docker
### Crear Imágenes Docker
```sh
docker build . -f salud_tech.Dockerfile -t salud-tech
```
Para el microservicio de notificaciones:
```sh
docker build . -f notificacion.Dockerfile -t salud-tech/notificacion
```
Para la UI:
```sh
docker build . -f ui.Dockerfile -t salud-tech/ui
```
Para el sidecar:
```sh
docker build . -f adaptador.Dockerfile -t salud-tech/adaptador
```

### Ejecutar Contenedores (sin Compose)
```sh
docker run -p 5000:5000 salud-tech
```
Para el microservicio de notificaciones:
```sh
docker run salud-tech/notificacion
```
Para la UI:
```sh
docker run salud-tech/ui
```
Para el sidecar:
```sh
docker run -p 50051:50051 salud-tech/adaptador
```

### Desplegar con Docker Compose
```sh
docker-compose up
```
Ejecutar en background:
```sh
docker-compose up -d
```
Detener contenedores:
```sh
docker-compose stop
```

### Comandos Útiles
Listar contenedores en ejecución:
```sh
docker ps
```
Listar todas las contenedoras:
```sh
docker ps -a
```
Parar contenedora:
```sh
docker stop <id_contenedora>
```
Eliminar contenedora:
```sh
docker rm <id_contenedora>
```
Listar imágenes:
```sh
docker images
```
Eliminar imágenes:
```sh
docker rmi <id_imagen>
```
Acceder a una contenedora:
```sh
docker exec -it <id_contenedora> sh
```
Liberar un puerto ocupado:
```sh
fuser -k <puerto>/tcp
```

### Ejecutar Docker-Compose con Perfiles
```sh
docker-compose --profile <pulsar|aeroalpes|ui|notificacion> up
```

## Contribuciones
1. Realizar un fork del repositorio.
2. Crear una nueva rama (`feature/nueva-funcionalidad`).
3. Enviar un **Pull Request** siguiendo el template de contribuciones.

## Licencia
MIT License. Ver el archivo `LICENSE` para más detalles.





---

# Tutorial 5 - CQRS y manejo de eventos

Repositorio con código base para el uso de un sistema usando el patrón CQRS y usando eventos de dominio e integración para la comunicación asíncrona entre componentes internos parte del mismo contexto acotado y sistemas externos.

Este repositorio está basado en el repositorio de sidecars visto en el tutorial 4 del curso. Por tal motivo, puede usar ese mismo repositorio para entender algunos detalles que este README no cubre.

## Estructura del proyecto

Este repositorio sigue en general la misma estructura del repositorio de origen. Sin embargo, hay un par de adiciones importante mencionar:

- El directorio **src** ahora cuenta con un nuevo directorio llamado **notificaciones**, el cual representa un servicio de mensajería que recibe eventos de integración propagados del sistema de AeroAlpes, por medio de un broker de eventos.
- El directorio **src** ahora también cuenta cuenta con un nuevo directorio llamado **ui**, el cual representa nuestra interfaz gráfica la cual puede recibir por medio de un BFF desarrollado en Python usando websockets, las respuestas de nuestros comandos de forma asíncrona.
- Nuestro proyecto de AeroAlpes ha cambiado de forma considerable. Los siguientes son los cambios relevantes en cada módulo:
    - **api**: En este módulo se modificó el API de `vuelos.py` el cual cuenta con dos nuevos endpoints: `/reserva-commando` y `/reserva-query`, los cuales por detrás de escenas usan un patrón CQRS como la base de su comunicación.
    - **modulos/../aplicacion**: Este módulo ahora considera los sub-módulos: `queries` y `comandos`. En dichos directorios pdrá ver como se desacopló las diferentes operaciones lectura y escritura. Vea en el módulo `vuelos` los archivos `obtener_reserva.py` y `crear_reserva.py` para ver como se logra dicho desacoplamiento.
    - **modulos/../aplicacion/handlers.py**: Estos son los handlers de aplicación que se encargan de oir y reaccionar a eventos. Si consulta el módulo de clientes podra ver que tenemos handlers para oir y reaccionar a los eventos de dominio para poder continuar con una transacción. En el modulo de vuelos encontramos handlers para eventos de integración los cuales pueden ser disparados desde la capa de infraestructura, la cual está consumiendo eventos y comandos del broker de eventos.
    - **modulos/../dominio/eventos.py**: Este archivo contiene todos los eventos de dominio que son disparados cuando una actividad de dominio es ejecutada de forma correcta.
    - **modulos/../infraestructura/consumidores.py**: Este archivo cuenta con toda la lógica en términos de infrastructura para consumir los eventos y comandos que provienen del broker de eventos. Desarrollado de una forma funcional.
    - **modulos/../infraestructura/despachadores.py**: Este archivo cuenta con toda la lógica en terminos de infrastructura para publicar los eventos y comandos de integración en el broker de eventos. Desarrollado de manera OOP.
    - **modulos/../infraestructura/schema**: En este directorio encontramos la definición de los eventos y comandos de integración. Puede ver que se usa un formato popular en la comunidad de desarrollo de software open source, en donde los directorios/módulos nos dan un indicio de las versiones `/schema/v1/...`. De esta manera podemos estar tranquilos con versiones incrementales y menores, pero listos cuando tengamos que hacer un cambio grande.
    - **seedwork/aplicacion/comandos.py**: Definición general de los comandos, handlers e interface del despachador.
    - **seedwork/infraestructura/queries.py**: Definición general de los queries, handlers e interface del despachador.
    - **seedwork/infraestructura/uow.py**: La Unidad de Trabajo (UoW) mantiene una lista de objetos afectados por una transacción de negocio y coordina los cambios de escritura. Este objeto nos va ser de gran importancia, pues cuando comenzamos a usar eventos de dominio e interactuar con otros módulos, debemos ser capaces de garantizar consistencia entre los diferentes objetos y partes de nuestro sistema.

## AeroAlpes
### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/aeroalpes/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/aeroalpes/api --debug run
```

### Ejecutar pruebas

```bash
coverage run -m pytest
```

### Ver reporte de covertura
```bash
coverage report
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f aeroalpes.Dockerfile -t aeroalpes/flask
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 5000:5000 aeroalpes/flask
```

## Sidecar/Adaptador
### Instalar librerías

En el mundo real es probable que ambos proyectos estén en repositorios separados, pero por motivos pedagógicos y de simpleza, 
estamos dejando ambos proyectos en un mismo repositorio. Sin embargo, usted puede encontrar un archivo `sidecar-requirements.txt`, 
el cual puede usar para instalar las dependencias de Python para el servidor y cliente gRPC.

```bash
pip install -r sidecar-requirements.txt
```

### Ejecutar Servidor

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/main.py 
```

### Ejecutar Cliente

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/cliente.py 
```

### Compilación gRPC

Desde el directorio `src/sidecar` ejecute el siguiente comando.

```bash
python -m grpc_tools.protoc -Iprotos --python_out=./pb2py --pyi_out=./pb2py --grpc_python_out=./pb2py protos/vuelos.proto
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f adaptador.Dockerfile -t aeroalpes/adaptador
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 50051:50051 aeroalpes/adaptador
```

## Microservicio Notificaciones
### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/notificaciones/main.py
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f notificacion.Dockerfile -t aeroalpes/notificacion
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run aeroalpes/notificacion
```

## UI Websocket Server
### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/ui/main.py
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f ui.Dockerfile -t aeroalpes/ui
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run aeroalpes/ui
```

## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`. Para ello, desde el directorio principal, ejecute el siguiente comando:

```bash
docker-compose up
```

Si desea detener el ambiente ejecute:

```bash
docker-compose stop
```

En caso de querer desplegar dicha topología en el background puede usar el parametro `-d`.

```bash
docker-compose up -d
```

## Comandos útiles

### Listar contenedoras en ejecución
```bash
docker ps
```

### Listar todas las contenedoras
```bash
docker ps -a
```

### Parar contenedora
```bash
docker stop <id_contenedora>
```

### Eliminar contenedora
```bash
docker rm <id_contenedora>
```

### Listar imágenes
```bash
docker images
```

### Eliminar imágenes
```bash
docker images rm <id_imagen>
```

### Acceder a una contendora
```bash
docker exec -it <id_contenedora> sh
```

### Kill proceso que esta usando un puerto
```bash
fuser -k <puerto>/tcp
```

### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|aeroalpes|ui|notificacion> up
```
