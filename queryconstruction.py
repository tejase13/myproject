#! /usr/bin/python3


class QueryConstruction:
	
	def __init__ (self, select_list, from_list, where_list):
		self.select_list = select_list
		self.from_list = from_list
		self.where_list = where_list

		self.final_query = ""



	def constructSelectPart(self):
		self.final_query += "select "
		if len(self.select_list) == 0:
			self.final_query += "* "
		else:
			for index in range(len(self.select_list)):
				self.final_query += self.select_list[index]
				if index < len(self.select_list) - 1:
					self.final_query += ","

			self.final_query += " "


	def getMaxKey(self):
		maxValue = 0
		maxKey = None 
		for key in self.from_list:
			if self.from_list[key] > maxValue:
				maxValue = self.from_list[key] 
				maxKey = key

		return maxKey
	def constructFromPart(self):
		self.final_query += "from "
		
		relation = self.getMaxKey()
		self.final_query += relation
		self.final_query += " "


	def constructWherePart(self):
		self.final_query += "where "
		
		for index in self.where_list:
			self.final_query += index
			self.final_query += " "
	
		print (self.final_query)

