CREATE DATABASE IF NOT EXISTS local_db;
USE local_db;

CREATE TABLE IF NOT EXISTS recipes (
  id integer PRIMARY KEY AUTO_INCREMENT,
  -- name of recipe
  title varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  -- time required to cook/bake the recipe
  making_time varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  -- number of people the recipe will feed
  serves varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  -- food items necessary to prepare the recipe
  ingredients varchar(300) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  -- price of recipe
  cost integer NOT NULL,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime on update CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

