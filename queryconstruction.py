#! /usr/bin/python3
import shelve,time

class QueryConstruction:
	
	def __init__ (self, select_list, from_list, where_list, unique_attribute_relation):
		conf = shelve.open('conf')
		self.attr_relations = conf['attr_relations']
		self.relations_attr = conf['relations_attr']
		self.select_list = select_list
		self.from_list = from_list
		self.where_list = where_list
		self.unique_attribute_relation = unique_attribute_relation

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

	def checkJoin(self):
		if len(self.unique_attribute_relation) > 1:
			self.select_list = []
			
			for key in self.attr_relations:
				flag = True
				rel = self.attr_relations[key]
				if len(rel) > 1:
					for element in rel:
						if element not in self.unique_attribute_relation:
							flag = False
							break
				else:
					flag = False

				if flag is True:
					self.where_list.append('and')
					for element in rel:
						print("key=",key," element=",element)
						where_key = element
						where_key += "."
						where_key += self.relations_attr[element][key]
						self.where_list.append(where_key)
						self.where_list.append ("=")
					self.where_list.pop(-1)	
					print("where list", self.where_list)



	def constructFromPart(self):
		self.final_query += "from "
		
		for index in range(len(self.unique_attribute_relation)):
			self.final_query += self.unique_attribute_relation[index]
			if index < len(self.unique_attribute_relation) - 1:
				self.final_query += ","


	def constructWherePart(self):

		if len(self.where_list) == 0:
			return

		self.final_query += " where "
		for index in range(len(self.where_list)):
			if (index + 1) % 4 == 3:
				if self.where_list[index].isdigit():
					self.final_query += self.where_list[index]	
				else:
					self.final_query += '\''
					self.final_query += self.where_list[index]
					self.final_query += '\''
					
			elif self.where_list[index] == "*":
				self.final_query += ">="

			elif self.where_list[index] == "/":
				self.final_query += "<="

			elif self.where_list[index] == "!":
				self.final_query += "!="

			else:
				self.final_query += self.where_list[index]
			self.final_query += " "
	

