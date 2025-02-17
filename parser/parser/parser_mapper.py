from typing import List, Dict, Self

class mclass:
    "class"
    full_class_regex = r"(net\.minecraft\.class_(\d+)(?:\.class_(\d+))?)"
    class_regex = r"(class_(\d+)(?:\.class_(\d+))?)"
    import_regex = r"(import net\.minecraft\.class_\d+(?:\.class_\d+)?)"
    
    def __init__(self, mapper_class: str, full_class: str) -> None:
        self.mapper_name = mapper_class
        self.full_name = full_class
        self.short_class = sclass(mapper_class.split(".")[-1], full_class.split(".")[-1])
        self.children: list[mclass] = []
        pass

    def __repr__(self) -> str:
        return f"< {self.__class__.__name__}: {self.mapper_name} >"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.mapper_name == other
        
        elif isinstance(other, self.__class__):
            return self.mapper_name == other.mapper_name
        
        return False
    
    def __hash__(self) -> int:
        return hash(self.mapper_name)
    

    def copy(self) -> "Self":
        return self.__class__(self.mapper_name, self.full_name)

class sclass:
    "Short Class"
    def __init__(self, mapper_class, full_class) -> None:
        self.mapper_name = mapper_class
        self.full_name = full_class
        pass

    def __repr__(self) -> str:
        return f"< {self.__class__.__name__}: {self.mapper_name} >"

class method:
    "method"
    method_regex = r'(method_[1-9]\d*)'
    
    # def __init__(self, mapper_method, full_method, return_class) -> None:
    def __init__(self, mapper_method, full_method) -> None:
        self.mapper_name = mapper_method
        self.full_name = full_method
        # self.return_class = return_class

    def __repr__(self) -> str:
        return f"< {self.__class__.__name__}: {self.mapper_name} >"
    

class field:
    "field"
    field_regex = r'(field_[1-9]\d*)'
    
    def __init__(self, mapper_fields, full_fields) -> None:
        self.mapper_name = mapper_fields
        self.full_name = full_fields

    def __repr__(self) -> str:
        return f"< {self.__class__.__name__}: {self.mapper_name} >"

class Mapper:
    def __init__(self, map_parser, parser) -> None:
        self.map: dict[str, mclass] = map_parser
        self.parser: "Dict[mclass, List[method | field]]" = parser



class ParserMapper:

    @staticmethod
    def parser(file: str) -> Mapper:
        mapper: "dict[mclass, list[method | field]]" = {}
        data = '\n'.join( open(file, 'r', encoding='utf-8').readlines()[1:] )
        m_class: mclass

        for line in data.split("\n"):
            line = line.replace("/", ".").replace("$", ".")

            split_line = line.split('\t')

            if len(split_line) <= 1:
                continue

            if split_line[0] == "c":
                m_class = mclass(split_line[1], split_line[2])
                # if split_line[1].find("$") != -1:
                if split_line[1].split(".")[-2] != "minecraft":
                    own_class = ".".join(split_line[1].split(".")[:-1])
                    for _mclass in mapper.keys():
                        if own_class == _mclass:
                            _mclass.children.append(m_class)
                            break
                mapper[m_class] = []
            
            elif split_line[1] == "f":
                mapper[m_class].append(
                    field(split_line[3], split_line[4])
                )
            elif split_line[1] == "m":
                # mapper_name = split_line[2].split(")L")
                # if len( mapper_name ) == 1:
                #     mapper_name = None
                # elif len(mapper_name) >= 2:
                #     mapper_name = mapper_name[-1].replace(";", "")
                mapper[m_class].append(
                    # method(split_line[3], split_line[4], mapper_name)
                    method(split_line[3], split_line[4])
                )

        # for _class in mapper:
        #     for is_method in mapper[_class]:
        #         if isinstance(is_method, method):
        #             rc: str = is_method.return_class
        #             is_method.return_class = None
        #             for x in mapper:
        #                 if rc == x.mapper_name:
        #                     is_method.return_class = x
        #                     break
        #             # else:
        #             #     break
                
        return Mapper( {_mclass.mapper_name : _mclass for _mclass in mapper}, mapper)