file = """CREATE TABLE IF NOT EXISTS files (
	id integer PRIMARY KEY AUTOINCREMENT,
	filename text NOT NULL UNIQUE,
	foldername text NOT NULL,
	created_datetime timestamp NOT NULL
);"""

transactions = """CREATE TABLE IF NOT EXISTS transactions (
                id integer PRIMARY KEY AUTOINCREMENT,
                source text NOT NULL,
                destination text NOT NULL,
                source_amount float(10,2) Not Null,
                destination_amount float(10,2) Not Null,
                destination_rate float(10,2) Not Null,
                file_id integer NOT NULL,
                created_datetime timestamp NOT NULL,
                FOREIGN KEY (file_id) REFERENCES files (id));"""
