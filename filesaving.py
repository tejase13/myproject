#! /usr/bin/python3

import shelve
import collections
relations1 = {'worker':'employee', 'staffer':'employee','staff':'employee', 'clerk':'employee', 'personnel':'employee', 'individual':'employee', 'laborer':'employee', 'employer':'employee', 'member':'employee', 'cashier':'employee', 'workforce':'employee', 'customer':'employee', 'student':'employee', 'job':'employee', 'employment':'employee', 'proletariat':'employee', 'faculty':'employee', 'participant':'employee', 'officer':'employee','workers':'employee','employees':'employee', 'employee':'employee','emp':'employee','program':'project', 'plan':'project', 'undertaking':'project', 'job':'project', 'task':'project','project':'project','proj':'project','prog':'project','prod':'project','product':'project', 'venture':'project', 'work':'project', 'enterprise':'project', 'endeavor':'project', 'activity':'project', 'experiment':'project', 'assignment':'project', 'campaign':'project', 'idea':'project', 'series':'project', 'crusade':'project', 'initiative':'project', 'construction':'project', 'proposal':'project', 'projector ':'project','division':'department','district':'department','agency':'department','ministry':'department','dept':'department','bureau':'department','major':'department','aspect':'department','office':'department','professor':'department','facet':'department','university':'department','committee':'department','profession':'department','departmental':'department','department':'department'}

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

replace_attr = {'names':'name','identity':'id','identities':'id','wage':'salary','wages':'salary','position':'post','designation':'post','positions':'post','designations':'post','contact number':'phone', 'contact':'phone', 'hods':'hod','title':'name','topic':'project','domain':'project','workface':'strength','manpower':'strength', 'ids':'id'}

syn_attr = (('eid','eid'),('empid','eid'),('employee id','eid'),('emp id','eid'),('emp-id','eid'),('employee-id','eid'),('id of employee','eid'),('employee name','ename'),('ename','ename'),('empname','ename'),('name of employee','ename'),('salary','salary'),('employee salary','salary'),('employee\'s salary','salary'),('employee\'s name','ename'),('employee\'s id','eid'),('salary of employee','salary'),('employee post','post'),('post','post'),('emp post','post'),('post of employee','post'),('project id','pid'),('id of project','pid'),('department id','did'),('id of department','did'),('deptid','did'),('deptid','did'),('did','did'),('dep id','did'),('department name','dname'),('deptname','dname'),('dept name','dname'),('name of department','dname'),('head','hod'), ('hod','hod'),('leader','hod'),('pname','pname'),('project name','pname'),('name of project','pname'),('pstrength','pstrength'),('strength of project','pstrength'),('strength','pstrength'))

syn_attr = collections.OrderedDict(syn_attr)

syn_common = {'hr':'hr','human resources':'hr','marketing':'marketing','sales':'sales','finance':'finance','it':'it','manager':'manager','lead':'lead','developer':'developer','salesrep':'salesrep'}

common_attr = { 'hr':'dname','marketing':'dname','sales':'dname','finance':'dname','it':'dname','manager':'post','lead':'post','developer':'post','salesrep':'post'}


relations_attr = {'employee':{'eid':'eid','did':'did','salary':'salary','post':'post','phone':'phone','pid':'pid'}, 'department':{'did':'deptid','dname':'dname','hod':'hod'}, 'project':{'pid':'projid','pname':'pname','pstrength':'pstrength'}}

replace_operators = (('>=', '*'), ('greater equal', '*'), ('greater and equal', '*'), ('greater or equal', '*'), ('higher and equal', '*'), ('higher or equal', '*'),('more','>'),('more or equal','*'),('more and equal','*'),('more equal','*'),('<=', '/'), ('less equal', '/'), ('lesser and equal', '/'), ('less and equal', '/'), ('lesser or equal', '/'),  ('lesser and equal', '/'),('lower and equal', '/'), ('lower or equal', '/'), ('smaller and equal', '/'), ('smaller or equal', '/'),('!=', '!'), ('<>', '!'), ('not equal', '!'), ('no', '!'),('>', '>'), ('greater', '>'), ('higher', '>'),('<','<'), ('lesser', '<'), ('smaller', '<'), ('lower', '<'))

replace_operators = collections.OrderedDict(replace_operators)
ant_operators = {'=':'!','!':'=','/':'>','>':'/','*':'<','<':'*'}
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
"you\'ve": "you have"
}


conf = shelve.open('conf')
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

conf.close()
