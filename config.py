import peewee

class BaseModel(peewee.Model):
  class Meta:
    database = peewee.SqliteDatabase('banco_dados.db')