import psycopg2
import toml 
import warnings


class dbConn():

    def acces():
        global conn
        config = toml.load('config.toml')
        db_host = config['credentials']['host']
        db_name = config['credentials']['dbname']
        db_user = config['credentials']['dbuser']
        db_pass = config['credentials']['dbpass']
        conn = psycopg2.connect(host=db_host,dbname=db_name,user=db_user,password=db_pass)
        return conn


    ## Pemanggilan data menggunakan Query dari psycopg2
    def command_sql(query, conn):
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            if query.lower().startswith('select'):
                result = cursor.fetchall()
                return result
            conn.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            conn.rollback()  # Rollback the failed transaction


    ## Pengambilan data dari Database menggunakan Pandas
    def get_data(query,conn):

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            dataframe = pd.read_sql(test, conn)

            return dataframe

