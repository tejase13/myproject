#! /usr/bin/python3
import shelve,time

class QueryConstruction:
	
	def __init__ (self, select_list, where_list, unique_attribute_relation, common_attribute_relation):
		conf = shelve.open('conf')
		self.attr_relations = conf['attr_relations']
		self.relations_attr = conf['relations_attr']
		self.attr_datatype = conf['attr_datatype']
		self.select_list = select_list
		self.where_list = where_list
		self.unique_attribute_relation = unique_attribute_relation
		self.common_attribute_relation = common_attribute_relation

		self.final_query = ""

	def constructSelectPart(self):
		self.final_query += "select "
		if len(self.select_list) == 0:
			self.final_query += "* "
		else:
			for index in range(len(self.select_list)):
				if self.select_list[index].find('(') != -1:
					start_index = self.select_list[index].find('(')
					end_index = self.select_list[index].find(')')
					attribute_name = self.select_list[index][start_index + 1:end_index]
					if attribute_name != '*':
						rel = self.attr_relations[attribute_name]
						for element in rel:
							if element in self.unique_attribute_relation:
								attribute_name = self.relations_attr[element][attribute_name]
								break
						new_string = self.select_list[index][0:start_index]
						new_string += '('
						new_string += attribute_name
						new_string += ')'
						self.select_list[index] = new_string
				else:		
					rel = self.attr_relations[self.select_list[index]]
					for element in rel:
						if element in self.unique_attribute_relation:
							self.select_list[index] = self.relations_attr[element][self.select_list[index]]
							break
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
	
		if len(self.unique_attribute_relation) > 0:
			for index in range(len(self.unique_attribute_relation)):
				self.final_query += self.unique_attribute_relation[index]
				if index < len(self.unique_attribute_relation) - 1:
					self.final_query += ","
			return True
		
		if len(self.common_attribute_relation) > 0:
			self.final_query += self.common_attribute_relation[0]
			return True
		
		else:
			self.final_query = "Invalid Query. Please provide appropriate information."
			return False

	def constructWherePart(self):

		if len(self.where_list) == 0:
			return

		self.final_query += " where "
		for index in range(len(self.where_list)):
			if (index + 1) % 4 == 3:
				if self.where_list[index - 2] in self.attr_datatype:
					if self.attr_datatype[self.where_list[index - 2]] == 'varchar':
						self.final_query += '\'' 
						if self.where_list[index - 2] == 'ename' or self.where_list[index - 2] == 'hod':
							self.final_query += self.where_list[index].upper()
						else:
							self.final_query += self.where_list[index]
						self.final_query += '\''
					elif self.attr_datatype[self.where_list[index - 2]] == 'int':
						self.final_query += self.where_list[index]
				else:
					self.final_query += self.where_list[index]
			elif self.where_list[index] == "*":
				self.final_query += ">="

			elif self.where_list[index] == "/":
				self.final_query += "<="

			elif self.where_list[index] == "!":
				self.final_query += "!="

			else:
				if self.where_list[index] in self.attr_relations:
					rel = self.attr_relations[self.where_list[index]]
					for element in rel:
						if element in self.unique_attribute_relation:
							self.where_list[index] = self.relations_attr[element][self.where_list[index]]
							break
				self.final_query += self.where_list[index]
			self.final_query += " "
	

