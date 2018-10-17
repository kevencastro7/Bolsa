#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'keven'

from peewee import *

database_file = 'storage.db'
db = SqliteDatabase(database_file)

class BaseModel(Model):
	class Meta:
		database = db

class MassMemory(BaseModel):
	papel = IntegerField(index=True)
	dt = DateTimeField(index=True)
	mass_memory = TextField()

class StorageService(object):

	def __init__(self):
		try:
			if MassMemory.table_exists():
				pass
			else:
				MassMemory.create_table()
		except Exception as e:
			pass

if __name__ == '__main__':
	storage = StorageService()
