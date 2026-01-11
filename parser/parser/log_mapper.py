import re

from .parser_mapper import Mapper, mclass, method, field

from itertools import zip_longest

class InculdeMapping:
    def __init__(self, mapper: Mapper, imapper: list[mclass]) -> None:
        self.__include_mapping = sum([ mapper.parser[_mclass]+[_mclass.short_class] for _mclass in imapper ], [])
        self.__map_mapping = { fuild.mapper_name: fuild.full_name for fuild in self.__include_mapping }
        
        # for x in self.__include_mapping.copy():
        #     if not isinstance(x, method):
        #         continue
        #     if x.return_class not in self.__include_mapping:
        #         print(x, x.return_class)
        #         if x.return_class is not None:
        #             # self.__include_mapping.append(  )
        #             self.__include_mapping = sum([ mapper.parser[x.return_class] ], [])
        
    
    def __iter__(self):
        return iter(self.__map_mapping)

    def __getitem__(self, key):
        if key not in self.__map_mapping:
            raise KeyError(f"Не нйден ключ {key} в InculdeMapping")
        return self.__map_mapping[key]
    
class FunnyMapping:
    def __init__(self, mapper: Mapper):
        self.__include_mapping = sum([ mapper.parser[_mclass] for _mclass in mapper.parser ], [])
        self.__map_mapping = { fuild.mapper_name: fuild.full_name for fuild in self.__include_mapping }
        self.c = self.__map_mapping.copy()

    def __iter__(self):
        return iter(self.__map_mapping)
    def __getitem__(self, key):
        if key not in self.__map_mapping:
            raise KeyError(f"Не нйден ключ {key} в FunnyMapping")
        return self.__map_mapping[key]

# def map_log(data: str, mapper: Mapper) -> str:
#     import_mapper = [ mapper.map[fclass.replace("import ", "")] for fclass in re.findall(mclass.import_regex, data) ]
#     if len(import_mapper) == 0: return data
    
#     import_mapper += sum([x.children for x in import_mapper], [])
#     include_mapping = InculdeMapping(mapper, import_mapper)
#     funny_mapping   = FunnyMapping  (mapper)

#     # imports
#     for iclass in import_mapper:
#         data = data.replace(iclass.mapper_name, iclass.full_name, 1)

#     # class.class / class / class_.field_ 
#     for iclass in include_mapping:
#         data = data.replace(iclass, include_mapping[iclass])

#     # non imports and non in class :/ method_11657 class_2680(class_2688)
#     fr = re.findall(field.field_regex  , data)
#     mr = re.findall(method.method_regex, data)
#     for _field, _method in list(zip_longest(fr,mr, fillvalue=None)):
#         # print(_field, _method)
#         try:
#             if _field is not None:  data = data.replace( _field, funny_mapping[_field ], 1 )
#             if _method is not None: data = data.replace(_method, funny_mapping[_method], 1 )
#         except KeyError as e:
#             print(f"{e}")

#     return data

def map_log(data: str, mapper: Mapper) -> str:
    # 1. Создаем плоский словарь для мгновенного поиска O(1)
    # Мы объединяем все классы, методы и поля в одну таблицу замен
    lookup = {}
    
    # Добавляем полные имена классов (net.minecraft.class_3721 -> BellBlockEntity)
    for full_m_name, m_obj in mapper.map.items():
        lookup[full_m_name] = m_obj.full_name
        # Добавляем короткие имена для работы внутри файлов (class_3721 -> BellBlockEntity)
        short_m_name = full_m_name.split('.')[-1]
        lookup[short_m_name] = m_obj.full_name.split('.')[-1]

    # Добавляем методы и поля
    for m_class_obj, members in mapper.parser.items():
        for member in members:
            lookup[member.mapper_name] = member.full_name

    # 2. Регулярное выражение, которое находит ВСЕ цели сразу
    # Ищем слова, начинающиеся на class_, method_ или field_
    pattern = re.compile(r'\b(class_\d+|method_\d+|field_\d+|net\.minecraft\.class_\d+)\b')

    # 3. Функция-заменитель
    def replace_match(match):
        word = match.group(0)
        # Если ключ есть в Tiny файле — меняем, если нет — оставляем как есть
        # Это решает твою проблему с "не нашел ключ"
        return lookup.get(word, word)

    # 4. Один проход по тексту — это в сотни раз быстрее циклов!
    return pattern.sub(replace_match, data)