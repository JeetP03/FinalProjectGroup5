create database finalproject;

create table users (
	id int not null auto_increment,
    username varchar(20) not null,
    passwords varchar(20) not null,
    primary key(id)
);