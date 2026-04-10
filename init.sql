create table cam
(
cam_id serial primary key,
uuid text not null UNIQUE
);

create table images
(
image_id serial primary key,
image_time timestamp default current_timestamp,
image_data BYTEA not null,
cam_id int not null
constraint key_users foreign key(cam_id) references cam(cam_id)
);