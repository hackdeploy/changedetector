import pyodbc
import pandas as pd
import sqlalchemy
import urllib    
import os

CONNECTION_STRING = os.getenv('ws_connectionstring')

def Get_SQL_Engine():
    params = urllib.parse.quote_plus(os.getenv("bamodels_prod_connectionstring"))
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    return engine



def _deleteTimeSeriesOutput(ts_id):
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM [WS_MBOLANOS].[ts].[ChangeDetectorOutput] where ts_id='{0}'".format(ts_id))
    cursor.commit()
    conn.close()

def GetTimeSeriesIDs():
    query="""
        SELECT DISTINCT TS_ID
        FROM [BA_MODELS].[ts].[TimeSeries_Inputs]
    """
    
    engine = Get_SQL_Engine()
    df = pd.read_sql_query(query, engine)
    return df.TS_ID.values


def GetTimeSeries(tsid):
    query="""
            SELECT [ds]
            ,[y]
            ,[ts_id]
            ,[target]
            ,[ts_name]
            ,[ts_periodicity]
            FROM [BA_MODELS].[ts].[TimeSeries_Inputs]
            WHERE [ts_id]='{0}' AND Y IS NOT NULL
            --AND DATENAME(WEEKDAY,DS) NOT IN ('SATURDAY','SUNDAY')
            --AND TARGET='Doral'
            ORDER BY DS ASC
    """.format(tsid)
    
    engine = Get_SQL_Engine()
    df = pd.read_sql_query(query, engine)
    return df


def GetSQLEngine():
    cstring = os.getenv('ws_connectionstring')
    params = urllib.parse.quote_plus(cstring)
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    return engine

def SaveResults(df):
    df.to_sql(name="ChangeDetectorOutput", schema="ts", con=GetSQLEngine(),if_exists='append',chunksize=50, index=False,method="multi")