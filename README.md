🏔️ Peak Wishlist: Mountain & Summit Tracker
Peak Wishlist es una plataforma integral diseñada para montañistas, excursionistas y escaladores. Permite catalogar montañas, rutas y refugios, funcionando como un asistente de planificación de expediciones y una bitácora digital de cumbres alcanzadas.

🛠️ Tecnologías y Herramientas
Framework: Django 5.x (Python)

Estilos: Bootstrap 5.3 con personalización mediante CSS modular.

Librerías Especializadas:

    django-money: Gestión profesional de divisas y presupuestos.

    django-phonenumber-field: Validación de contactos internacionales.

Diseño: UI/UX optimizada con asistencia de IA para componentes visuales.

🧠 Arquitectura de Datos y Lógica de Negocio

El proyecto destaca por una estructura relacional robusta diseñada para escenarios geográficos reales:

* Geografía Transfronteriza: Las montañas utilizan una relación Many-to-Many con los Países (ej. El Everest se vincula a Nepal y China).

* Jerarquía de Actividades: Una Excursión (salida al terreno) está vinculada a una Ruta específica, la cual a su vez pertenece a una Montaña.

* Agrupación por Proyectos: Las excursiones pueden organizarse dentro de un Proyecto (Expedición de larga duración), permitiendo un seguimiento presupuestario y de objetivos.

* Entidades Complementarias: Gestión de Refugios (relación inversa con Montaña) y Áreas Protegidas/Parques con validación de permisos.

🚀 Guía de Pruebas (Orden Sugerido)
Para validar el flujo de integridad referencial de la aplicación, se sugiere seguir este orden en el Panel de Administración o en el Frontend:

* Países: Registrar los países base (ej. Argentina, Venezuela, España).

* Áreas Protegidas (Opcional): Crear un Parque Nacional vinculado a un país.

* Montañas: Registrar una cumbre vinculándola a uno o más países y un área protegida.

* Rutas: Definir una vía de ascenso para la montaña creada (ej. "Ruta Normal").

* Proyectos: Crear una expedición futura (ej. "Inca Trail 2026").

* Excursiones: Registrar la salida final vinculando la Ruta y el Proyecto.

📁 Estructura de Plantillas
La aplicación utiliza un sistema de Herencia de Plantillas de Django:

* base.html: Contiene la lógica global, navegación, Bootstrap CDN y estilos CSS base.

* templates/: Cada vista (Paises, Montañas, Proyectos, etc.) extiende del base, sobrescribiendo únicamente el bloque de contenido ({% block contenido %}).

🔐 Credenciales de Acceso (Superusuario)
Para acceder al panel de administración (/admin) y gestionar los modelos, utilice las siguientes credenciales:

Usuario: admin

Contraseña: CH_ijmm12345

Enlace: http://127.0.0.1:8000/admin