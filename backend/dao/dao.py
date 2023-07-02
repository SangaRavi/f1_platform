from attrs import define
import pandas as pd
import psycopg2
import functools
import json
import psycopg2.extras as extras


@define
class AbstractDBDao:
    conn: psycopg2.extensions.connection

    def query(self, query: str, params: dict, use_cache: bool = False) -> pd.DataFrame:
        return pd.read_sql_query(query, con=self.conn, params=params)

    # def query(self, query: str, params: dict, use_cache: bool = False) -> pd.DataFrame:
    #     psconnection = self.conn.cursor()
    #     try:
    #         kwargs = dict(conn=psconnection, query=query)
    #         if not use_cache:
    #             return _query(params=params, **kwargs)
    #         else:
    #             df, dtypes = _cached_query(params=json.dumps(params), **kwargs)
    #             return pd.read_json(df, precise_float=True).astype(dtypes)
    #     finally:
    #         self.conn.commit()


@functools.lru_cache(16)
def _cached_query(params: str, **kwargs):
    df = _query(params=json.loads(params), **kwargs)
    return df.to_json(date_format="iso", date_unit="ns"), df.dtypes


@functools.lru_cache(16)
def _query(query: str, params: dict, conn) -> pd.DataFrame:
    df = pd.read_sql_query(query, con=conn, params=params if params else {})
    return df


class TemporalContextAggregation(AbstractDBDao):
    def fetch_data(self, query: str, params: dict) -> pd.DataFrame:
        return self.query(query, params)

    def write_data(self, data, table):
        tuples = [tuple(x) for x in data.to_numpy()]

        cols = ','.join(list(data.columns))
        # SQL query to execute
        query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
        cursor = self.conn.cursor()
        try:
            extras.execute_values(cursor, query, tuples)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            cursor.close()
            return 1
        print("the dataframe is inserted")
        cursor.close()


class TemporalContextAggregationImpl(TemporalContextAggregation, AbstractDBDao):
    def fetch_data_from_table(self, params, table):
        print(params)
        query = f"select * from {table} where year=%(year)s and gp=%(country)s and event=%(mode)s"
        return self.query(query, params)