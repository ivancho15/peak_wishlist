🏔️ Peak Wishlist: Mountain & Summit Tracker
Peak Wishlist es una plataforma integral diseñada para la comunidad montañera. Funciona como un asistente de planificación de expediciones y una bitácora digital, permitiendo a los usuarios transformar sus sueños de cumbre en registros históricos detallados.

🧠 Lógica de Negocio y Permisos
El sistema está diseñado bajo una jerarquía de datos que garantiza la integridad de la información geográfica y técnica:

CRUDs de Usuario (Gestión Total): Actualmente, las entidades de Proyectos y Excursiones cuentan con un sistema CRUD (Create, Read, Update, Delete) completo para el usuario final. Esto se debe a que representan la actividad personal y privada del montañista (sus planes y sus logros).

Entidades Estructurales (Lectura y Sugerencia): Las Montañas, Rutas, Áreas Protegidas y Refugios funcionan como una "Wiki" base de datos compartida.

Estado actual: El usuario puede visualizar y consumir estos datos para crear sus planes.

Visión a futuro: Para evitar la duplicidad de datos y garantizar la precisión técnica (altitudes exactas, coordenadas, etc.), el registro de nuevas montañas o rutas por parte de usuarios pasará por un sistema de moderación. Los usuarios podrán "sugerir" contenido, pero este deberá ser verificado por un administrador antes de ser oficial en la plataforma.

🛠️ Tecnologías y Herramientas
Framework: Django 5.x (Python)

Frontend: Bootstrap 5.3 con personalización mediante CSS modular.

Autenticación: Sistema de usuarios con gestión de Avatares personalizados.

Interactividad: Implementación de HTMX para filtrado dinámico de dificultades técnicas sin recargar la página.

Librerías Especializadas:

django-money: Gestión profesional de divisas para presupuestos de expedición.

django-phonenumber-field: Validación de contactos internacionales para refugios.

🏗️ Arquitectura de Datos
El proyecto destaca por una estructura relacional robusta diseñada para escenarios geográficos reales:

Geografía Transfronteriza: Relación Many-to-Many entre Montañas y Países (ej. El Everest se vincula a Nepal y China).

Jerarquía de Actividades: Una Excursión (evento temporal) se vincula a una Ruta específica, la cual pertenece a una Montaña.

Agrupación por Proyectos: Permite agrupar múltiples excursiones bajo un mismo objetivo (ej. "Proyecto 7 Cumbres"), permitiendo seguimiento de estados (En progreso/Completado).

🚀 Guía de Pruebas (Flujo de Integridad)
Para validar el sistema, se recomienda el siguiente flujo de carga:

Países: Registrar los países base.

Áreas Protegidas: Crear un Parque Nacional vinculado a un país.

Montañas: Registrar una cumbre vinculándola a países y parques.

Rutas: Definir una vía de ascenso (Ruta Normal, Directa, etc.).

Proyectos: Crear una expedición futura (ej. "Aconcagua 2026").

Excursiones: Registrar la salida final vinculando la Ruta elegida y el Proyecto correspondiente.

🔮 Próximas Cumbres (Roadmap)
Peak Wishlist está en constante ascenso. Los siguientes hitos incluyen:

Comunidad Montañera: Evolución hacia una red social donde los usuarios puedan compartir sus relatos fotográficos y seguir el progreso de otros escaladores.

Arquitectura Avanzada: Migración a un Custom User Model para perfiles técnicos detallados.

Geolocalización: Integración con mapas interactivos para visualizar rutas y cumbres conquistadas de forma dinámica.

📁 Estructura de Plantillas
base.html: Esqueleto global con navegación dinámica según el estado de autenticación.

templates/: Organización modular donde cada vista extiende de la base, asegurando una UI consistente y ligera.