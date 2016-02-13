# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from pyparsing import *

from mysqlparse.grammar.data_type import data_type_syntax


#
# PARTIAL PARSERS
#

_nullable = CaselessKeyword("NOT NULL").setParseAction(replaceWith(False)) ^ CaselessKeyword("NULL").setParseAction(replaceWith(True))
_default = Suppress(CaselessKeyword("DEFAULT")) + Or([Word(nums), QuotedString("'")]).setName("default").setResultsName("default")
_auto_increment = CaselessKeyword("AUTO_INCREMENT").setResultsName("auto_increment").setParseAction(replaceWith(True))
_index_type = Or([
    (CaselessKeyword("UNIQUE") + Optional(CaselessKeyword("KEY"))).setParseAction(replaceWith("unique_key")),
    (Optional(CaselessKeyword("PRIMARY")) + CaselessKeyword("KEY")).setParseAction(replaceWith("primary_key"))
]).setResultsName("index_type")
_comment = CaselessKeyword("COMMENT") + Or([QuotedString("'"), QuotedString('"')]).setResultsName("comment")


#
# COLUMN DEFINITION SYNTAX
#
# Source: http://dev.mysql.com/doc/refman/5.7/en/create-table.html
#

column_definition_syntax = Forward()
column_definition_syntax <<= (
    data_type_syntax +
    Optional(_nullable).setResultsName("null") +
    Optional(_default) +
    Optional(_auto_increment) +
    Optional(_index_type) +
    Optional(_comment)
)    
