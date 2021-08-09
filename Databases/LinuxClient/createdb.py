from tinydb import TinyDB, Query

import os

cmd = 'rm *.db'
os.system(cmd)

def rentable() :
  dbt = TinyDB('mydb.db')
  dbt.drop_table('Hr')
  tabx = dbt.table('Hr')
  for i in range(1,500):
      tabx.insert({'id':i, 'age': 10 ,'nom': 'Salah', 'years':1000 })
  return dbt
rentable()

def school() :
  dbt = TinyDB('school.db')
  dbt.drop_table('Hr')
  tabx = dbt.table('Hr')
  tabx.insert({'nom': 'Salah', 'years':0    ,'id':1 })
  tabx.insert({'nom': 'Ahmed', 'years':2000 ,'id':2 })
  tabx.insert({'nom': 'Rajae', 'years':2500 ,'id':3 })
  tabx.insert({'nom': 'Hamid', 'years':1000 ,'id':4 })

  return dbt
school()

