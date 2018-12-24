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
    
  def get_all():
      return super().select()
      
  def get_this_one(self, idx)
      return super().select(None, None, idx, True)
