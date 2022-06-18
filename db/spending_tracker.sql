DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS merchants;


CREATE TABLE accounts(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255),
    balance INT
);

CREATE TABLE merchants(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    balance INT,
    description VARCHAR(255)
);

CREATE TABLE transactions(
    id SERIAL PRIMARY KEY,
    amount INT,
    date DATE,
    description VARCHAR(255),
    account_id INT REFERENCES accounts(id) ON DELETE CASCADE,
    merchant_id INT REFERENCES merchants(id) ON DELETE CASCADE
);

