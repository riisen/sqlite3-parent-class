# sqlite3-parent-class
a parent class for sqlite3

## Example
	class CarsDB(db.Databas):
	
		def __init__(self, db='example.db'):
			super().__init__('cars', db)
			super().add_column('license_plate', 'TEXT', 1)
			super().add_column('brand', 'TEXT')
			super().add_column('model', 'TEXT')
			super().add_column('year', 'INTEGER')
			self.create_database_table()
    
		def get_all(self):
			return super().select()
			
	  	def get_this_one(self, idx):
			return super().select(None, None, idx, True)
		
		def create_new(self, license_plate, brand, model, year):
			super().query_this(super().insert_into_query(),(
				license_plate,
				brand,
				model,
				year)
			)

##### __init__(table, db='Database.db')
table : [string]
	the name of the table your class will represent
	
db : [string]
	the name of the database file sqlite3 will use

##### add_column(name, kind, primary_key=None)
name : [string]
	column name in the table
	
kind : [string]
	the type of the column (INTEGER, REAL, TEXT, BLOB)
	
primary_key : [integer]
	if not None it is primary key in sqlite3 db

##### create_database_table()
is kinda self explanatory but runs a CREATE TABLE IF NOT EXISTS
with the table name and columns you add to youre class

##### select(cols=None, table=None, where=None, fetchone=None)
cols : [string]
	which columns you wanna select, if None use every one

table : [string]
	which table to select from, if None this table is used
	
where : [string]
	the column value of the primary_key in db table
	
fetchone : [integer]
	if None fetchall else fetchone
	
##### query_this(q, v, ret)
q : [string]
	sql query (for example: "UPDATE bilar SET year = 1960 WHERE license_plate = ?")
	
v : [tuple]
	value's of all the question marks in q
	
ret : [bool]
	should it fetch results and return them

##### insert_into_query()
will return "INSERT INTO cars(license_plate, brand, model, year) VALUES(?, ?, ?, ?)" for this example
