CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE public.store (
    id              uuid default  uuid_generate_v4()  primary key,
    number          varchar(250) not null,
    brand           varchar(250) not null,
    ownership_type  varchar(250) not null,
    store_name      varchar(250) not null,
    street          varchar(250) not null,
    city_ref        integer not null,
    city_name       varchar(250) not null,
    postcode        varchar(250),
    phone_number    varchar(250),
    store_coordinates       point
);

CREATE TABLE public.city (
    id              SERIAL primary key,
    name            varchar(250) not null,
    country         varchar(10) not null,
    state_province  varchar(10) not null,
    city_coordinates       geometry default null
);

ALTER TABLE store
    ADD CONSTRAINT stores_city_ref_fk
        FOREIGN KEY (city_ref) REFERENCES city
            ON DELETE SET NULL;