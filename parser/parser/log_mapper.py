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

def map_log(data: str, mapper: Mapper) -> str:
    import_mapper = [ mapper.map[fclass.replace("import ", "")] for fclass in re.findall(mclass.import_regex, data) ]
    if len(import_mapper) == 0: return data
    
    import_mapper += sum([x.children for x in import_mapper], [])
    include_mapping = InculdeMapping(mapper, import_mapper)
    funny_mapping   = FunnyMapping  (mapper)

    # imports
    for iclass in import_mapper:
        data = data.replace(iclass.mapper_name, iclass.full_name, 1)

    # class.class / class / class_.field_ 
    for iclass in include_mapping:
        data = data.replace(iclass, include_mapping[iclass])

    # non imports and non in class :/ method_11657 class_2680(class_2688)
    fr = re.findall(field.field_regex  , data)
    mr = re.findall(method.method_regex, data)
    for _field, _method in list(zip_longest(fr,mr, fillvalue=None)):
        # print(_field, _method)
        try:
            if _field is not None:  data = data.replace( _field, funny_mapping[_field ], 1 )
            if _method is not None: data = data.replace(_method, funny_mapping[_method], 1 )
        except KeyError as e:
            print(f"{e}")

    return data