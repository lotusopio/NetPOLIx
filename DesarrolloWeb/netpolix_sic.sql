CREATE DATABASE IF NOT EXISTS netpolix_sic
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE netpolix_sic;

CREATE TABLE IF NOT EXISTS video (
    idvideo          INT          NOT NULL AUTO_INCREMENT,
    titulo           VARCHAR(255) NOT NULL,
    anio_produccion  INT,
    duracion         INT,                        -- duración en minutos
    descripcion      TEXT,
    fecha_creacion   DATETIME     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idvideo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS calificacion (
    idcalificacion  INT     NOT NULL AUTO_INCREMENT,
    idvideo         INT     NOT NULL,
    nivel           ENUM('Excelente','Buena','Regular','Mala') NOT NULL,
    puntaje         FLOAT,                       -- valor opcional 1.0 – 5.0
    comentario      TEXT,
    fecha_creacion  DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idcalificacion),
    CONSTRAINT fk_calificacion_video
        FOREIGN KEY (idvideo) REFERENCES video(idvideo)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS genero (
    idgenero        INT          NOT NULL AUTO_INCREMENT,
    nombre          VARCHAR(80)  NOT NULL UNIQUE,
    descripcion     TEXT,
    fecha_creacion  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idgenero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS director (
    iddirector      INT          NOT NULL AUTO_INCREMENT,
    nombre          VARCHAR(100) NOT NULL,
    apellido        VARCHAR(100) NOT NULL,
    nacionalidad    VARCHAR(60),
    fecha_nac       DATE,
    biografia       TEXT,
    fecha_creacion  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (iddirector)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS premio (
    idpremio        INT          NOT NULL AUTO_INCREMENT,
    nombre          VARCHAR(150) NOT NULL,
    tipo            ENUM('Oscar','Globo de Oro','BAFTA','Emmy','Otro') DEFAULT 'Otro',
    categoria       VARCHAR(100),                -- ej. "Mejor Película"
    anio            INT,
    descripcion     TEXT,
    fecha_creacion  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idpremio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS plataforma (
    idplataforma    INT          NOT NULL AUTO_INCREMENT,
    nombre          VARCHAR(100) NOT NULL UNIQUE,
    url             VARCHAR(255),
    descripcion     TEXT,
    fecha_creacion  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idplataforma)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS video_genero (
    idvideo   INT NOT NULL,
    idgenero  INT NOT NULL,
    PRIMARY KEY (idvideo, idgenero),
    CONSTRAINT fk_vg_video  FOREIGN KEY (idvideo)  REFERENCES video(idvideo)  ON DELETE CASCADE,
    CONSTRAINT fk_vg_genero FOREIGN KEY (idgenero) REFERENCES genero(idgenero) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS video_plataforma (
    idvideo       INT NOT NULL,
    idplataforma  INT NOT NULL,
    PRIMARY KEY (idvideo, idplataforma),
    CONSTRAINT fk_vp_video      FOREIGN KEY (idvideo)      REFERENCES video(idvideo)         ON DELETE CASCADE,
    CONSTRAINT fk_vp_plataforma FOREIGN KEY (idplataforma) REFERENCES plataforma(idplataforma) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS video_premio (
    idvideo   INT NOT NULL,
    idpremio  INT NOT NULL,
    PRIMARY KEY (idvideo, idpremio),
    CONSTRAINT fk_vpr_video  FOREIGN KEY (idvideo)  REFERENCES video(idvideo)  ON DELETE CASCADE,
    CONSTRAINT fk_vpr_premio FOREIGN KEY (idpremio) REFERENCES premio(idpremio) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS video_director (
    idvideo     INT NOT NULL,
    iddirector  INT NOT NULL,
    PRIMARY KEY (idvideo, iddirector),
    CONSTRAINT fk_vd_video    FOREIGN KEY (idvideo)    REFERENCES video(idvideo)       ON DELETE CASCADE,
    CONSTRAINT fk_vd_director FOREIGN KEY (iddirector) REFERENCES director(iddirector) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─────────────────────────────────────────────────────────────
--  DATOS DE EJEMPLO (opcional — descomenta si los necesitas)
-- ─────────────────────────────────────────────────────────────

-- INSERT INTO genero (nombre, descripcion) VALUES
--     ('Acción',   'Películas con escenas de acción y adrenalina'),
--     ('Drama',    'Narrativas centradas en conflictos emocionales'),
--     ('Comedia',  'Contenido humorístico y entretenido'),
--     ('Terror',   'Películas de miedo y suspenso'),
--     ('Ciencia Ficción', 'Historias basadas en ciencia y tecnología futura');

-- INSERT INTO plataforma (nombre, url) VALUES
--     ('Netflix',  'https://www.netflix.com'),
--     ('HBO Max',  'https://www.hbomax.com'),
--     ('Disney+',  'https://www.disneyplus.com');
