import sqlite3


def createTables():
    conn = sqlite3.connect('financisto.db')
    c = conn.cursor()
    c.executescript('''CREATE TABLE payee (
    _id integer primary key autoincrement,
    title text,
    last_category_id long not null default 0,
    updated_on TIMESTAMP DEFAULT 0);

    CREATE TABLE category (
    _id integer primary key autoincrement,
    title text not null,
    left integer not null default 0,
    right integer not null default 0,
    last_location_id not null default 0,
    last_project_id long not null default 0,
    sort_order integer not null default 0,
    type integer not null default 0,
    updated_on TIMESTAMP DEFAULT 0);

    CREATE INDEX category_left_idx ON category (left);
    INSERT INTO category(_id,title,left,right) VALUES(-1,-99000,-99000,'[Split...]');


    CREATE TABLE transactions (
    _id integer primary key autoincrement,
    from_account_id long not null,
    to_account_id long not null default 0,
    category_id long not null default 0,
    project_id long not null default 0,
    location_id long not null default 0,
    note text,
    from_amount integer not null default 0,
    to_amount integer not null default 0,
    datetime long not null,
    accuracy long not null default 0,
    latitude long not null default 0,
    longitude long not null default 0,
    is_template integer not null default 0,
    status text not null default 'UR',
    is_ccard_payment integer not null default 0,
    last_recurrence long not null default 0,
    payee_id long,
    parent_id long not null default 0,
    updated_on TIMESTAMP DEFAULT 0,
    original_currency_id long not null default 0,
    original_from_amount long not null default 0);

    CREATE INDEX transaction_from_act_idx ON transactions (from_account_id);
    CREATE INDEX transaction_to_act_idx ON transactions (to_account_id);
    CREATE INDEX transaction_dt_idx ON transactions (datetime desc);
    CREATE INDEX idx_is_template ON transactions(is_template);
    CREATE INDEX transaction_pid_idx ON transactions (parent_id);

    CREATE TABLE account (
    _id integer primary key autoincrement,
    title text not null,
    creation_date long not null,
    currency_id integer not null,
    total_amount integer not null default 0,
    type text not null default 'CASH',
    sort_order integer not null default 0,
    is_active boolean not null default 1,
    is_include_into_totals boolean not null default 1,
    last_category_id long not null default 0,
    last_account_id long not null default 0,
    total_limit integer not null default 0,
    closing_day integer not null default 0,
    payment_day integer not null default 0,
    last_transaction_date long not null default 0,
    updated_on TIMESTAMP DEFAULT 0);

    CREATE TABLE attributes (
    _id integer primary key autoincrement,
    type integer not null default 1,
    name text not null,
    list_values text,
    default_value text,
    updated_on TIMESTAMP DEFAULT 0);

    INSERT INTO attributes VALUES(-1,4,'DELETE_AFTER_EXPIRED',NULL,'true',0);

    CREATE TABLE category_attribute (
    category_id integer not null,
    attribute_id integer not null);

    CREATE INDEX category_attr_idx ON category_attribute (category_id);

    CREATE TABLE transaction_attribute (
    transaction_id integer not null,
    attribute_id integer not null,
    value text);

    CREATE INDEX transaction_attr_idx ON transaction_attribute (transaction_id);


    CREATE TABLE currency (
    _id integer primary key autoincrement,
    name text not null,
    title text not null,
    symbol text not null,
    is_default integer not null default 0,
    decimals integer not null default 2,
    decimal_separator text,
    group_separator text,
    symbol_format text not null default 'RS',
    updated_on TIMESTAMP DEFAULT 0);

    CREATE TABLE currency_exchange_rate (
    from_currency_id integer not null,
    to_currency_id integer not null,
    rate_date long not null,
    rate float not null,
    updated_on TIMESTAMP DEFAULT 0,
    PRIMARY KEY (from_currency_id, to_currency_id, rate_date));

    CREATE TABLE locations (
    _id integer primary key autoincrement,
    name text not null,
    datetime long not null,
    provider text,
    accuracy long not null default 0,
    latitude long not null default 0,
    longitude long not null default 0,
    is_payee integer not null default 0,
    count long not null default 0,
    updated_on TIMESTAMP DEFAULT 0,
    title text not null);

    CREATE TABLE project (
    _id integer primary key autoincrement,
    title text,
    is_active boolean not null default 1,
    updated_on TIMESTAMP DEFAULT 0);''')

    conn.commit()
    conn.close()
def writeQuery(rawdata, query):
    conn = sqlite3.connect('financisto.db')
    c = conn.cursor()
    c.execute(query, rawdata)
    conn.commit()
