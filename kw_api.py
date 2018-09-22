# coding=utf-8
import math, os, requests, re, json
import warnings
from datetime import datetime

apikey = ''
CACHESIZE = 0

apihost = 'http://shuyantech.com/api/'

def SetApiKey(key):
	global apikey
	apikey = key

def SetCacheSize(size=100000):
	global CACHESIZE
	CACHESIZE = size

class Cache:
	cache = {}
	def get(self, key):
		return self.cache.get(key)
	def insert(self, key, value):
		if CACHESIZE <= 0: return value
		if len(self.cache) > CACHESIZE: self.cache.clear()
		self.cache[key] = value
		return value
cache = Cache()

def GetAPI(apiurl, data, apihost=apihost):
	if apikey == '':
		warnings.warn('Please set your apikey by calling the SetApiKey(key) function, the parameter key is your apikey'
					  'If you don\'t have an apikey, please goto http://shuyantech.com/ for one first.')
	else:
		data['apikey'] = apikey
	ky = apiurl + str(data)
	if len(ky) < 100:
		rr = cache.get(ky)
		if rr: return rr
	for i in range(3):
		try:
			host = apihost if type(apihost) is type('') else apihost[i%len(apihost)]
			r = requests.post(host + apiurl, data=data, timeout=1)
			return cache.insert(ky, r.json())
		except:
			pass
	return {}


def Ment2Ent(ments):
	'''
	:param ments: Input an entity or a list of entity mentions
	:return: entities list : [{'m':ments, 'e':[]}]
	'''
	query = '\t'.join(ments) if type(ments) is not type('') else ments
	rr = GetAPI('cndbpedia/ment2entmulti', {'q': query}).get('ret', [])
	return {x['m']:x['e'] for x in rr}

def GetEntMentions(ent):
	'''
	:param ent: Input an entity
	:return: A list of mentions : [m1,m2,...]
	'''
	rets = GetAPI('cndbpedia/ent2ment',{'q':ent}).get('ret',[])
	return rets

def GetEntDesc(ent):
	'''
	:param ent: Input an entity
	:return: descriptions of this entity : String
	'''
	return (GetAPI('cndbpedia/value', {'q': ent, 'attr': 'DESC'}).get('ret', []) + [''])[0]


def GetEntTags(ents):
	'''
	:param ents: Input a list of entities
	:return: tags of this entity : [{'e':ents, 'values':[tag1,tag2....]}]
	'''
	query = '\t'.join(ents) if type(ents) is not type('') else ents
	return GetAPI('cndbpedia/valuemulti', {'q': query, 'attr': 'CATEGORY_ZH'}).get('ret', [])

def GetEntType(ent):
	'''
	:param ent:  Input entity
	:return: the type of this entity in DBpedia : [type1,type2,...]
	'''
	rets = GetAPI('cndbpedia/type', {'q': ent}).get('ret', [])
	return rets

def GetEntTypes(ents):
	'''
	:param ents: Input a list of entities : [s1,s2,...]
	:return: The type information of this entity in DBpedia : {s1:[type1,type2...],s2:[],...}
	'''
	rets = GetAPI('cndbpedia/typemulti', {'q': '\t'.join(ents)}).get('ret', [])
	rr = {}
	for item in rets:
		ent, tps = item['e'], item['type']
		rr[ent] = tps
	return rr


def GetEntAttrValues(ent, attr):
	'''
	:param ent: Input an entity
	:param attr: Input a attribute of this entity
	:return: value of this entity，attribute : [v1,v2,...]
	'''
	rets = GetAPI('cndbpedia/value', {'q':ent, 'attr':attr}).get('ret',[])
	return rets

def GetEntAttrValuesMulti(ents, attr):
	'''
	:param ents: Input a list of entities
	:param attr: Input an attribute of these entities
	:return: value of these entities, attribute : [{e1:[v1,v2,...],e2:[v21,v22,...]}]
	'''
	rets = GetAPI('cndbpedia/valuemulti', {'q': '\t'.join(ents), 'attr': attr}).get('ret', [])
	retdict = {}
	for ent in rets:
		values = ent.get('values',[])
		retdict[ent.get('e')] = values
	return retdict

def GetEntListTriples(ent):
	'''
	:param ent: Input entity
	:return: list properties and values of this entity : [[p1, [v11,v12,...]],[p2,[v21,v22,....]]...]
	'''
	trs = GetAPI('cndbpedia/avpair_list', {'q': ent}).get('ret', [])
	return trs

def GetEntInvTriples(ent):
	'''
	:param ent: Input entity
	:return: inverse triples of this entity, return a list of p,s which o is this entity : [[p1,s1],[p2,s2]...]
	'''
	trs = GetAPI('cndbpedia/avpair_inv', {'q': ent}).get('ret', [])
	return trs

def GetEntClicks(ents):
	'''
	:param ents: Input a list of entity
	:return: popularity of this entity :[{'e': ents, 'click': num}]
	'''
	query = '\t'.join(ents) if type(ents) is not type('') else ents
	rr = GetAPI('cndbpedia/entclick', {'q': query}).get('ret', [])
	return {x['e']:x['click'] for x in rr}

def RM(patt, sr):
	mat = re.search(patt, sr, re.DOTALL | re.MULTILINE)
	return mat.group(1) if mat else ''
def CalcAge(trs):
	zz = [x for x in trs if x[0] == '出生日期']
	zv = [x for x in trs if x[0] == '逝世日期']
	if len(zz) > 0 and len(zv) == 0:
		year = RM('([0-9]{4})', zz[0][1])
		if year != '': return [['年龄', str(datetime.now().year - int(year)) + '岁']]
	return []

def GetEntTriples(ent, keephref=False):
	'''
	:param ent: Input entity
	:return: triples of entities : [[p1:v1],[p2,v2],...]
	'''
	query = {'q': ent}
	if keephref: query['keephref'] = 1
	trs = GetAPI('cndbpedia/avpair', query).get('ret', [])
	trs.extend(CalcAge(trs))
	return trs

def GetEntTriplesMulti(ents, keephref=False):
	'''
	:param: Input a list of entities
	:return: The triples of these entities : {s1:[[p1,v1],...], s2:[[p2,v2],...]}
	'''
	query = {'q': '\t'.join(ents), 'nospecial': 1}
	if keephref: query['keephref'] = 1
	rets = GetAPI('cndbpedia/avpairmulti', query).get('ret', [])
	rr = {}
	for item in rets:
		ent, trs = item['e'], item['avpairs']
		trs.extend(CalcAge(trs))
		rr[ent] = trs
	return rr


def GetEntConcepts(ents):
	'''
	:param ents: Input a entity
	:return: Concepts of this entity: [c1,c2,c3]
	'''
	query = ents
	rets = GetAPI('cnprobase/concept', {'q': query}).get('ret',[])
	return [item[0] for item in rets]

def GetEntConceptsMulti(ents):
	'''
	:param ents: Input a list of entities
	:return: Concepts of each entity
	'''
	query = '\t'.join(ents) if type(ents) is not type('') else ents
	rets = GetAPI('cnprobase/conceptmulti', {'q': query}).get('ret',[])
	retdict = {}
	for item in rets:
		ent = item.get('e','')
		cons = item.get('concepts',[])
		retdict[ent] = cons
	return retdict

def GetEntsByConcept(con):
	'''
	:param con: Input a concept
	:return: Entities of this concept : [e1,e2,...]
	'''
	rets = GetAPI('cnprobase/entity',{'q': con}).get('ret',[])
	return [item[0] for item in rets]

def IsEnt(ents):
	'''
	:param ents: Input a mention or a list of mentions
	:return: If the mention is an entity then return True else return False : {m1:False, m2:True}
	'''
	query = '\t'.join(ents) if type(ents) is not type('') else ents
	rets = GetAPI('cndbpedia/isentmulti', {'q': query}).get('ret',[])
	retdict = {}
	for item in rets:
		ent = item.get('e','')
		isent = item.get('isent','')
		retdict[ent] = isent
	return retdict


if __name__ == '__main__':
	print(Ment2Ent('dota'))
	print('completed')
