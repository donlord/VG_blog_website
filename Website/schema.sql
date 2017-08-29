drop table if exists VideoGame;
drop table if exists Genre;
drop table if exists Platform;
drop table if exists Reviews;
drop table if exists VGRelease;
drop table if exists Users;
drop table if exists WishList;
drop table if exists StarRating;

create table VideoGame (
  VGid integer primary key not null,
  price float(2) not null,
  title varchar(80) not null,
  company varchar(80) not null,
  maxPlayer integer not null
 );
                      
create table Genre (
  VGid integer not null,
  Genre varchar(80) not null,
  primary key(VGid, Genre)
);
                      
create table Platform (
  VGid integer not null,
  Plat varchar(80) not null,
  primary key(VGid, Plat)
);
                      
create table Reviews (
  VGid integer not null,
  userid integer not null,
  Rating float(1) not null,
  Review text not null,
  primary key(VGid, userid, Review)
);


Create table VGRelease (
  VGid integer not null,
  releaseDay varchar(2) not null,
  releaseMonth varchar(2) not null,
  releaseYear varchar(4) not null,
  primary key(VGid, releaseYear)
);
                      
create table Users(
  userid integer primary key not null,
  name varchar(80) not null,
  username varchar(80) not null,
  password varchar(80) not null
);
                      
create table WishList (
  VGid integer not null,
  userid integer not null,
  primary key(VGid, userid)
);


create table StarRating(
  VGid integer not null,
  avgRate float(1) not null,
  primary key(VGid, avgRate)
);
