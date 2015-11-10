import sqlalchemy as sql
import os

class App:
    def __init__(self, db_connection_string):
        if db_connection_string != None:
            self.engine = sql.create_engine(db_connection_string)
            self.metadata = sql.MetaData()
        
    def get_ddl(self, table_name):
        return "n0ne"
        return sql.schema.CreateTable(sql.Table(table_name, self.metadata, autoload=True, autoload_with=self.engine ), bind=self.engine)
        
    def get_table_objects(self):
        return "none"
        insp = sql.inspect(self.engine)
        return insp.get_table_names()
        
    @staticmethod
    def get_tns_names():
        try:
            names_file = open(os.environ.get("TNS_ADMIN") + "\\tnsnames.ora", 'r')
            
            names_list = []
            
            for line in names_file:
                names_list.append(line[0:line.find("=") - 1]) if line[0].isalpha() else 0
            return names_list
        except:
            return None
