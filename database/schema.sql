--
-- File generated with SQLiteStudio v3.4.20 on mi�. ene. 21 23:23:46 2026
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: auditoria_activo
CREATE TABLE IF NOT EXISTS auditoria_activo (
    id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
    tabla        TEXT NOT NULL,
    id_registro  INTEGER NOT NULL,
    accion       TEXT NOT NULL,
    fecha        DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario   INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Table: devolucion_detalle
CREATE TABLE IF NOT EXISTS devolucion_detalle (
    id_detalle     INTEGER PRIMARY KEY AUTOINCREMENT,
    id_devolucion  INTEGER NOT NULL,
    id_producto    INTEGER NOT NULL,
    cantidad       REAL NOT NULL CHECK(cantidad >= 0),
    FOREIGN KEY (id_devolucion) REFERENCES devoluciones(id_devolucion),
    FOREIGN KEY (id_producto)   REFERENCES productos(id_producto)
);

-- Table: devoluciones
CREATE TABLE IF NOT EXISTS devoluciones (
    id_devolucion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venta      INTEGER NOT NULL,
    fecha         DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INTEGER NOT NULL,
    observacion   TEXT,
    FOREIGN KEY (id_venta)   REFERENCES ventas(id_venta),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

-- Table: entrada_detalle
CREATE TABLE IF NOT EXISTS entrada_detalle (
    id_detalle    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_entrada    INTEGER NOT NULL,
    id_producto   INTEGER NOT NULL,
    cantidad      REAL NOT NULL CHECK(cantidad >= 0),
    tipo_ingreso  TEXT,
    precio_compra REAL CHECK(precio_compra >= 0),
    FOREIGN KEY (id_entrada)  REFERENCES entradas(id_entrada),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Table: entradas
CREATE TABLE IF NOT EXISTS entradas (
    id_entrada   INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha        DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_proveedor INTEGER NOT NULL,
    id_usuario   INTEGER NOT NULL,
    observacion  TEXT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE RESTRICT,
    FOREIGN KEY (id_usuario)   REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

-- Table: movimientos_stock
CREATE TABLE IF NOT EXISTS movimientos_stock (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto   INTEGER NOT NULL,
    tipo          TEXT NOT NULL,
    cantidad      REAL NOT NULL,
    fecha         DATETIME DEFAULT CURRENT_TIMESTAMP,
    referencia    TEXT,
    id_usuario    INTEGER NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_usuario)  REFERENCES usuarios(id_usuario)
);

-- Table: productos
CREATE TABLE IF NOT EXISTS productos (
    id_producto     INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo            TEXT CHECK(LOWER(tipo) IN ('tuerca','perno')) NOT NULL,
    medida          TEXT NOT NULL,
    largo           TEXT,
    material        TEXT,
    precio_unidad   REAL CHECK(precio_unidad >= 0),
    precio_kilo     REAL CHECK(precio_kilo >= 0),
    stock           INTEGER DEFAULT 0 CHECK(stock >= 0),
    stock_minimo    INTEGER DEFAULT 0 CHECK(stock_minimo >= 0),
    activo          INTEGER DEFAULT 1 CHECK(activo IN (0,1)),
    fecha_creacion  DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_proveedor    INTEGER NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- Table: proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       TEXT NOT NULL,
    contacto     TEXT,
    activo       INTEGER DEFAULT 1 CHECK(activo IN (0,1))
);

-- Table: usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario     INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario        TEXT UNIQUE NOT NULL,
    password_hash  TEXT NOT NULL,
    rol            TEXT CHECK(rol IN ('admin','vendedor')) NOT NULL,
    activo         INTEGER DEFAULT 1 CHECK(activo IN (0,1)),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: venta_detalle
CREATE TABLE IF NOT EXISTS venta_detalle (
    id_detalle      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venta        INTEGER NOT NULL,
    id_producto     INTEGER NOT NULL,
    cantidad        REAL NOT NULL CHECK(cantidad >= 0),
    tipo_venta      TEXT,
    precio_unitario REAL NOT NULL CHECK(precio_unitario >= 0),
    subtotal        REAL NOT NULL,
    FOREIGN KEY (id_venta)    REFERENCES ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Table: ventas
CREATE TABLE IF NOT EXISTS ventas (
    id_venta   INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha      DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER NOT NULL,
    total      REAL NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

-- Index: idx_movimientos_producto_fecha
CREATE INDEX IF NOT EXISTS idx_movimientos_producto_fecha
ON movimientos_stock(id_producto, fecha);

-- Index: idx_productos_tipo_medida
CREATE INDEX IF NOT EXISTS idx_productos_tipo_medida
ON productos(tipo, medida);

-- Index: idx_usuarios_usuario
CREATE INDEX IF NOT EXISTS idx_usuarios_usuario
ON usuarios(usuario);

-- Index: idx_ventas_fecha
CREATE INDEX IF NOT EXISTS idx_ventas_fecha
ON ventas(fecha);

-- Trigger: trg_auditoria_productos_activo
CREATE TRIGGER IF NOT EXISTS trg_auditoria_productos_activo
AFTER UPDATE OF activo ON productos
FOR EACH ROW
WHEN OLD.activo <> NEW.activo
BEGIN
    INSERT INTO auditoria_activo (tabla, id_registro, accion, id_usuario)
    VALUES ('productos', NEW.id_producto,
            CASE WHEN NEW.activo=0 THEN 'desactivado' ELSE 'activado' END,
            NULL);
END;

-- Trigger: trg_auditoria_proveedores_activo
CREATE TRIGGER IF NOT EXISTS trg_auditoria_proveedores_activo
AFTER UPDATE OF activo ON proveedores
FOR EACH ROW
WHEN OLD.activo <> NEW.activo
BEGIN
    INSERT INTO auditoria_activo (tabla, id_registro, accion, id_usuario)
    VALUES ('proveedores', NEW.id_proveedor,
            CASE WHEN NEW.activo=0 THEN 'desactivado' ELSE 'activado' END,
            NULL);
END;

-- Trigger: trg_auditoria_usuarios_activo
CREATE TRIGGER IF NOT EXISTS trg_auditoria_usuarios_activo
AFTER UPDATE OF activo ON usuarios
FOR EACH ROW
WHEN OLD.activo <> NEW.activo
BEGIN
    INSERT INTO auditoria_activo (tabla, id_registro, accion, id_usuario)
    VALUES (
        'usuarios',
        NEW.id_usuario,
        CASE WHEN NEW.activo = 0 THEN 'desactivado' ELSE 'activado' END,
        NULL
    );
END;

-- -- Trigger: trg_devolucion_detalle_insert
-- CREATE TRIGGER IF NOT EXISTS trg_devolucion_detalle_insert
-- AFTER INSERT ON devolucion_detalle
-- FOR EACH ROW
-- BEGIN
--     UPDATE productos
--     SET stock = stock + NEW.cantidad
--     WHERE id_producto = NEW.id_producto;

--     INSERT INTO movimientos_stock (id_producto, tipo, cantidad, fecha, referencia, id_usuario)
--     VALUES (NEW.id_producto, 'devolucion', NEW.cantidad, CURRENT_TIMESTAMP,
--             'devolucion:' || NEW.id_devolucion,
--             (SELECT id_usuario FROM devoluciones WHERE id_devolucion = NEW.id_devolucion));
-- END;

-- -- Trigger: trg_entrada_detalle_insert
-- CREATE TRIGGER IF NOT EXISTS trg_entrada_detalle_insert
-- AFTER INSERT ON entrada_detalle
-- FOR EACH ROW
-- BEGIN
--     UPDATE productos
--     SET stock = stock + NEW.cantidad
--     WHERE id_producto = NEW.id_producto;

--     INSERT INTO movimientos_stock (id_producto, tipo, cantidad, fecha, referencia, id_usuario)
--     VALUES (NEW.id_producto, 'entrada', NEW.cantidad, CURRENT_TIMESTAMP,
--             'entrada:' || NEW.id_entrada,
--             (SELECT id_usuario FROM entradas WHERE id_entrada = NEW.id_entrada));
-- END;

-- Trigger: trg_no_delete_productos
CREATE TRIGGER IF NOT EXISTS trg_no_delete_productos
BEFORE DELETE ON productos
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'No se permite borrar productos, use activo=0');
END;

-- Trigger: trg_no_delete_proveedores
CREATE TRIGGER IF NOT EXISTS trg_no_delete_proveedores
BEFORE DELETE ON proveedores
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'No se permite borrar proveedores, use activo=0');
END;

-- Trigger: trg_no_delete_usuarios
CREATE TRIGGER IF NOT EXISTS trg_no_delete_usuarios
BEFORE DELETE ON usuarios
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'No se permite borrar usuarios, use activo=0');
END;

-- Trigger: trg_no_delete_ventas
CREATE TRIGGER IF NOT EXISTS trg_no_delete_ventas
BEFORE DELETE ON ventas
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'No se permite borrar ventas');
END;

-- Trigger: trg_no_stock_negativo
CREATE TRIGGER IF NOT EXISTS trg_no_stock_negativo
BEFORE UPDATE OF stock ON productos
FOR EACH ROW
WHEN NEW.stock < 0
BEGIN
    SELECT RAISE(ABORT, 'Stock no puede ser negativo');
END;

-- -- Trigger: trg_venta_detalle_insert
-- CREATE TRIGGER IF NOT EXISTS trg_venta_detalle_insert
-- AFTER INSERT ON venta_detalle
-- FOR EACH ROW
-- BEGIN
--     UPDATE productos
--     SET stock = stock - NEW.cantidad
--     WHERE id_producto = NEW.id_producto;

--     INSERT INTO movimientos_stock (id_producto, tipo, cantidad, fecha, referencia, id_usuario)
--     VALUES (NEW.id_producto, 'venta', NEW.cantidad, CURRENT_TIMESTAMP,
--             'venta:' || NEW.id_venta,
--             (SELECT id_usuario FROM ventas WHERE id_venta = NEW.id_venta));
-- END;

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
