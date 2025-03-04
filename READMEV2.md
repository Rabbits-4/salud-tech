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

