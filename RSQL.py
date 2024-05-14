# Imports 
import mysql.connector
import pandas as pd
import math as m
import Creds

# connect to master schema
def connect_master():
    host,user,password = Creds.parse_SQL_creds('sql_creds.csv')
    _mydb = mysql.connector.connect(host=host,user=user,password=password)
    return _mydb

# connect to specific DB
def connect_DB(DB_NAME):
    print('-> Connecting to: '+DB_NAME)
    host,user,password = Creds.parse_SQL_creds('sql_creds.csv')

    return mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=DB_NAME 
    )

# create DB
def create_db(cursor,DB_NAME):
    cursor.execute("CREATE DATABASE " + DB_NAME)
    
# check to see if DB exists, if not create DB
def DB_check_create(cursor, name):
    new_db_flag = False
    try:
        create_db(cursor,name)
        print('-> '+name+ ' Created')
        new_db_flag = True
    except:
        print('-> '+name+' found')
    return new_db_flag

# verify and create db 
def generate_DB(cursor, DB_NAME):
    return DB_check_create(cursor, DB_NAME)

# check to see if table exists
def check_Table_exists(cursor,Table_name):
    
    cursor.execute("SHOW TABLES")
    lis = []
    check_flag = False
    for x in cursor:
        
        lis.append(x[0])
        
        if Table_name in lis:
            check_flag = True

    return check_flag

# cols = 'X VARCHAR(255), Y VARCHAR(255), Name VARCHAR(255), Color VARCHAR(255), Address VARCHAR(255)'
def generate_table(cursor, Table_NAME,SQL_cols):
    
    exists = check_Table_exists(cursor,Table_NAME)
    
    if exists == False:
        print('-> Creating Table: ', Table_NAME)
        try:
            print('-> '+Table_NAME,' Table created')
            
            cursor.execute("CREATE TABLE "+Table_NAME+" (id INT AUTO_INCREMENT PRIMARY KEY, "+SQL_cols+")")
        
        except:
            print('-> '+Table_NAME,': Error!')
    else:
        print('-> '+Table_NAME,' Table Found')
    
# Init Point Table
def Create_Points_Table(df, DB, cursor):
    
    exists =check_Table_exists(cursor, 'points') 


    cols = 'X VARCHAR(255), Y VARCHAR(255), Name VARCHAR(255), Color VARCHAR(255), Address VARCHAR(255)'

    generate_table(cursor, 'points',cols)
    
    if not exists:
        # insert data into table 
        points_list = []

        for index,row in df.iterrows():

            points_list.append([row['X'],row['Y'],row['Name'],row['Color'],row['Address']])

        sql = "INSERT INTO Points (X, Y, Name, Color, Address) VALUES (%s, %s, %s, %s, %s)"

        cursor.executemany(sql, points_list)
        
        DB.commit()
        print('-> ',cursor.rowcount, "was inserted.")
    else:
        print('-> No Data Appended')
        
# EOL Features
def generate_input_SQL(df):
    Insert_col_Names = ''
    Insert_col_plc = ''
    Create_cols = ''

    for col in df.columns:
        Create_cols = Create_cols +' '+ col+' VARCHAR(255),'
        Insert_col_plc = Insert_col_plc + '%s, '
        Insert_col_Names = Insert_col_Names + col + ', '
    Insert_col_plc = Insert_col_plc[0:-2]
    Create_cols = Create_cols[0:-1]
    Insert_col_Names = Insert_col_Names[0:-2]
    return Create_cols, Insert_col_Names, Insert_col_plc

# Init Point Table
def Create_DATA_Table(df, DB, cursor):
    
    exists =check_Table_exists(cursor, 'collected_data') 

    
    cols,insert_name,insert_plc = generate_input_SQL(df)
    
    #cols = 'X VARCHAR(255), Y VARCHAR(255), Name VARCHAR(255), Color VARCHAR(255), Address VARCHAR(255)'

    generate_table(cursor, 'collected_data',cols)
    
    if not exists:
        print('-> Data Table Found')
        # insert data into table 
        points_list = []
        print('-> appending data!')
        for index,row in df.iterrows():
            print('-> Progress: ' + str(m.ceil(index/df.shape[0]*100)) + '%',end = '\r')

            points_list.append(df.values.tolist()[index])

        sql = "INSERT INTO collected_data ("+insert_name+") VALUES ("+insert_plc+")"
    
        cursor.executemany(sql, points_list)
        
        DB.commit()
        print('-> ',cursor.rowcount, "was inserted.")
    else:
        print('-> No Data Appended')
        
# Query DB for XY locations based on address
def Query_XY(cursor, Address):
    Add_str = format(Address, '#x')
    sql = "SELECT * FROM points WHERE Address ="+ "'"+ Add_str + "'"

    cursor.execute(sql)

    lis = cursor.fetchall()
    
    return lis[0][1],lis[0][2]

# Query Heatmap DF
def get_heatmap_df(cursor,DataName):

    cursor.execute("SELECT points.X, points.Y, collected_data."+DataName+",collected_data.date FROM points INNER JOIN collected_data ON points.Address = collected_data.Address;")
    print('Fetching '+DataName)
    table_rows = cursor.fetchall()

    return pd.DataFrame(table_rows)

# Get Table Column names as list
def get_col_names(cursor,table_name):
    sql = 'SHOW COLUMNS FROM '+table_name+';'
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())
    return df[0].tolist() 

# Get SQL Table
def Get_Table(cursor,tablename):
    print('Fetching data from '+tablename)
    sql = "SELECT * FROM "+tablename+';'
    cursor.execute(sql)
    x = cursor.fetchall() 
    df = pd.DataFrame(x)
    col_names = get_col_names(cursor,tablename)
    df.columns = col_names
    return df

# full init Routine
def init_SQL_DB(db_name,points_df,data_df):
    
    print(' -- DB Initialisation --')
    print()
    # connect to master 
    mydb = connect_master()
    
    mycursor = mydb.cursor()

    print('-> Checking DB')
    # init db
    new_db = generate_DB(mycursor,db_name)

    # connect to the db 
    mydb = connect_DB(db_name)

    # reset cursor
    mycursor = mydb.cursor()

    # check/ create points table
    print('-> Init Points Table')
    Create_Points_Table(points_df,mydb,mycursor)

    # reset cursor
    mycursor = mydb.cursor()

    # check create data table
    print('-> Init Data Table')
    Create_DATA_Table(data_df,mydb,mycursor)   
    print()
    print(db_name+' Fully initialised!')
    print()
    return mydb
