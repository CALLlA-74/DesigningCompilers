from enum import unique, Enum


@unique
class Scopes(str, Enum):
    LABELS = "labels"
    CONSTS = "consts"
    VARS = "vars"
    PROCEDURES = "procedures"
    FUNCTIONS = "functions"
    RECORDS = "records"
    TYPES = "types"


@unique
class TypesEnum(str, Enum):
    STRING = "string"
    #STRING_LITERAL = "string_literal"
    CHAR = "char"
    #CHAR_LITERAL = "char_literal"
    INTEGER = "integer"
    #INT_LITERAL = "int_literal"
    REAL = "real"
    #REAL_LITERAL = "real_literal"
    BOOLEAN = "boolean"
    #BOOLEAN_LITERAL = "boolean_literal"
    IDENTIFIER = "identifier"
    SIGNED_IDENTIFIER = "signed_identifier"


@unique
class EmbeddedTypesEnum(str, Enum):
    IDENTIFIER = "identifier"
    SUBRANGE = "subrange"
    ARRAY = "array"
    FIXEDSTRING = "fixedstring"
    RECORD = "record"
    POINTER = "pointer"
    PROCEDURE = "procedure"
    FUNCTION = "function"


