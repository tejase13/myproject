#! /usr/bin/python3

import sqlite3 
import shelve
from nltk.corpus import state_union
import collections
relations1 = {'worker':'employee','people':'employee', 'person':'employee',  'staffer':'employee','staff':'employee', 'clerk':'employee', 'personnel':'employee', 'individual':'employee', 'laborer':'employee', 'employer':'employee', 'member':'employee', 'cashier':'employee', 'customer':'employee', 'student':'employee', 'job':'employee', 'employment':'employee', 'proletariat':'employee', 'faculty':'employee', 'participant':'employee', 'officer':'employee','workers':'employee','employees':'employee', 'employee':'employee','emp':'employee','program':'project', 'plan':'project', 'undertaking':'project', 'job':'project', 'task':'project','project':'project','proj':'project','prog':'project','prod':'project','product':'project', 'venture':'project', 'enterprise':'project', 'endeavor':'project', 'activity':'project', 'experiment':'project', 'assignment':'project', 'campaign':'project', 'idea':'project', 'series':'project', 'crusade':'project', 'initiative':'project', 'construction':'project', 'proposal':'project', 'projector ':'project','division':'department','district':'department','agency':'department','ministry':'department','dept':'department','bureau':'department','major':'department','aspect':'department','office':'department','professor':'department','facet':'department','university':'department','committee':'department','profession':'department','departmental':'department','department':'department'}

relations = {}
for key,value in relations1.items():
	relations[key] = value 

print(len(relations))
for key,value in relations1.items():
	key = key + 's'
	relations[key] = value

print(len(relations))
'''
for i in relations:
	s = i + ':' + relations[i]
	print(s)
'''


attr_relations = {'eid':['employee'],'ename':['employee'],'salary':['employee'],'post':['employee'],'phone':['employee'],'pid':['employee','project'],'did':['employee','department'],'dname':['department'],'hod':['department'],'pname':['project'],'pstrength':['project']}

replace_attr = {'names':'name','identity':'id','identities':'id','wage':'salary','wages':'salary','position':'post','designation':'post','positions':'post','designations':'post','contact number':'phone', 'contact':'phone', 'hods':'hod','title':'name','topic':'project','domain':'project','workforce':'strength','manpower':'strength', 'ids':'id', 'income':'salary', 'earning' :' salary'}

syn_attr = (('eid','eid'),('empid','eid'),('employee id','eid'),('emp id','eid'),('emp-id','eid'),('employee-id','eid'),('id of employee','eid'),('employee name','ename'),('ename','ename'),('empname','ename'),('name of employee','ename'),('salary','salary'),('employee salary','salary'),('employee\'s salary','salary'),('employee\'s name','ename'),('employee\'s id','eid'),('salary of employee','salary'),('employee post','post'),('post','post'),('emp post','post'),('post of employee','post'),('project id','pid'),('id of project','pid'),('department id','did'),('id of department','did'),('deptid','did'),('deptid','did'),('did','did'),('dep id','did'),('department name','dname'),('deptname','dname'),('dept name','dname'),('name of department','dname'),('head','hod'), ('hod','hod'),('leader','hod'),('pname','pname'),('project name','pname'),('name of project','pname'),('pstrength','pstrength'),('strength of project','pstrength'),('strength','pstrength'))

syn_attr = collections.OrderedDict(syn_attr)

syn_common = {'hr':'hr','human resource':'hr', 'marketing':'marketing','sale':'sales', 'accounting':'finance', 'finance':'finance','information technology':'information technology', 'financial consultant':'financial consultant', 'CA':'chartered accountant', 'chartered accountant':'chartered accountant' ,'developer':'developer','salesrep':'sales representative', 'sale representative':'sales representative', 'sale strategist':'sales strategist', 'operation manager': 'operations manager', 'officer hr': 'officer hr', 'hr assistant': 'hr assistant', 'business consultant': 'business consultant', 'business analyst': 'business analyst', 'BA':'business analyst'}

common_attr = { 'hr':'dname','marketing':'dname','sales':'dname','finance':'dname','information technology':'dname', 'designer':'post','developer':'post', 'tester':'post', 'sales representative':'post', 'officer hr':'post', 'hr assistant':'post', 'business consultant':'post', 'business analyst':'post', 'operations manager':'post', 'sales strategist':'post', 'sales representative':'post', 'financial consultant':'post', 'chartered accountant':'post'}


relations_attr = {'employee':{'ename':'ename','eid':'eid','did':'did','salary':'salary','post':'post','phone':'phone','pid':'pid'}, 'department':{'did':'deptid','dname':'dname','hod':'hod'}, 'project':{'pid':'projid','pname':'pname','pstrength':'pstrength'}}

attr_datatype = {'eid':'int', 'did': 'int', 'salary':'int', 'post':'varchar', 'phone':'int', 'pid':'int','ename':'varchar', 'deptid':'int','dname':'varchar', 'hod':'varchar', 'projid':'int', 'pname':'varchar', 'pstrength':'int'}
replace_operators = (('>=', '*'), ('is greater equal', '*'), ('is greater and equal', '*'), ('greater equal', '*'), ('greater and equal', '*'), ('greater or equal', '*'), ('is higher equal', '*'), ('is higher and equal', '*'), ('higher and equal', '*'), ('higher or equal', '*'), ('is more equal', '*'), ('is more and equal', '*'), ('more or equal','*'), ('more and equal','*'), ('more equal','*'), ('>', '>'), ('is greater', '>'), ('greater', '>'), ('is higher', '>'), ('higher', '>'), ('is more', '>'), ('more', '>'), ('<=', '/'), ('is less equal', '/'), ('is less and equal', '/'), ('less equal', '/'), ('is lesser equal', '/'), ('is lesser and equal', '/'), ('less and equal', '/'), ('lesser or equal', '/'),  ('lesser and equal', '/'), ('is lower equal', '/'), ('is lower and equal', '/'), ('lower and equal', '/'), ('lower or equal', '/'), ('is smaller equal', '/'), ('is smaller and equal', '/'), ('smaller and equal', '/'), ('smaller or equal', '/'), ('<','<'), ('is lesser', '<'), ('lesser', '<'), ('is smaller', '<'), ('smaller', '<'), ('is lower', '<'), ('lower', '<'), ('is less', '<'), ('less', '<'), ('!=', '!'), ('<>', '!'), ('is not equal', '!'), ('not equal', '!'), ('is equal','='), ('is =','='), ('equal','='), ('is','='))

replace_operators = collections.OrderedDict(replace_operators)
ant_operators = {'=':'!','!':'=','/':'>','>':'/','*':'<','<':'*'}
operator_list = ['=','!','/','>','<','*']

syn_aggregate = (('highest', 'max'), ('max','max'), ('maximum','max'), ('greatest','max'), ('biggest', 'max'), ('most','max'), ('largest','max'), ('least','min'), ('lowest', 'min'), ('min','min'), ('minimum','min'), ('smallest','min'), ('tiniest','min'), ('average','avg'), ('avg','avg'), ('mean','avg'), ('total number','count'), ('count','count'), ('sum','sum'), ('total','sum'), ('summation','sum'), ('add','sum'), ('net','sum'))

syn_aggregate = collections.OrderedDict(syn_aggregate)
aggregate_list = ['max', 'min', 'avg', 'sum', 'count']
replace_contractions = { 
"aini\'t": "am not",
"aren\'t": "are not",
"can\'t": "cannot",
"can\'t\'ve": "cannot have",
"'cause": "because",
"could\'ve": "could have",
"couldn\'t": "could not",
"couldn\'t\'ve": "could not have",
"didn\'t": "did not",
"doesn\'t": "does not",
"don\'t": "do not",
"hadn\'t": "had not",
"hadn\'t\'ve": "had not have",
"hasn\'t": "has not",
"haven\'t": "have not",
"he\'d": "he had",
"he\'d\'ve": "he would have",
"he\'ll": "he shall",
"he\'ll\'ve": "he shall have",
"he\'s": "he has",
"how\'d": "how did",
"how\'d\'y": "how do you",
"how\'ll": "how will",
"how\'s": "how has",
"I\'d": "I had",
"I\'d\'ve": "I would have",
"I\'ll": "I shall",
"I\'ll\'ve": "I shall have",
"I\'m": "I am",
"I\'ve": "I have",
"isn\'t": "is not",
"it\'d": "it had",
"it\'d\'ve": "it would have",
"it\'ll": "it shall",
"it\'ll\'ve": "it shall have",
"it\'s": "it has",
"let\'s": "let us",
"ma\'am": "madam",
"mayn\'t": "may not",
"might\'ve": "might have",
"mightn\'t": "might not",
"mightn\'t\'ve": "might not have",
"must\'ve": "must have",
"mustn\'t": "must not",
"mustn\'t\'ve": "must not have",
"needn\'t": "need not",
"needn\'t\'ve": "need not have",
"o\'clock": "of the clock",
"oughtn\'t": "ought not",
"oughtn\'t\'ve": "ought not have",
"shan\'t": "shall not", 
"sha\'n\'t": "shall not",
"shan\'t\'ve": "shall not have",
"she\'d": "she had",
"she\'d\'ve": "she would have",
"she\'ll": "she shall",
"she\'ll\'ve": "she shall have",
"she\'s": "she has",
"should\'ve": "should have",
"shouldn\'t": "should not",
"shouldn\'t\'ve": "should not have",
"so\'ve": "so have",
"so\'s": "so as",
"that\'d": "that would",
"that\'d\'ve": "that would have",
"that\'s": "that has",
"there\'d": "there had",
"there\'d\'ve": "there would have",
"there\'s": "there has",
"they\'d": "they had",
"they\'d\'ve": "they would have",
"they\'ll": "they shall",
"they\'ll\'ve": "they shall have",
"they\'re": "they are",
"they\'ve": "they have",
"to\'ve": "to have",
"wasn\'t": "was not",
"we\'d": "we had",
"we\'d\'ve": "we would have",
"we\'ll": "we will",
"we\'ll\'ve": "we will have",
"we\'re": "we are",
"we\'ve": "we have",
"weren\'t": "were not",
"what\'ll": "what shall",
"what\'ll\'ve": "what shall have",
"what\'re": "what are",
"what\'s": "what has",
"what\'ve": "what have",
"when\'s": "when has",
"when\'ve": "when have",
"where\'d": "where did",
"where\'s": "where has",
"where\'ve": "where have",
"who\'ll": "who shall",
"who\'ll've": "who shall have",
"who\'s": "who has",
"who\'ve": "who have",
"why\'s": "why has",
"why\'ve": "why have",
"will\'ve": "will have",
"won\'t": "will not",
"won\'t\'ve": "will not have",
"would\'ve": "would have",
"wouldn\'t": "would not",
"wouldn\'t\'ve": "would not have",
"y\'all": "you all",
"y\'all\'d": "you all would",
"y\'all\'d\'ve": "you all would have",
"y\'all\'re": "you all are",
"y\'all\'ve": "you all have",
"you\'d": "you had",
"you\'d\'ve": "you would have",
"you\'ll": "you shall",
"you\'ll\'ve": "you shall have",
"you\'re": "you are",
"you\'ve": "you have",
"neither":"not",
"nor":"not or",
"either":"or",
"but":"and",
"how many":"count"
}

#DB part from proper noun
conn = sqlite3.connect('be_proj_check.db')
''' We need to use the Connection instance method cursor() to return a Cursor instance corresponding to the database we want to query.
'''
cursor = conn.cursor()
cursor.execute('SELECT ename FROM employee;')
results = cursor.fetchall()
proper_nouns = {}

for name in results:
	proper_nouns[name[0].lower()] = 'ename'

cursor.execute('SELECT hod FROM DEPARTMENT;')
results = cursor.fetchall()

for name in results:
	proper_nouns[name[0].lower()] = 'hod'

cursor.execute('SELECT pname FROM PROJECT;') 
results = cursor.fetchall()

for name in results:
	proper_nouns[name[0].lower()] = 'pname'
conn.commit()
train_text = state_union.raw("2005-GWBush.txt")

conf = shelve.open('conf')
conf['train_text'] = train_text
conf['relations'] = relations
conf['attr_relations'] = attr_relations
conf['replace_attr'] = replace_attr
conf['syn_attr'] = syn_attr
conf['syn_common'] = syn_common
conf['common_attr'] = common_attr
conf['relations_attr'] = relations_attr
conf['replace_contractions'] = replace_contractions
conf['replace_operators'] = replace_operators
conf['ant_operators'] = ant_operators
conf['operator_list'] = operator_list
conf['syn_aggregate'] = syn_aggregate
conf['aggregate_list'] = aggregate_list
conf['attr_datatype'] = attr_datatype
conf['proper_nouns'] = proper_nouns
conf.close()
