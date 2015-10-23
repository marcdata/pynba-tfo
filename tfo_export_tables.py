

# Module for exporting pandas tables to two formats: 
# 1) Excel tables
# 2) SQL tables 

# -----------------------------------------------------------------------------

import os.path

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import pickle

from scipy.stats.stats import pearsonr   
from scipy.stats.stats import spearmanr   


# -----------------------------------------------------------------------------
    
# -----------------------------------------------------------------------------

# read in pickle file data from prev
outfilename = 'shots_allteams.pik'
bigdf = pickle.load(open(outfilename, 'rb'))

fn_team_table = 'team_report_table.pik'
fn_player_table = 'player_report_table.pik'

team_report = pd.read_pickle(fn_team_table)
player_report = pd.read_pickle(fn_player_table)

team_report = team_report.sort_index()

out_folder = 'tables_out'

# -----------------------------------------------------------------------------

# Write out two dataframes to excel tables
# Note: requies openpyxl 
#
#team_report.to_excel(out_folder + '/' + 'team_table.xlsx', sheet_name='Sheet1')
#
#player_report.to_excel(out_folder + '/' + 'player_table.xlsx', sheet_name='Sheet1')


# -----------------------------------------------------------------------------

# xlsxwriter stuff

# From here and below // code to export pandas table to Excel
# and add pretty formatting. 

# Requires module xlsxwriter. Object created in Pandas call, but xlsxwriter option needs separate package install.
   
def export_team_table_excel():
    """ Exports an excel table of performance stats, team level.
    Adds some formatting and other notes describing the data and columns."""
             
    writer = pd.ExcelWriter('tables_out' + '/' + 'team_report_out.xlsx', engine='xlsxwriter')
    
    team_report.to_excel(writer, index=True, sheet_name='report', startrow=3,
        header=['TFO eFG%', 'Baseline eFG%', 'eFG diff', '3pt % TFO', '3pt % Baseline', '3pt diff', '3pt # shots TFO',
        'Proportion 3s TFO', 'Prop 3s Baseline', 'Prop diff', 'Shotrate baseline', 'Shotrate diff' ])
    
    # Prep for formatting 
    workbook = writer.book
    worksheet = writer.sheets['report']
    
    # Do some formatting.   Display percentages as percent. 
    # Columns B-G and I-M
    
    percent_fmt = workbook.add_format({'num_format': '0.0%'})
    decimal_fmt = workbook.add_format({'num_format': '0.00'})
    # Add a bold format to use to highlight cells.
    bold_fmt = workbook.add_format({'bold': 1})
    
    # Format percent columns
    col_width = 12
    worksheet.set_column('B:G', col_width, percent_fmt)
    worksheet.set_column('C:C', col_width+4, percent_fmt)
    worksheet.set_column('H:H', 14)
    worksheet.set_column('I:J', col_width+4, percent_fmt)
    worksheet.set_column('L:L', col_width+4, decimal_fmt)
    worksheet.set_column('M:M', col_width, percent_fmt)
    
    # Update wide columns
    worksheet.set_column('C:C', col_width+4, percent_fmt)
    worksheet.set_column('F:F', col_width+4, percent_fmt)
    
    # Update notation in sheet
    worksheet.write('B1', 'TFO = Two-for-One window', bold_fmt)
    worksheet.write('B3', 'Overall Shooting', bold_fmt)
    worksheet.write('E3', '3 pt Shooting', bold_fmt)
    worksheet.write('I3', '2s vs 3s (shot selection)', bold_fmt)
    worksheet.write('L3', 'Shot rate (shot volume)', bold_fmt)
    
    worksheet.write('A4', 'Team', bold_fmt)
    
    
    # Finalize output in workbook
    
    writer.save()
    
# End team table export to excel


# --------------------------------

# Export function for excel table, individual level.  

def export_player_table_excel():
    """ Exports an excel table of performance stats, individual level.
    Adds some formatting and other notes describing the data and columns."""
        
    fn_out = "player_report_out.xlsx"
    writer = pd.ExcelWriter('tables_out' + '/' + fn_out, engine='xlsxwriter')
    
    player_report.to_excel(writer, index=True, sheet_name='report', startrow=3,
        header=['# shots TFO', 'eFG diff', 'TFO eFG%', 'Baseline eFG%', 
        'Proportion 3s diff','Proportion 3s TFO', 'Prop 3s Baseline',  
        'Shotrate baseline', 'Shotrate diff', 
        '3pt # shots TFO', '3pt diff', '3pt % TFO', '3pt % Baseline'  ])
        
    # Prep for formatting 
    workbook = writer.book
    worksheet = writer.sheets['report']
    
    # Do some formatting.   Display percentages as percent. 
    
    percent_fmt = workbook.add_format({'num_format': '0.0%'})
    decimal_fmt = workbook.add_format({'num_format': '0.00'})
    # Add a bold format to use to highlight cells.
    bold_fmt = workbook.add_format({'bold': 1})
    
    # Format percent columns
    
    # Percent columns: C, D, E,  //  L, M, N
    # Decimal columns: F, G, H, I, J
    # Regular int number B, K
    
    col_width = 12
    worksheet.set_column('C:E', col_width+1, percent_fmt)
    worksheet.set_column('F:H', col_width+4, decimal_fmt)   
    worksheet.set_column('L:L', 14, percent_fmt)
    worksheet.set_column('M:N', col_width+4, percent_fmt)
    worksheet.set_column('H:H', 14)
    worksheet.set_column('I:J', col_width+4, decimal_fmt)
    worksheet.set_column('K:K', 14)
    worksheet.set_column('B:B', 12)    
      
    # Update notation in sheet
    worksheet.write('C3', 'Overall Shooting', bold_fmt)
    worksheet.write('L3', '3 pt Shooting', bold_fmt)
    worksheet.write('F3', '2s vs 3s (shot selection)', bold_fmt)
    worksheet.write('I3', 'Shot rate (shot volume)', bold_fmt)
    
    worksheet.write('A4', 'Player', bold_fmt)
    
    worksheet.write('B1', 'TFO = Two-for-One window', bold_fmt)
    worksheet.write('F1', 'Note: empty cells denote lack of data for 3-pt shooting for player', bold_fmt)
        
    # Finalize output in workbook
    
    writer.save()

# end excel player table export ----

def export_tables_to_excel():
    """ Exports two tables to excel. Tables of performance stats
    for team and individual level.
    Adds some formatting and other notes describing the data and columns.
    Basically a convenience function call for executing both 
    export_team_table_excel() and export_player_table_excel() together.
    
    Output files hard-coded to both: player_table_out.xlsx and team_table_out.xlsx.
    """
    
    export_team_table_excel()
    export_player_table_excel()

# End export_tables_to_excel

        
    
# -------------------------------------------------------------

# ------------------------------------------

# Here and below is SQL output table stuff. 

# ------------------------------------------

# Write player_report to sql table. 

from pandas.io import sql

import mysql.connector




con = mysqldb.connect()



# ----------------


try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO

bio = BytesIO()

# By setting the 'engine' in the ExcelWriter constructor.
writer = ExcelWriter(bio, engine='xlsxwriter')



# ------------------------------

from sqlalchemy import create_engine

# default
engine = create_engine('mysql://mysql:mysql@localhost/world')


# ---------------------------------


con = mysql.connector.connect(host='localhost',database='world',user='root',password='mysql')

cursor.execute("select * from country")
row = cursor.fetchone()

# -------------------------------------

con = mysql.connector.connect(host='localhost',database='world',user='root',password='mysql')

# --------------------------------------

# Write a dataframe to sql table 
# Db: nbashots

con_nba = mysql.connector.connect(host='localhost',database='nbashots',user='root',password='mysql')

# default
import mysqldb

engine = create_engine('mysql://mysql:mysql@localhost/nbashots')


cursor.execute("")
row = cursor.fetchone()

# -------------------------------------

short_table = player_report.head(30).sort(['plyr_efg_diff'])

short_table[['fga_e3_n', 'plyr_efg_diff', 'plyr_efg_e3', 'plyr_efg_e5', 'shotrate_diff', 'threeperc_diff']]


# --------------------------------------

TABLES = {}
TABLES['team_tfo_perf'] = (
    "CREATE TABLE `team_tfo_perf` ("
    "  `team_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `team_name` varchar(3) NOT NULL,"
    "  `fga_e3_n` int(4) NOT NULL, "
    "  `team_efg_e3` float(4,2), "
    "  `team_efg_e5` float(4,2), "
    "  `team_efg_diff` float(4,2), "
    "  PRIMARY KEY (`team_no`), KEY `team_no` (`team_no`)"
    ") ENGINE=InnoDB")

TABLES['teams'] = (
    "CREATE TABLE `teams` ("
    "  `team_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `team_name` varchar(3) NOT NULL,"
    "  `full_name` varchar(60), "
    "  `city` varchar(30), "
    "  PRIMARY KEY (`team_no`), KEY `team_name` (`team_name`)"
    ") ENGINE=InnoDB")



#name, ddl in TABLES.iteritems():
#    try:
#        print("Creating table {}: ".format(name), end='')
#        cursor.execute(ddl)
#    except err:
#        print 'failed: ', err.msg
#        


cursor = con_nba.cursor()
cursor.execute(TABLES['team_tfo_perf'])

cursor.execute(TABLES['teams'])

# ok - made table 

# ----------------------------

# Insert data into table 



add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
# Insert salary information
data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}

add_team_efg = ("INSERT INTO team_tfo_perf "
               "(team_no, team_name, fga_e3_n, team_efg_e3, team_efg_e5, team_efg_diff) "
               "VALUES (%(team_no)s, %(team_name)s, %(fga_e3_n)s, %(team_efg_e3)s, %(team_efg_e5)s, %(team_efg_diff)s)")
               
add_team_efg_auto_id = ("INSERT INTO team_tfo_perf "
               "(team_name, fga_e3_n, team_efg_e3, team_efg_e5, team_efg_diff) "
               "VALUES (%(team_name)s, %(fga_e3_n)s, %(team_efg_e3)s, %(team_efg_e5)s, %(team_efg_diff)s)")
               
               
# Insert salary information
data_team_perf = {
#    'team_no': 2,
    'team_name': 'ABC',
    'fga_e3_n': 100,
    'team_efg_e3': 0.40,
    'team_efg_e5': 0.50,
    'team_efg_diff': 0.10,
}

# Execute the INSERT

cursor.execute(add_team_efg, data_team_perf)

cursor.execute(add_team_efg_auto_id, data_team_perf)


con_nba.commit()


add_team_efg_raw = ("INSERT INTO team_tfo_perf "
               "(team_no, team_name, fga_e3_n, team_efg_e3, team_efg_e5, team_efg_diff) "
              "VALUES (1, 'ABC', 20, 0.40, 0.50, 0.10)")
              
cursor.execute(add_team_efg_raw)
       
              


# Add in data for Team Table

team_name_list = bigdf['Tm'].unique()

add_team_name = ("INSERT INTO teams "
               "(team_name) "
               "VALUES (%(team_name)s)")
               
team_name_data = {
    'team_name': 'ABC'
}

for team_data in team_name_list:
    team_name_data = {
        'team_name': team_data
    }
    print team_name_data

# Insert multiple rows into db

for team_data in team_name_list:
    team_name_data = {
        'team_name': team_data
    }
    print team_name_data
    
    # add to db
    
    cursor.execute(add_team_name, team_name_data)

con_nba.commit()

# end
    
# Test section

cursor.execute(add_team_name, team_name_data)
con_nba.commit()

        
# Update db for efg performance for all teams

# ... 




