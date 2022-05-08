DROP TABLE IF EXISTS rl_test;

CREATE TABLE rl_test (
    sub_id INTEGER PRIMARY KEY,
    fname VARCHAR(20),
    lname VARCHAR(20),
    test_name VARCHAR(20),
    variant VARCHAR(20),
    result INTEGER,
    test_done CHAR
);
