create database apple_store;
use apple_store;

create table apple_data(
product_id integer primary key,
product_category text not null, 
product_name text not null, 
price integer not null,
stock_quantity integer not null);

create table discounts(
product_id integer primary key,
discount_perc integer not null);
