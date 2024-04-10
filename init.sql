CREATE DATABASE dataSAE;
use dataSAE;

CREATE TABLE datastorage (
  username VARCHAR(20),
  email VARCHAR(30),
  password VARCHAR(20)
);

INSERT INTO datastorage
  (username, email, password)
VALUES
  ('JohnDoe', 'johnDoetest@gmail.com','JohnDoe%123'),
  ('bob', 'bobleuser@univ-rouen.fr','aF5eX44sC');
