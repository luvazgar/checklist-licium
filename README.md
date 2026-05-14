# Proyecto Licium Modules

Colección de módulos desarrollados para Licium orientados a la gestión de tareas, moderación de contenido y eventos comunitarios.

El proyecto utiliza una arquitectura modular basada en:

- modelos SQLAlchemy
- servicios personalizados
- ACL
- vistas dinámicas
- configuración YAML
- internacionalización
- integración UI

Todos los módulos se cargan desde:

```text
backend/modules/
```

---

# Estructura general

Cada módulo sigue una estructura similar:

```text
module_name/
├── __init__.py
├── __manifest__.yaml
├── models/
├── services/
├── data/
├── views/
├── i18n/
└── tests/
```

---

# Practice Checklist

Módulo para gestionar listas de verificación e ítems asociados.

Permite:
- crear checklists
- asignar tareas
- marcar tareas como completadas
- cerrar y reabrir checklists
- controlar acceso mediante ACL

## Modelos

### PracticeChecklist
Representa una checklist principal.

Incluye:
- nombre
- descripción
- estado
- propietario
- visibilidad pública
- fecha de cierre

### PracticeChecklistItem
Representa tareas individuales dentro de una checklist.

Incluye:
- título
- nota
- usuario asignado
- estado completado
- fecha de finalización

Relación:
- una checklist contiene múltiples ítems

---

## Servicios

### PracticeChecklistService

Acciones:
- creación automática con propietario actual
- cierre de checklist
- reapertura de checklist

### PracticeChecklistItemService

Acciones:
- marcar ítems como completados o pendientes

---

## Seguridad

### Grupos
- reader
- manager

### ACL
- lectura pública de checklists cerradas
- permisos CRUD completos para managers

---

## Configuración adicional

Incluye:
- settings
- bulk actions
- internacionalización
- tests
- service overrides

---

# Feedback Moderation

Módulo para gestionar sugerencias y comentarios con flujo de moderación.

Permite:
- publicar sugerencias
- rechazar contenido
- fusionar sugerencias
- moderar comentarios
- clasificar mediante etiquetas

---

## Modelos

### Suggestion
Sugerencias enviadas por usuarios.

Incluye:
- título
- contenido
- estado
- datos del autor
- visibilidad
- notas de moderación

### Comment
Comentarios asociados a sugerencias.

### Tag
Etiquetas reutilizables.

Relación:
- muchas etiquetas por sugerencia

---

## Servicios

### SuggestionService

Acciones:
- publicar
- rechazar
- fusionar
- reabrir

### CommentService

Acciones:
- publicar comentarios
- rechazar comentarios

---

## Seguridad

### Grupos
- viewer
- moderator

### ACL
- creación pública de sugerencias y comentarios
- lectura pública únicamente de contenido publicado
- permisos completos para moderadores

---

# Community Events

Módulo para gestión de eventos y sesiones comunitarias.

Permite:
- crear eventos
- gestionar sesiones
- registrar asistentes
- controlar eventos públicos o privados

---

## Modelos

### Event
Representa eventos principales.

### Session
Sesiones asociadas a eventos.

### Registration
Inscripciones de usuarios a eventos.

Relación:
- un evento puede contener múltiples sesiones
- los usuarios pueden registrarse a eventos

---

## Seguridad

### Staff
Permisos completos sobre todos los modelos.

### Público
Lectura únicamente de eventos y sesiones publicadas.

### Usuarios internos
Acceso a sus propias inscripciones.

---

# UI Modules

Cada módulo registra un `ui.uimodule` para integrarse en el panel administrativo.

Ejemplo:

```yaml
- model: ui.uimodule
  ext_id: practice_checklist_ui_module
  fields:
    slug: practice-checklist
    name: Practice Checklist
    active: true
```

El campo `slug` es obligatorio.

---

# ACL

Las reglas ACL utilizan:

```yaml
group_id.ext_id:
```

Todos los grupos utilizados deben existir previamente.

---

# Instalación de módulos

Instalar un módulo:

```bash
python -m app.cli.module install modules/module_name -y
```

Actualizar un módulo:

```bash
python -m app.cli.module update modules/module_name -y
```

Ejemplos:

```bash
python -m app.cli.module install modules/practice_checklist -y
```

```bash
python -m app.cli.module install modules/feedback_moderation -y
```

```bash
python -m app.cli.module install modules/community_events -y
```