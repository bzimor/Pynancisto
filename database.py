import sqlite3


# Writes data parsed from backup file to sqlite3 database
def writeQuery(rawdata, query):
    conn = sqlite3.connect('databases/financisto.db')
    c = conn.cursor()
    c.execute(query, rawdata)
    conn.commit()


# Get one item based on criteria
def getOne(query, options):
    conn = sqlite3.connect('databases/financisto.db')
    c = conn.cursor()
    # t = ('RHAT',)
    c.execute(query, options)
    return c.fetchone()


# Get all raw based on criteria
def getAll(query, options=None):
    conn = sqlite3.connect('databases/financisto.db')
    c = conn.cursor()
    # t = ('RHAT',)
    c.execute(query, options)
    return c.fetchall()


# Creates financisto database and all tables
def createTables():
    conn = sqlite3.connect('databases/financisto.db')
    c = conn.cursor()
    c.executescript('''

    CREATE TABLE payee (
    _id integer primary key autoincrement,
    title text,
    last_category_id long not null default 0,
    remote_key text,
    updated_on TIMESTAMP DEFAULT 0);

    CREATE TABLE if not exists category (
    _id integer primary key autoincrement,
    title text not null,
    left integer not null default 0,
    right integer not null default 0,
    last_location_id not null default 0,
    last_project_id long not null default 0,
    sort_order integer not null default 0,
    type integer not null default 0,
    remote_key text,
    updated_on TIMESTAMP DEFAULT 0);


    CREATE TABLE if not exists transactions (
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
    provider text,
    accuracy float,
    latitude double,
    longitude double ,
    payee text,
    is_template integer not null default 0,
    template_name text,
    recurrence text,
    notification_options text,
    status text not null default 'UR',
    attached_picture text,
    is_ccard_payment integer not null default 0,
    last_recurrence long not null default 0,
    payee_id long,
    parent_id long not null default 0,
    updated_on TIMESTAMP DEFAULT 0,
    remote_key text,
    original_currency_id long not null default 0,
    original_from_amount long not null default 0,
    blob_key text);


    CREATE TABLE if not exists account (
    _id integer primary key
    autoincrement, title text not null,
    creation_date long not null,
    currency_id integer not null,
    total_amount integer not null default 0 ,
    type text not null default 'CASH',
    issuer text, number text,
    sort_order integer not null default 0,
    is_active boolean not null default 1,
    is_include_into_totals boolean not null default 1,
    last_category_id long not null default 0,
    last_account_id long not null default 0,
    total_limit integer not null default 0,
    card_issuer text,
    closing_day integer not null default 0,
    payment_day integer not null default 0,
    note text,
    last_transaction_date long not null default 0,
    updated_on TIMESTAMP DEFAULT 0,
    remote_key text);


    CREATE TABLE if not exists attributes (
    _id integer primary key autoincrement,
    type integer not null default 1,
    title text not null,
    list_values text,
    default_value text,
    remote_key text,
    updated_on TIMESTAMP DEFAULT 0);


    CREATE TABLE if not exists category_attribute (
    category_id integer not null,
    attribute_id integer not null);


    CREATE TABLE if not exists transaction_attribute (
    transaction_id integer not null,
    attribute_id integer not null,
    value text);


    CREATE TABLE if not exists currency (
    _id integer primary key autoincrement,
    name text not null,
    title text not null,
    symbol text not null,
    is_default integer not null default 0,
    decimals integer not null default 2,
    decimal_separator text,
    group_separator text,
    symbol_format text not null default 'RS',
    remote_key text,
    updated_on TIMESTAMP DEFAULT 0);


    CREATE TABLE if not exists currency_exchange_rate (
    from_currency_id integer not null,
    to_currency_id integer not null,
    rate_date long not null,
    rate float not null,
    updated_on TIMESTAMP DEFAULT 0,
    PRIMARY KEY (from_currency_id, to_currency_id, rate_date));


    CREATE TABLE if not exists locations (
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
    remote_key text,
    title text not null);


    CREATE TABLE if not exists project (
    _id integer primary key autoincrement,
    title text,
    is_active boolean not null default 1,
    remote_key text,
    updated_on TIMESTAMP DEFAULT 0);


    CREATE TABLE if not exists split ( _id integer primary key autoincrement,
    transaction_id integer not null,
    category_id integer not null,
    amount integer not null,
    note text );


    CREATE TABLE if not exists running_balance ( account_id integer not null,
    transaction_id integer not null,
    datetime long not null,
    balance integer not null,
    PRIMARY KEY (account_id, transaction_id) );


    CREATE TABLE alterlog (
    script text not null,
    datetime long not null);


    CREATE TABLE if not exists sms_template (
    _id integer primary key autoincrement,
    title text not null,
    template text not null,
    category_id integer not null,
    updated_on TIMESTAMP DEFAULT 0,
    is_income BOOLEAN not null default 0,
    remote_key text,
    account_id integer);


    CREATE INDEX transaction_to_act_idx ON transactions (to_account_id);
    CREATE INDEX transaction_pid_idx ON transactions (parent_id);
    CREATE INDEX transaction_from_act_idx ON transactions (from_account_id);
    CREATE INDEX transaction_dt_idx ON transactions (datetime desc);
    CREATE INDEX transaction_attr_idx ON transaction_attribute (transaction_id);
    CREATE INDEX split_txn_idx ON split (transaction_id);
    CREATE INDEX split_cat_idx ON split (category_id);
    CREATE INDEX running_balance_txn_idx ON running_balance (transaction_id);
    CREATE INDEX running_balance_dt_idx ON running_balance (datetime);
    CREATE INDEX running_balance_act_idx ON running_balance (account_id);
    CREATE INDEX idx_key_pro ON project (remote_key);
    CREATE INDEX idx_key_payee ON payee (remote_key);
    CREATE INDEX idx_key_loc ON LOCATIONS (remote_key);
    CREATE INDEX idx_key_cur ON currency (remote_key);
    CREATE INDEX idx_key_cat ON category (remote_key);
    CREATE INDEX idx_key_act ON account (remote_key);
    CREATE INDEX idx_is_template ON transactions(is_template);
    CREATE INDEX category_left_idx ON category (left);
    CREATE INDEX category_attr_idx ON category_attribute (category_id);
    CREATE INDEX alterlog_script_idx on alterlog (script);

    CREATE VIEW v_transaction_attributes AS SELECT t._id as _id, a._id as attribute_id, a.type as attribute_type, a.name as attribute_name, a.list_values as attribute_list_values, a.default_value as attribute_default_value, ta.value as attribute_value FROM transactions t INNER JOIN transaction_attribute ta ON ta.transaction_id=t._id INNER JOIN attributes a ON a._id=ta.attribute_id ORDER BY a.name;
    CREATE VIEW v_report_sub_category AS select c._id as _id, c.left as left, c.right as right, c.title as name, t.datetime as datetime, t.from_account_currency_id as from_account_currency_id, t.from_amount as from_amount, t.to_account_currency_id as to_account_currency_id, t.to_amount as to_amount, t.original_currency_id as original_currency_id, t.original_from_amount as original_from_amount, t.is_transfer as is_transfer, t.from_account_id as from_account_id, t.to_account_id as to_account_id, t.category_id as category_id, t.category_left as category_left, t.category_right as category_right, t.project_id as project_id, t.location_id as location_id, t.payee_id as payee_id, t.status as status from v_category c inner join v_blotter_for_account_with_splits t on t.category_left between c.left and c.right where c._id > 0 and from_account_is_include_into_totals=1;
    CREATE VIEW v_report_project AS select p._id as _id, p.title as name, t.datetime as datetime, t.from_account_currency_id as from_account_currency_id, t.from_amount as from_amount, t.to_account_currency_id as to_account_currency_id, t.to_amount as to_amount, t.original_currency_id as original_currency_id, t.original_from_amount as original_from_amount, t.is_transfer as is_transfer, t.from_account_id as from_account_id, t.to_account_id as to_account_id, t.category_id as category_id, t.category_left as category_left, t.category_right as category_right, t.project_id as project_id, t.location_id as location_id, t.payee_id as payee_id, t.status as status from project p inner join v_blotter_for_account_with_splits t on t.project_id=p._id where p._id != 0 and from_account_is_include_into_totals=1;
    CREATE VIEW v_report_period AS select 0 as _id, null as name, t.datetime as datetime, t.from_account_currency_id as from_account_currency_id, t.from_amount as from_amount, t.to_account_currency_id as to_account_currency_id, t.to_amount as to_amount, t.is_transfer as is_transfer, t.original_currency_id as original_currency_id, t.original_from_amount as original_from_amount, t.from_account_id as from_account_id, t.to_account_id as to_account_id, t.category_id as category_id, t.category_left as category_left, t.category_right as category_right, t.project_id as project_id, t.location_id as location_id, t.payee_id as payee_id, t.status as status from v_blotter_for_account_with_splits t where t.category_id != -1 and from_account_is_include_into_totals=1;
    CREATE VIEW v_report_payee AS select p._id as _id, p.title as name, t.datetime as datetime, t.from_account_currency_id as from_account_currency_id, t.from_amount as from_amount, t.to_account_currency_id as to_account_currency_id, t.to_amount as to_amount, t.is_transfer as is_transfer, t.original_currency_id as original_currency_id, t.original_from_amount as original_from_amount, t.from_account_id as from_account_id, t.to_account_id as to_account_id, t.category_id as category_id, t.category_left as category_left, t.category_right as category_right, t.project_id as project_id, t.location_id as location_id, t.payee_id as payee_id, t.status as status from payee p inner join v_blotter_for_account t on t.payee_id=p._id where p._id != 0 and from_account_is_include_into_totals=1;
    CREATE VIEW v_report_location AS select l._id as _id, l.name as name, t.datetime as datetime, t.from_account_currency_id as from_account_currency_id, t.from_amount as from_amount, t.to_account_currency_id as to_account_currency_id, t.to_amount as to_amount, t.original_currency_id as original_currency_id, t.original_from_amount as original_from_amount, t.is_transfer as is_transfer, t.from_account_id as from_account_id, t.to_account_id as to_account_id, t.category_id as category_id, t.category_left as category_left, t.category_right as category_right, t.project_id as project_id, t.location_id as location_id, t.payee_id as payee_id, t.status as status from locations l inner join v_blotter_for_account t on t.location_id=l._id where l._id != 0 and from_account_is_include_into_totals=1;
    CREATE VIEW v_report_category AS select c._id as _id, c.parent_id as parent_id, c.title as name, t.datetime as datetime, t.from_account_currency_id as from_account_currency_id, t.from_amount as from_amount, t.to_account_currency_id as to_account_currency_id, t.to_amount as to_amount, t.original_currency_id as original_currency_id, t.original_from_amount as original_from_amount, t.is_transfer as is_transfer, t.from_account_id as from_account_id, t.to_account_id as to_account_id, t.category_id as category_id, t.category_left as category_left, t.category_right as category_right, t.project_id as project_id, t.location_id as location_id, t.payee_id as payee_id, t.status as status from v_category_list c inner join v_blotter_for_account_with_splits t on t.category_left between c.left and c.right where c._id > 0 and from_account_is_include_into_totals=1;
    CREATE VIEW v_category_list AS SELECT B._id AS parent_id, B.title AS parent_title, B.left AS parent_left, B.right AS parent_right, B.type AS parent_type, P._id as _id, P.title AS title, P.left as left, P.right as right, P.type as type FROM category AS B, category AS P WHERE P.left BETWEEN B.left AND B.right AND B._id = (SELECT MAX(S._id) FROM category AS S WHERE S.left < P.left AND S.right > P.right);
    CREATE VIEW v_category AS SELECT node._id as _id, node.title as title, node.left as left, node.right as right, node.type as type, node.last_location_id as last_location_id, node.last_project_id as last_project_id, node.sort_order as sort_order, count(parent._id)-1 as level FROM category as node, category as parent WHERE node.left BETWEEN parent.left AND parent.right GROUP BY node._id ORDER BY node.left;
    CREATE VIEW v_blotter_for_account_with_splits AS SELECT t._id as _id, t.parent_id as parent_id, a._id as from_account_id, a.title as from_account_title, a.is_include_into_totals as from_account_is_include_into_totals, c._id as from_account_currency_id, a2._id as to_account_id, a2.title as to_account_title, a2.currency_id as to_account_currency_id, cat._id as category_id, cat.title as category_title, cat.left as category_left, cat.right as category_right, cat.type as category_type, p._id as project_id, p.title as project, loc._id as location_id, loc.name as location, pp._id as payee_id, pp.title as payee, t.note as note, t.from_amount as from_amount, t.to_amount as to_amount, t.datetime as datetime, t.original_currency_id as original_currency_id, t.original_from_amount as original_from_amount, t.is_template as is_template, t.template_name as template_name, t.recurrence as recurrence, t.notification_options as notification_options, t.status as status, t.is_ccard_payment as is_ccard_payment, t.last_recurrence as last_recurrence, t.attached_picture as attached_picture, rb.balance as from_account_balance, 0 as to_account_balance, t.to_account_id as is_transfer FROM transactions as t INNER JOIN account as a ON a._id=t.from_account_id INNER JOIN currency as c ON c._id=a.currency_id INNER JOIN category as cat ON cat._id=t.category_id LEFT OUTER JOIN running_balance as rb ON rb.transaction_id=(CASE WHEN t.parent_id=0 THEN t._id ELSE t.parent_id END) AND rb.account_id=t.from_account_id LEFT OUTER JOIN account as a2 ON a2._id=t.to_account_id LEFT OUTER JOIN locations as loc ON loc._id=t.location_id LEFT OUTER JOIN project as p ON p._id=t.project_id LEFT OUTER JOIN payee as pp ON pp._id=t.payee_id WHERE is_template=0 UNION ALL SELECT t._id as _id, t.parent_id as parent_id, a._id as from_account_id, a.title as from_account_title, a.is_include_into_totals as from_account_is_include_into_totals, c._id as from_account_currency_id, a2._id as to_account_id, a2.title as to_account_title, a2.currency_id as to_account_currency_id, cat._id as category_id, cat.title as category_title, cat.left as category_left, cat.right as category_right, cat.type as category_type, p._id as project_id, p.title as project, loc._id as location_id, loc.name as location, pp._id as payee_id, pp.title as payee, t.note as note, t.to_amount as from_amount, t.from_amount as to_amount, t.datetime as datetime, t.original_currency_id as original_currency_id, t.original_from_amount as original_from_amount, t.is_template as is_template, t.template_name as template_name, t.recurrence as recurrence, t.notification_options as notification_options, t.status as status, t.is_ccard_payment as is_ccard_payment, t.last_recurrence as last_recurrence, t.attached_picture as attached_picture, rb.balance as from_account_balance, 0 as to_account_balance, -1 as is_transfer FROM transactions as t INNER JOIN account as a ON a._id=t.to_account_id INNER JOIN currency as c ON c._id=a.currency_id INNER JOIN category as cat ON cat._id=t.category_id LEFT OUTER JOIN running_balance as rb ON rb.transaction_id=t._id AND rb.account_id=t.to_account_id LEFT OUTER JOIN account as a2 ON a2._id=t.from_account_id LEFT OUTER JOIN locations as loc ON loc._id=t.location_id LEFT OUTER JOIN project as p ON p._id=t.project_id LEFT OUTER JOIN payee as pp ON pp._id=t.payee_id WHERE is_template=0;
    CREATE VIEW v_blotter_for_account AS SELECT * FROM v_blotter_for_account_with_splits WHERE is_template=0 AND parent_id=0;
    CREATE VIEW v_blotter AS SELECT * FROM v_all_transactions WHERE is_template = 0 AND parent_id=0;
    CREATE VIEW v_attributes AS SELECT a._id as _id, a.name as name, a.type as type, a.list_values as list_values, a.default_value as default_value, c._id as category_id, c.left as category_left, c.right as category_right, a.remote_key as remote_key FROM attributes as a, category_attribute as ca, category c WHERE ca.attribute_id=a._id AND ca.category_id=c._id;
    CREATE VIEW v_all_transactions AS SELECT t._id as _id, t.parent_id as parent_id, a1._id as from_account_id, a1.title as from_account_title, a1.is_include_into_totals as from_account_is_include_into_totals, c1._id as from_account_currency_id, a2._id as to_account_id, a2.title as to_account_title, c2._id as to_account_currency_id, cat._id as category_id, cat.title as category_title, cat.left as category_left, cat.right as category_right, cat.type as category_type, p._id as project_id, p.title as project, loc._id as location_id, loc.name as location, pp._id as payee_id, pp.title as payee, t.note as note, t.from_amount as from_amount, t.to_amount as to_amount, t.datetime as datetime, t.original_currency_id as original_currency_id, t.original_from_amount as original_from_amount, t.is_template as is_template, t.template_name as template_name, t.recurrence as recurrence, t.notification_options as notification_options, t.status as status, t.is_ccard_payment as is_ccard_payment, t.last_recurrence as last_recurrence, t.attached_picture as attached_picture, frb.balance as from_account_balance, trb.balance as to_account_balance, t.to_account_id as is_transfer FROM transactions as t INNER JOIN account as a1 ON a1._id=t.from_account_id INNER JOIN currency as c1 ON c1._id=a1.currency_id INNER JOIN category as cat ON cat._id=t.category_id LEFT OUTER JOIN running_balance as frb ON frb.transaction_id = t._id AND frb.account_id=t.from_account_id LEFT OUTER JOIN running_balance as trb ON trb.transaction_id = t._id AND trb.account_id=t.to_account_id LEFT OUTER JOIN account as a2 ON a2._id=t.to_account_id LEFT OUTER JOIN currency as c2 ON c2._id=a2.currency_id LEFT OUTER JOIN project as p ON p._id=t.project_id LEFT OUTER JOIN locations as loc ON loc._id=t.location_id LEFT OUTER JOIN payee as pp ON pp._id=t.payee_id;

    INSERT INTO category(_id,title,left,right) VALUES(-1,-99000,-99000,'[Split...]');
    INSERT INTO attributes VALUES(-1, 4, 'DELETE_AFTER_EXPIRED', NULL, 'true', '', 0);
    ''')

    conn.commit()
    conn.close()
