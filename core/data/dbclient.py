"""
Class for sqlite database
"""
import sqlite3

DB_PATH = "reddit_nlp_db"
PRAGMA_INFO_FIELD_INDEX = 1
PRAGMA_INFO_DTYPE_INDEX = 2


class DBClient:
    """
    Class for managing sqlite db
    """

    def __init__(self, db_path=DB_PATH):
        """
        Connect to stored db if exists, otherwise create new
        :param db_path: path to read/write db
        """

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table_from_pandas(self, data_df, table_name, replace=True):
        """
        Creates table from pandas DataFrame
        :param data_df: data to insert
        :param table_name: sqlite table name
        :param replace: if table exists and true, rewrite, otherwise fail
        """

        try:
            data_df.to_sql(table_name, self.conn, if_exists='replace' if replace else 'fail')
        except sqlite3.InterfaceError as e:
            print(data_df.dtypes)
            raise e

    def get_table_info(self, table_name):
        """
        Returns table info
        :param table_name:
        :return: (list) field names and data types
        """

        pragma_statement = f"pragma table_info({table_name})"
        return [(x[PRAGMA_INFO_FIELD_INDEX], x[PRAGMA_INFO_DTYPE_INDEX])
                for x in self.cursor.execute(pragma_statement).fetchall()]
