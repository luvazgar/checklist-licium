# Practice Checklist

En esta práctica he creado el módulo **Practice Checklist**, cuyo objetivo es gestionar listas de verificación (checklists) y sus elementos asociados (items) dentro del backend modular del proyecto. Para ello he seguido la estructura estándar que utiliza el sistema para descubrir módulos en tiempo de ejecución.

El backend carga automáticamente cualquier módulo que se encuentre dentro de `backend/modules`, por lo que la primera parte del trabajo ha consistido en crear la estructura mínima del módulo.

## Estructura del módulo

La estructura que he utilizado es la siguiente:

```bash
backend/modules/practice_checklist/
  __init__.py
  __manifest__.yaml
  models/
    __init__.py
    checklist.py
  services/
    __init__.py
    checklist.py
  data/
    groups.yml
    acl_rules.yml
    ui_modules.yml
  views/
    views.yml
    menu.yml
```

En este entorno concreto, normalmente la carpeta `backend/modules/*` suele contener enlaces simbólicos (`symlinks`) hacia `/opt/modules/*`, pero para esta práctica he creado directamente el módulo dentro de `backend/modules`.

---

## Creación del manifest del módulo

Lo primero que he hecho ha sido crear el archivo `__manifest__.yaml`, ya que este archivo define la configuración principal del módulo: su nombre, su identificador técnico, su versión, sus dependencias y los archivos que el sistema debe cargar al instalarlo o inicializarlo.

La ruta del archivo es:

```bash
backend/modules/practice_checklist/__manifest__.yaml
```

y su contenido es el siguiente:

```yaml
name: Practice Checklist
technical_name: practice_checklist
version: 0.1
depends:
  - ui
data:
  - data/groups.yml
  - data/acl_rules.yml
  - data/ui_modules.yml
  - views/views.yml
  - views/menu.yml
migrations: {}
post_init_hook: null
```

En este archivo he definido:

- `name`: nombre visible del módulo
- `technical_name`: nombre técnico del módulo
- `version`: versión inicial
- `depends`: dependencias necesarias para que funcione
- `data`: archivos que se cargarán automáticamente
- `migrations`: espacio reservado para futuras migraciones
- `post_init_hook`: hook opcional tras la inicialización

---

## Creación de los imports del módulo

Después de crear el manifest, he preparado los archivos `__init__.py` necesarios para que el sistema pueda importar correctamente los modelos y servicios del módulo.

### Archivo principal del módulo

Primero he creado el archivo principal del módulo, que sirve para cargar automáticamente sus submódulos al inicializarse.

La ruta del archivo es:

```bash
backend/modules/practice_checklist/__init__.py
```

y su contenido es:

```python
from . import models  # noqa: F401
from . import services  # noqa: F401
```

Con esto hago que al cargar el módulo también se carguen automáticamente sus modelos y sus servicios.

---

### Archivo `models/__init__.py`

Después he creado el archivo de inicialización de la carpeta `models`, que sirve para exponer los modelos definidos dentro del módulo.

La ruta del archivo es:

```bash
backend/modules/practice_checklist/models/__init__.py
```

y su contenido es:

```python
from .checklist import PracticeChecklist, PracticeChecklistItem  # noqa: F401
```

Con este import estoy registrando los dos modelos principales del módulo: la checklist principal y los items asociados a cada checklist.

---

### Archivo `services/__init__.py`

También he creado el archivo de inicialización de la carpeta `services`, que se utilizará para cargar los servicios asociados a los modelos.

La ruta del archivo es:

```bash
backend/modules/practice_checklist/services/__init__.py
```

y su contenido es:

```python
from .checklist import PracticeChecklistService, PracticeChecklistItemService  # noqa: F401
```

Con esto dejo preparado el módulo para poder trabajar más adelante con la lógica de negocio asociada a ambos modelos.

---

## Definición del modelo de datos

Antes de escribir el código de los modelos, he pensado primero qué entidades necesitaba representar y cómo se relacionaban entre sí. En este caso, el módulo se basa en dos conceptos principales:

- una **checklist**, que representa la lista general
- un **item**, que representa cada tarea o elemento individual dentro de esa checklist

Por tanto, he definido dos modelos:

- `PracticeChecklist`
- `PracticeChecklistItem`

La relación entre ellos es de **uno a muchos**: una checklist puede tener varios items, pero cada item pertenece únicamente a una checklist.

---

## Creación del archivo `models/checklist.py`

Para implementar estos modelos, he creado el archivo:

```bash
backend/modules/practice_checklist/models/checklist.py
```

con el siguiente contenido:

```python
from __future__ import annotations

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import backref, relationship
from app.core.base import Base
from app.core.fields import field


class PracticeChecklist(Base):
    __tablename__ = "practice_checklist"
    __abstract__ = False
    __model__ = "checklist"
    __service__ = "modules.practice_checklist.services.checklist.PracticeChecklistService"

    __selector_config__ = {
        "label_field": "name",
        "search_fields": ["name", "status", "description"],
        "columns": [
            {"field": "id", "label": "ID"},
            {"field": "name", "label": "Checklist"},
            {"field": "status", "label": "Estado"},
            {"field": "is_public", "label": "Público"},
        ],
    }

    name = field(
        String(180),
        required=True,
        public=True,
        editable=True,
        info={"label": {"es": "Checklist", "en": "Checklist"}},
    )
    description = field(
        Text,
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Descripción", "en": "Description"}},
    )
    status = field(
        String(20),
        required=True,
        public=True,
        editable=True,
        default="draft",
        info={
            "label": {"es": "Estado", "en": "Status"},
            "choices": [
                {"label": "Draft", "value": "draft"},
                {"label": "Open", "value": "open"},
                {"label": "Closed", "value": "closed"},
            ],
        },
    )
    is_public = field(
        Boolean,
        required=True,
        public=True,
        editable=True,
        default=False,
        info={"label": {"es": "Público", "en": "Public"}},
    )
    owner_id = field(
        Integer,
        ForeignKey("core_user.id"),
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Responsable", "en": "Owner"}},
    )
    owner = relationship(
        "User",
        foreign_keys=lambda: [PracticeChecklist.owner_id],
        info={"public": True, "recursive": False, "editable": True},
    )
    closed_at = field(
        DateTime(timezone=True),
        required=False,
        public=True,
        editable=False,
        info={"label": {"es": "Cerrado en", "en": "Closed at"}},
    )


class PracticeChecklistItem(Base):
    __tablename__ = "practice_checklist_item"
    __abstract__ = False
    __model__ = "checklist_item"
    __service__ = "modules.practice_checklist.services.checklist.PracticeChecklistItemService"

    __selector_config__ = {
        "label_field": "title",
        "search_fields": ["title", "note"],
        "columns": [
            {"field": "id", "label": "ID"},
            {"field": "checklist", "label": "Checklist"},
            {"field": "title", "label": "Ítem"},
            {"field": "is_done", "label": "Hecho"},
        ],
    }

    checklist_id = field(
        Integer,
        ForeignKey("practice_checklist.id", ondelete="CASCADE"),
        required=True,
        public=True,
        editable=True,
        info={"label": {"es": "Checklist", "en": "Checklist"}},
    )
    checklist = relationship(
        "modules.practice_checklist.models.checklist.PracticeChecklist",
        foreign_keys=lambda: [PracticeChecklistItem.checklist_id],
        backref=backref("items", cascade="all, delete-orphan"),
        info={"public": True, "recursive": False, "editable": True},
    )
    title = field(
        String(180),
        required=True,
        public=True,
        editable=True,
        info={"label": {"es": "Ítem", "en": "Item"}},
    )
    note = field(
        Text,
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Nota", "en": "Note"}},
    )
    assigned_user_id = field(
        Integer,
        ForeignKey("core_user.id"),
        required=False,
        public=True,
        editable=True,
        info={"label": {"es": "Asignado a", "en": "Assigned to"}},
    )
    assigned_user = relationship(
        "User",
        foreign_keys=lambda: [PracticeChecklistItem.assigned_user_id],
        info={"public": True, "recursive": False, "editable": True},
    )
    is_done = field(
        Boolean,
        required=True,
        public=True,
        editable=True,
        default=False,
        info={"label": {"es": "Hecho", "en": "Done"}},
    )
    done_at = field(
        DateTime(timezone=True),
        required=False,
        public=True,
        editable=False,
        info={"label": {"es": "Hecho en", "en": "Done at"}},
    )
```

---

## Explicación del modelo `PracticeChecklist`

El primer modelo que he definido es `PracticeChecklist`, que representa la checklist principal.

La clase hereda de `Base`, lo que significa que pasa a ser un modelo persistente del sistema y que se almacenará en la base de datos.

### Configuración básica del modelo

Dentro del modelo he definido:

```python
__tablename__ = "practice_checklist"
```

Esto indica el nombre de la tabla real en la base de datos.

También he añadido:

```python
__abstract__ = False
```

para indicar que no se trata de un modelo abstracto, sino de una tabla real.

Además, he configurado:

```python
__model__ = "checklist"
```

como nombre lógico del modelo dentro del sistema, y:

```python
__service__ = "modules.practice_checklist.services.checklist.PracticeChecklistService"
```

para asociarlo con su servicio correspondiente.

### Configuración del selector

También he definido `__selector_config__`, que sirve para indicar cómo se mostrará este modelo en selectores o tablas dentro de la interfaz.

```python
__selector_config__ = {
    "label_field": "name",
    "search_fields": ["name", "status", "description"],
    "columns": [
        {"field": "id", "label": "ID"},
        {"field": "name", "label": "Checklist"},
        {"field": "status", "label": "Estado"},
        {"field": "is_public", "label": "Público"},
    ],
}
```

Con esta configuración he indicado que:

- el campo principal será `name`
- se podrá buscar por `name`, `status` y `description`
- en las tablas se mostrarán el ID, el nombre, el estado y si la checklist es pública

### Campos del modelo `PracticeChecklist`

#### Campo `name`

He definido el campo `name` de esta forma:

```python
name = field(
    String(180),
    required=True,
    public=True,
    editable=True,
    info={"label": {"es": "Checklist", "en": "Checklist"}},
)
```

Este campo representa el nombre principal de la checklist. Es obligatorio, visible públicamente y editable.

#### Campo `description`

También he añadido una descripción opcional:

```python
description = field(
    Text,
    required=False,
    public=True,
    editable=True,
    info={"label": {"es": "Descripción", "en": "Description"}},
)
```

Este campo permite guardar información adicional sobre la checklist.

#### Campo `status`

Después he añadido el estado de la checklist:

```python
status = field(
    String(20),
    required=True,
    public=True,
    editable=True,
    default="draft",
    info={
        "label": {"es": "Estado", "en": "Status"},
        "choices": [
            {"label": "Draft", "value": "draft"},
            {"label": "Open", "value": "open"},
            {"label": "Closed", "value": "closed"},
        ],
    },
)
```

Este campo representa el estado en el que se encuentra la checklist. He definido tres valores posibles:

- `draft`
- `open`
- `closed`

Además, he establecido como valor por defecto `draft`.

#### Campo `is_public`

También he añadido un campo booleano para indicar si la checklist es pública:

```python
is_public = field(
    Boolean,
    required=True,
    public=True,
    editable=True,
    default=False,
    info={"label": {"es": "Público", "en": "Public"}},
)
```

Por defecto, la checklist se crea como no pública.

#### Campo `owner_id`

A continuación he añadido el campo `owner_id`:

```python
owner_id = field(
    Integer,
    ForeignKey("core_user.id"),
    required=False,
    public=True,
    editable=True,
    info={"label": {"es": "Responsable", "en": "Owner"}},
)
```

Este campo guarda la referencia al usuario responsable de la checklist. Está conectado mediante una clave foránea a la tabla de usuarios del sistema.

#### Relación `owner`

Además del identificador, he definido la relación completa con el usuario:

```python
owner = relationship(
    "User",
    foreign_keys=lambda: [PracticeChecklist.owner_id],
    info={"public": True, "recursive": False, "editable": True},
)
```

Gracias a esta relación, no solo puedo guardar el ID del usuario, sino también acceder directamente al objeto `User` asociado.

#### Campo `closed_at`

Por último, he añadido el campo:

```python
closed_at = field(
    DateTime(timezone=True),
    required=False,
    public=True,
    editable=False,
    info={"label": {"es": "Cerrado en", "en": "Closed at"}},
)
```

Este campo sirve para almacenar la fecha y hora en la que la checklist se cierra. No es editable manualmente, lo que indica que normalmente se gestionará desde la lógica del sistema.

---

## Explicación del modelo `PracticeChecklistItem`

El segundo modelo que he definido es `PracticeChecklistItem`, que representa cada tarea o elemento individual dentro de una checklist.

Igual que en el caso anterior, este modelo también hereda de `Base`, por lo que también se almacenará como tabla real en la base de datos.

### Configuración básica del modelo

He definido:

```python
__tablename__ = "practice_checklist_item"
```

como nombre de la tabla, y:

```python
__model__ = "checklist_item"
```

como nombre lógico del modelo.

Además, he asociado este modelo con su servicio correspondiente:

```python
__service__ = "modules.practice_checklist.services.checklist.PracticeChecklistItemService"
```

### Configuración del selector

También he configurado `__selector_config__`:

```python
__selector_config__ = {
    "label_field": "title",
    "search_fields": ["title", "note"],
    "columns": [
        {"field": "id", "label": "ID"},
        {"field": "checklist", "label": "Checklist"},
        {"field": "title", "label": "Ítem"},
        {"field": "is_done", "label": "Hecho"},
    ],
}
```

Con esto he definido que el campo principal del item será `title`, que se podrá buscar por `title` y `note`, y que en las tablas se mostrarán el ID, la checklist asociada, el título y si está completado.

### Campos del modelo `PracticeChecklistItem`

#### Campo `checklist_id`

El primer campo importante es:

```python
checklist_id = field(
    Integer,
    ForeignKey("practice_checklist.id", ondelete="CASCADE"),
    required=True,
    public=True,
    editable=True,
    info={"label": {"es": "Checklist", "en": "Checklist"}},
)
```

Este campo guarda la referencia a la checklist a la que pertenece el item. He usado una clave foránea hacia `practice_checklist.id` y además he añadido `ondelete="CASCADE"` para que, si se elimina una checklist, también se eliminen automáticamente todos sus items.

#### Relación `checklist`

Además, he definido la relación completa con el modelo `PracticeChecklist`:

```python
checklist = relationship(
    "modules.practice_checklist.models.checklist.PracticeChecklist",
    foreign_keys=lambda: [PracticeChecklistItem.checklist_id],
    backref=backref("items", cascade="all, delete-orphan"),
    info={"public": True, "recursive": False, "editable": True},
)
```

Esta relación permite acceder desde un item a su checklist correspondiente. También he añadido un `backref("items")`, lo que significa que desde una checklist puedo acceder directamente a todos sus items asociados mediante `checklist.items`.

Además, el parámetro:

```python
cascade="all, delete-orphan"
```

garantiza que si un item queda huérfano o si se elimina su checklist, también será eliminado automáticamente.

#### Campo `title`

Después he añadido el título del item:

```python
title = field(
    String(180),
    required=True,
    public=True,
    editable=True,
    info={"label": {"es": "Ítem", "en": "Item"}},
)
```

Este campo representa el nombre o título principal de la tarea.

#### Campo `note`

También he añadido una nota opcional:

```python
note = field(
    Text,
    required=False,
    public=True,
    editable=True,
    info={"label": {"es": "Nota", "en": "Note"}},
)
```

Este campo sirve para guardar información adicional sobre el item.

#### Campo `assigned_user_id`

A continuación he añadido el usuario asignado al item:

```python
assigned_user_id = field(
    Integer,
    ForeignKey("core_user.id"),
    required=False,
    public=True,
    editable=True,
    info={"label": {"es": "Asignado a", "en": "Assigned to"}},
)
```

Este campo almacena el identificador del usuario responsable de realizar ese item concreto.

#### Relación `assigned_user`

Además, he definido la relación con el usuario asignado:

```python
assigned_user = relationship(
    "User",
    foreign_keys=lambda: [PracticeChecklistItem.assigned_user_id],
    info={"public": True, "recursive": False, "editable": True},
)
```

Con esto puedo acceder directamente al objeto `User` correspondiente al usuario asignado.

#### Campo `is_done`

También he añadido un campo booleano para indicar si el item está completado:

```python
is_done = field(
    Boolean,
    required=True,
    public=True,
    editable=True,
    default=False,
    info={"label": {"es": "Hecho", "en": "Done"}},
)
```

Por defecto, cada item se crea como no completado.

#### Campo `done_at`

Finalmente, he añadido:

```python
done_at = field(
    DateTime(timezone=True),
    required=False,
    public=True,
    editable=False,
    info={"label": {"es": "Hecho en", "en": "Done at"}},
)
```

Este campo sirve para guardar la fecha y hora en la que el item se marca como completado. Igual que ocurría con `closed_at`, no es editable manualmente.

---

## Relación entre ambos modelos

La parte más importante de esta práctica ha sido definir correctamente la relación entre ambos modelos.

He planteado que:

- una checklist puede contener varios items
- cada item pertenece únicamente a una checklist

Esto se ha implementado mediante:

```python
ForeignKey("practice_checklist.id", ondelete="CASCADE")
```

y también mediante:

```python
backref=backref("items", cascade="all, delete-orphan")
```

Gracias a esta configuración:

- desde un item puedo acceder a su checklist
- desde una checklist puedo acceder a todos sus items
- si elimino una checklist, también se eliminan automáticamente todos sus items

De esta manera, la estructura de datos queda correctamente normalizada y preparada para seguir desarrollando el resto del módulo.

---