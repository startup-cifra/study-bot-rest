create type roles as enum ('student','tutor');
create type lesson_types as enum ('lecture','practice','hybrid','conference','test','other');
create table if not exists users
(
    tg_id       integer
        constraint customer_pk
            primary key,
    username text unique,
    name text,
    surname text,
    course integer,
    faculty text
);
create table if not exists homework
(
    id serial
        constraint homework_pk
            primary key,
    owner_id integer references users(tg_id),
    chat_id integer references groups(chat_id),
    name text not null,
    deadline timestamp,
    url text
);
create table if not exists users_hw
(
    tg_id integer references users(tg_id),
    hw_id integer references homework(id) on delete cascade,
    mark integer,
  	unique(tg_id,hw_id)
);
create table if not exists groups
(
    chat_id integer
        constraint group_pk
            primary key,
    name text
);
create table if not exists users_groups
(
	tg_id integer references users(tg_id),
	chat_id integer references groups(chat_id),
    role roles,
	unique(tg_id,chat_id)
);
create table if not exists message
(
    id serial
        constraint message_pk
            primary key,
    tg_id integer references users(tg_id),
    chat_id integer references groups(chat_id),
    body text,
    date timestamp not null
);
create table if not exists lesson
(
    id serial
        constraint lesson_pk
            primary key,
    owner_id integer references users(tg_id),
    chat_id integer references groups(chat_id),
    attedance integer,
    lesson_type lesson_types,
    body text not null,
    data timestamp
);
create table if not exists users_lesson
(
    tg_id integer references users(tg_id),
    lesson_id integer references lesson(id) on delete cascade,
    unique(tg_id,lesson_id)
);
