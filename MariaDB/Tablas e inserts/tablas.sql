mysql -u root -p
CREATE DATABASE camiones;
CREATE USER 'mmarnun'@'localhost' IDENTIFIED BY 'mmarnun';
GRANT ALL PRIVILEGES ON *.* TO 'mmarnun'@'localhost';
IDENTIFIED BY 'mmarnun' WITH GRANT OPTION;
exit
mysql -u mmarnun -p
use camiones;

CREATE TABLE Ciudad (
	codigo varchar(5),
	nombre varchar(20),
	comunidadautonoma varchar(30),
	codigo_postal varchar(5) NOT NULL,
CONSTRAINT pk_ciudad PRIMARY KEY (codigo),
CONSTRAINT uc_cp UNIQUE (codigo_postal),
CONSTRAINT c_codigopciu CHECK (codigo_postal REGEXP '[0-9]{5}'),
CONSTRAINT c_codigociu CHECK (codigo REGEXP '[0-9]{5}'),
CONSTRAINT c_nombreciud CHECK (not (nombre collate latin1_general_cs) REGEXP '(^|[[:space:]])[[:lower:]]'),
CONSTRAINT c_comunidadautonoma CHECK (comunidadautonoma NOT IN ('Islas Baleares','Santa Cruz de Tenerife','Las Palmas','Ceuta','Melilla')),
CONSTRAINT c_comunidadautonoma_mays CHECK (not (comunidadautonoma collate latin1_general_cs) REGEXP '(^|[[:space:]])[[:lower:]]')
);

CREATE TABLE Parque (
	codigo varchar(5),
	calle varchar(50),
	num_calle varchar(3),
	capacidad INT(3),
	codigo_ciudad varchar(5),
    nombre varchar(20),
CONSTRAINT pk_parque PRIMARY KEY (codigo),
CONSTRAINT c_codigoparq CHECK (codigo REGEXP '[0-9]{5}'),
CONSTRAINT c_nombrecalle CHECK (not (calle collate latin1_general_cs) REGEXP '(^|[[:space:]])[[:lower:]]'),
CONSTRAINT c_num_calle CHECK (num_calle REGEXP '[0-9]{3}'),
CONSTRAINT fk_parque foreign key (codigo_ciudad) references Ciudad (codigo)
);

CREATE TABLE Remolque (
	matricula varchar(7),
	modelo varchar(10),
	peso DECIMAL(7,2) DEFAULT 10000.00,
	codigo_parque varchar(5),
CONSTRAINT pk_remolque PRIMARY KEY (matricula),
CONSTRAINT c_modelorem CHECK (BINARY modelo = UPPER (modelo)),
CONSTRAINT c_matricularem CHECK (matricula REGEXP '[0-9]{4}[A-Z]{3}'),
CONSTRAINT ck_matricularem CHECK(BINARY matricula = UPPER(matricula)),
CONSTRAINT fk_codigo_parque foreign key (codigo_parque) references Parque (codigo),
CONSTRAINT c_peso CHECK (peso>10000)
);

CREATE TABLE Remolque_Cisterna (
	matricula_remolque varchar(7),
	capacidad DECIMAL(7,2),
	tipo_mercancia varchar(12),
CONSTRAINT fk_remolque_cisterna foreign key (matricula_remolque) references Remolque (matricula),
CONSTRAINT ck_tipo_mercancia CHECK(BINARY tipo_mercancia = UPPER(tipo_mercancia)),
CONSTRAINT c_tipo_mercancia CHECK (tipo_mercancia IN ('PELIGROSO','NO PELIGROSO')),
CONSTRAINT c_capacidadremcis CHECK (capacidad BETWEEN 2000 AND 20000)
);

CREATE TABLE Remolque_Frigorifico (
	matricula_remolque varchar(7),
	capacidad DECIMAL(7,2),
	rango_temperatura DECIMAL(3,1),
CONSTRAINT fk_remolque_frigorifico foreign key (matricula_remolque) references Remolque (matricula),
CONSTRAINT c_capacidadremfrig CHECK (capacidad BETWEEN 2000 AND 20000),
CONSTRAINT c_temp CHECK (rango_temperatura BETWEEN -30 AND 10)
);

CREATE TABLE Remolque_Normal (
	matricula_remolque varchar(7),
	capacidad DECIMAL(7,2),
CONSTRAINT fk_remolque_normal foreign key (matricula_remolque) references Remolque (matricula),
CONSTRAINT c_capacidadremnorm CHECK (capacidad BETWEEN 2000 AND 20000)
);