import sys
import traceback

import pymysql
from pymysql.cursors import DictCursor

from singleton_instance import SingletonInstance


class DatabaseManager(SingletonInstance):
    connection = None
    cursor = None
    DB_CREDENTIALS = "credentials"
    DB_WATCH_DATA = "watch_data"
    DB_USER_DATA = "userinfo"

    def create_connection(self, database):
        """ Create connection with database """
        try:
            print(f"Connecting to database : {database} ...", file=sys.stderr)
            self.connection = pymysql.connect(user="ubuntu", password='', database=database)
            print(f"Successfully connected to database : {database}", file=sys.stderr)
        except pymysql.Error:
            traceback.print_exc(file=sys.stderr)

    def get_cursor(self):
        """ Create cursor """
        self.cursor = self.connection.cursor(DictCursor)

    def close_connection(self, database):
        """ Close connection to database """
        if self.connection is not None:
            self.connection.close()
            print(f"Succesfully closed database : {database}", file=sys.stderr)

    def select_column_with_filter(self, filter_keyword, finding_column, selecting_column, table_name):
        """Fetch all records with 'filter_keyword' inside 'column_name' """
        query = f"""
        SELECT {selecting_column} 
        FROM {table_name} 
        WHERE {finding_column} LIKE '%{filter_keyword}%';
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def select_column_matches(self, match_keyword, finding_column, selecting_column, table_name):
        """Fetch all records which exactly matches 'match_keyword' inside 'column_name' """
        query = f"""
        SELECT {selecting_column} 
        FROM {table_name} 
        WHERE {finding_column} = '{match_keyword}';
        """
        print(f"select_column_matches query : {query}", file=sys.stderr)
        self.cursor.execute(query)
        print(self.cursor.fetchone(), file=sys.stderr)

    def select_last_element_of_column(self, table_name, column_name):
        """Fetch last record in 'column_name' """
        query = f"""
        SELECT {column_name} 
        FROM {table_name} 
        WHERE {column_name};
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()[-1]

    def insert_row(self, *values, database, table_name):
        """ Insert new row with some values into table_name at database.\n
        You should pass values in order with table columns. """
        column_name_list = self.get_column_names(database, table_name)
        for i, col in enumerate(column_name_list):
            if col == "id":
                column_name_list.pop(i)
        column_str = '('
        column_str += ", ".join(column_name_list)
        column_str += ')'

        value_str = "('"
        value_str += "', '".join(values)
        value_str += "')"

        query = f"""
        INSERT INTO {table_name} 
        {column_str}
        VALUES
        {value_str};
        """
        self.cursor.execute(query)
        print(f"Inserted values {value_str} into columns {column_str} at table {table_name}", file=sys.stderr)
        self.connection.commit()

    def get_column_names(self, database, table_name):
        column_name_list = []
        query = f"""
        SELECT `COLUMN_NAME`
        FROM `INFORMATION_SCHEMA`.`COLUMNS`
        WHERE `TABLE_SCHEMA` = '{database}'
            AND `TABLE_NAME` = '{table_name}';
        """
        self.cursor.execute(query)
        for col in reversed(self.cursor.fetchall()):
            column_name_list.append(col['COLUMN_NAME'])
        return column_name_list

    def insert_with_specific_field(self,*values,table_name,field_name):
        float_list = []
        column_str = '('
        column_name_list = field_name
        column_str += ", ".join(column_name_list)
        column_str += ')'
            
        if isinstance(values[0], float):
            for flo in values:
                float_list.append(str(flo))
        if len(values)!=0:
            for value in values:
                float_list.append(str(value))

        value_str = '("'
        value_str += '", "'.join(float_list)
        value_str += '")'

        query = f"""
        INSERT INTO {table_name} 
        {column_str}
        VALUES
        {value_str};
        """
        print(query)
        self.cursor.execute(query)
        self.connection.commit() 
    def get_login_info(self,login_id,pw,table_name):
        
        
#        login_id = '"'+login_id+'"'
#        pw = '"'+pw+'"'
        query=f"""
        SELECT id, name, phone, patient_locate_latitude, patient_locate_longitude,patient_range
        FROM {table_name}
        WHERE id="{login_id}" AND pw="{pw}";
        """
         
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if result:
            return result[-1]
        else:
            return "wrong"
