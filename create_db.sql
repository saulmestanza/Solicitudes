CREATE DATABASE seguimiento_db CHARACTER SET UTF8;
CREATE USER seguimiento_user@localhost IDENTIFIED BY '2Tug69@j^v+RY69?8FhmfpddX?VwnVGb';
GRANT ALL PRIVILEGES ON seguimiento_db.* TO seguimiento_user@localhost;
FLUSH PRIVILEGES;