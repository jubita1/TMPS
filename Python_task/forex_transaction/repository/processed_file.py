
import sqlite3
from sqlite3 import Error as Err
from .tables import file, transactions
import traceback


class Forex_db:
    def __init__(self):
        try:
            self.conn_open = False
            self.conn_open = self.db_connection()
        except Err:
            print(Err)

    def create_tables(self):
        try:
            if self.conn_open:
                existing_table = self.existing_tables()
                for tables in existing_table:
                    if 'files' not in tables[0]:
                        self.conn.execute(file)
                    elif 'transactions' not in tables[0]:
                        self.conn.execute(transactions)
                    else:
                        print("tables are already created")
                else:
                    self.conn.execute(file)
                    self.conn.execute(transactions)
            else:
                self.db_connection()
                self.create_tables()
        except Exception as exc:
            print(exc)
            traceback.print_exc()

    def transaction_insert(self, data):
        #if table is not created
        self.create_tables()
        insert_query = f"""insert into transactions (source, destination, source_amount, destination_amount, destination_rate, file_id, created_datetime)
                            values """
        val = ''
        try:
            for row in data:
                if not val:
                    val += f"""('{row[1]}','{row[2]}','{row[3]}','{row[5]}', '{row[4]}',{row[6]}, '{row[7]}')"""
                else:
                    val += f""",('{row[1]}','{row[2]}','{row[3]}', '{row[5]}', '{row[4]}', {row[6]}, '{row[7]}')"""
            if val:
                insert_query = insert_query + val + ';'
                self.conn.execute(insert_query)
                #print(self.conn.execute("select * from transactions").fetchall())

        except Exception as exc:
            print(exc)

    def files_insert(self, data):
        # if table is not created
        self.create_tables()
        insert_query = ''
        try:
            insert_query += f""" insert into files (filename, foldername, created_datetime)  
                   values ('{data[0]}', '{data[1]}', '{data[2]}');
                    """
            if insert_query:
                self.conn.execute(insert_query)
                self.conn.commit()
                print(self.conn.execute(f"""select * from files""").fetchall())
            id = self.conn.execute(f"""select id from files where filename = '{data[0]}'""").fetchall()
            print(id)
            if id:
                return id[0][0]
        except Exception as exc:
            print(exc)

    def close_conn(self):
        self.conn.commit()
        self.conn.close()

    def db_connection(self):
        if not self.conn_open:
            self.conn = sqlite3.connect('processedfiles.db')
            print("Database connection is established successfully!")
            self.cursor_object = self.conn.cursor()
            print('DB Connection is active now')
        else:
            print('DB Connection is already active')
        return True

    def existing_tables(self):
        check_table = """SELECT name FROM sqlite_master WHERE type='table' """
        existing_table = self.conn.execute(check_table).fetchall()
        return existing_table

    def fetch_filedetails(self, directory):
        existing_table = self.existing_tables()
        processed_files_lst = set()
        query = f"""select filename from files where foldername = '{directory}'"""
        for tables in existing_table:
            if 'files' in tables[0]:
                res = self.conn.execute(query).fetchall()
                for data in res:
                    processed_files_lst.add(data[0])
        return processed_files_lst

    def fetch_filename(self, id):
        query = f"""select filename from files where id = {id}"""
        existing_table = self.existing_tables()
        for tables in existing_table:
            if 'transactions' in tables[0]:
                res = self.conn.execute(query).fetchall()
                if res:
                    return res[0][0]
