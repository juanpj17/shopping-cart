# 🛒 Shopping Cart API

Este repositorio contiene el código y la configuración para el backend de una aplicación de comercio electrónico. Desarrollado con 🐍 Python y 🚀 FastAPI, este proyecto está diseñado para gestionar 🛍️ productos, 👤 usuarios, 🛒 carritos de compras, 📦 órdenes y generar 📊 reportes básicos.

## Características Principales

- **Gestión de usuarios:** Roles de 👑 superadministrador, 👔 gerente y 🧑‍💻 cliente.
- **Catálogo de productos:** 🔍 Búsqueda, ✏️ creación, 🔧 edición y ❌ eliminación de productos.
- **Carrito de compras:** ➕ Agregar y 🔄 gestionar productos en el carrito.
- **Procesamiento de órdenes:** 🆕 Creación, 🔄 actualización y ❌ cancelación de órdenes.
- **Reportes básicos:** 💵 Ventas totales, 📈 ganancias y 🔥 productos más vendidos.

## Tecnologías Utilizadas

- **Lenguaje:** 🐍 Python 3.13
- **Framework:** 🚀 FastAPI 0.115.4
- **Base de Datos:** 🐘 PostgreSQL
- **ORM:** 🔗 SQLModel
- **Herramientas adicionales:** 🐳 Docker, 🧪 pytest, 🎨 Alembic

## Guía de Instalación

### Requisitos Previos

- 🐳 Docker instalado en tu sistema.
- Una cuenta de DockerHub.

### Instalación y Ejecución con Docker

1. **Obtén los archivos necesarios:**

   Para ejecutar la aplicación con la imagen de Docker, solamente necesitas descargar el archivo docker-compose.yml que se encuentra en este repositorio. 

2. **Ingresa desde la terminal cmd:**

   Ubícate en la ruta donde se encuentra el archivo de docker-compose.

3. **Obtén la imagen desde DockerHub:**

   ```bash
   docker pull nadinechancay/shopping-cart:latest
   ```

4. **Ejecuta el contenedor:**

   ```bash
   docker run -d -p 8000:8000 --name shopping-cart nadinechancay/shopping-cart:latest
   ```

5. **Accede a la API:**

   La aplicación estará disponible en [http://localhost:8000](http://localhost:8000).

## Documentación de la API

La documentación interactiva de la API se encuentra disponible en:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

