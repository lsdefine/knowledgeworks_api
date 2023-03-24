CN-DBpedia & CN-Probase API Utils
========
* http://kw.fudan.edu.cn/apis/intro/ 
* http://shuyantech.com/docuapi

```python
# encoding=utf-8
import kw_api as api

api.SetApiKey('')
# without it, some api requests will be blocked 
# goto http://shuyantech.com/ for a free key

api.SetCacheSize(size=100000)

print(api.Ment2Ent('上海'))
# {'上海': ['上海（中华人民共和国直辖市）', '上海（小行星）', '上海（任天堂game boy掌机游戏《上海》）', '上海（倪锡英的著作）', '上海（钟立风演唱歌曲）']}
print(api.Ment2Ent(['中国','李白']))
# {'中国': ['中国（世界四大文明古国之一）', '中华人民共和国', ..., 
#  '李白': ['李白（唐代著名浪漫主义诗人）', '李白（李荣浩演唱歌曲）', ...
#  }

ent = list(api.Ment2Ent('周杰伦').values())[0][0]
print(ent)
# '周杰伦（华语流行乐男歌手、音乐人、演员、导演）'

print(api.GetEntMentions(ent))
# ['jay chou', '周杰倫', '周杰伦', '小公举', '周董' ...]

print(api.GetEntDesc(ent))
# '周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市 ...

print(api.GetEntAttrValues(ent, '出生日期'))
# ['1979年01月18日']
print(api.GetEntAttrValuesMulti([ent, '方文山'], '出生日期'))
# {'周杰伦（华语流行乐男歌手、音乐人、演员、导演）': ['1979年01月18日'], '方文山': ['1969年01月26日']}

print(api.GetEntListTriples('复旦大学'))
# [['历届校友', ['邵力子', '罗家伦', '陈维稷', '王铁崖', '包蕾', '洪绂曾'], ['国家级教学团队', ['物理化学系列课程教学团队', '复旦大学汉语言文学原典精读系列课程教学团队', ...

print(api.GetEntInvTriples('许宁生'))
# [['i现任校长', '复旦大学'], ['i致词人', '珠三角改革发展研究院'], ['i副校长', '中山大学莱恩功能材料研究所']]

print(api.GetEntClicks(ent))
# {'周杰伦（华语流行乐男歌手、音乐人、演员、导演）': 72638580}
print(api.GetEntClicks([ent, '方文山']))
# {'周杰伦（华语流行乐男歌手、音乐人、演员、导演）': 72638580, '方文山': 9010477}

print(api.IsEnt([ent, '周3杰伦']))
# {'周杰伦（华语流行乐男歌手、音乐人、演员、导演）': True, '周3杰伦': False}

print(api.GetEntsByConcept('歌手'))
# ['陈伟霆', '鹿晗', '周笔畅', '黄子韬', '张艺兴', '易烊千玺', '赵丽颖', '杨幂', ...
print(api.GetEntConcepts(ent))
# ['人物', '演员', '娱乐人物', '歌手', '音乐人物', '导演', '企业家', '编剧', '制作人', '音乐人']
print(api.GetEntConceptsMulti([ent,'林俊杰','复旦大学']))
# {'周杰伦（华语流行乐男歌手、音乐人、演员、导演）': [['人物', 1299103], ['演员', 59658], ['娱乐人物', 25299], ...], 
#  '林俊杰': [['人物', 1299103], ['演员', 59658], ['作家', 45715], ...], 
#  '复旦大学': [['学校', 143990], ['大学', 1961], ['中国大学', 1933], ...]}

print(api.GetEntTriples(ent))
# [['中文名', '周杰伦'], ['外文名称', 'Jay Chou'], ['别名', '周董'], ['国籍', '中国'], ...
print(api.GetEntTriplesMulti([ent, '复旦大学']))
# {'周杰伦（华语流行乐男歌手、音乐人、演员、导演）': [['中文名', '周杰伦'], ['外文名称', 'Jay Chou'], ['别名', '周董'], ['国籍', '中国'], ['民族', '汉族'], ...
#  '复旦大学': [['中文名', '复旦大学'], ['英文名称', 'Fudan University'], ['简称', '复旦·FUDAN'], ...
#  }
```

