# sqlite3-parent-class
a parent class for sqlite3

# Example
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
			
	  	def get_this_one(self, idx)
			return super().select(None, None, idx, True)

the init function takes 2 parameters (table_name, database_name)

the add_column function can take 3 parameters (name, type, primary_key)

create_database_table is kinda self explanatory

select function can take 4 parameters (cols, table, where, fetchone)
if all are None (default) it takes all columns in this table and fetches all and returns the fetched list
