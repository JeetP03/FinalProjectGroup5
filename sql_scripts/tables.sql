create database finalproject;

create table users (
	id int not null auto_increment,
    username varchar(20) not null,
    passwords varchar(20) not null,
    primary key(id)
);

CREATE TABLE posts (
	id int not null auto_increment,
    profile_username varchar(20) not null,
    written_text varchar(200) not null,
    media_location varchar(300) not null,
    primary key(id)
);