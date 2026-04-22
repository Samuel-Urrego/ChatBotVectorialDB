# 💬 Floating Chat Component - Blazor WebAssembly

¡Bienvenido a la interfaz oficial del **ChatBotVectorialDB**! Esta es una aplicación de chat flotante moderna, elegante y reactiva, diseñada específicamente para ser integrada en cualquier portal corporativo o aplicación web.

---

## ✨ Características Premium

- **Diseño Glassmorphic**: Interfaz moderna con efectos de transparencia y desenfoque (blur).
- **Animaciones Suaves**: Transiciones fluidas al abrir/cerrar y al recibir mensajes.
- **Modo Flotante**: Se ubica discretamente en la esquina inferior derecha, listo para asistir.
- **Totalmente Responsive**: Adaptable a dispositivos móviles y escritorios.
- **Integración Nativa**: Desarrollado con **Blazor WebAssembly (.NET 8)** para un rendimiento óptimo.

## 🛠️ Tecnologías Utilizadas

- **C# / .NET 8**
- **Blazor WebAssembly**
- **Vanilla CSS** (con diseño personalizado)
- **Bootstrap 5** (solo para rejilla y utilidades básicas)

---

## 🚀 Instalación y Uso

### 1. Requisitos Previos
- Tener instalado el **SDK de .NET 8**.
- El backend de FastAPI debe estar corriendo (por defecto en `http://localhost:8000`).

### 2. Ejecutar la Aplicación
Navega a la carpeta del proyecto y ejecuta:

```bash
dotnet watch run
```

### 3. Configuración de API
Asegúrate de que la URL del backend esté correctamente configurada en el archivo `FloatingChat.razor` (o en tu servicio de comunicación).

---

## 📸 Vista Previa del Componente

> [!TIP]
> El componente utiliza un sistema de burbujas interactivas. Al hacer clic en el botón flotante 🗨️, se despliega la ventana de conversación.

### Estructura de Archivos
```text
frontend/
├── ChatFlotante.sln         # Solución de Visual Studio
└── ChatFlotante/            # Proyecto principal
    ├── Components/          # Componentes Razor
    │   └── Layout/          # FloatingChat.razor (Componente core)
    └── wwwroot/             # Estilos y activos estáticos
```

---

## 🎨 Personalización

Puedes modificar los colores y el estilo general editando los archivos CSS en `wwwroot/app.css` y los estilos específicos del componente en `MainLayout.razor.css`.

¡Disfruta de una experiencia de chat de siguiente nivel! 🚀
