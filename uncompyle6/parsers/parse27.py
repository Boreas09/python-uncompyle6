#  Copyright (c) 2016 Rocky Bernstein
#  Copyright (c) 2005 by Dan Pascu <dan@windowmaker.org>
#  Copyright (c) 2000-2002 by hartmut Goebel <hartmut@goebel.noris.de>

from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parser import PythonParserSingle
from uncompyle6.parsers.parse2 import Python2Parser

class Python27Parser(Python2Parser):

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python27Parser, self).__init__(debug_parser)
        self.customized = {}

    def p_comprehension27(self, args):
        """
        list_for ::= expr _for designator list_iter JUMP_BACK

        setcomp_func ::= BUILD_SET_0 LOAD_FAST FOR_ITER designator comp_iter
                JUMP_BACK RETURN_VALUE RETURN_LAST

        dict_comp_body ::= expr expr MAP_ADD
        set_comp_body ::= expr SET_ADD

        # See also common Python p_list_comprehension
        """

    def p_try27(self, args):
        """
        try_middle   ::= JUMP_FORWARD COME_FROM except_stmts
                         END_FINALLY COME_FROM
        try_middle   ::= jmp_abs COME_FROM except_stmts
                         END_FINALLY

        tryelsestmt    ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                           try_middle else_suite COME_FROM

        except_cond1 ::= DUP_TOP expr COMPARE_OP
                         jmp_false POP_TOP POP_TOP POP_TOP

        except_cond2 ::= DUP_TOP expr COMPARE_OP
                         jmp_false POP_TOP designator POP_TOP
        """

    def p_jump27(self, args):
        """
        _ifstmts_jump ::= c_stmts_opt JUMP_FORWARD COME_FROM
        jmp_false ::= POP_JUMP_IF_FALSE
        jmp_true  ::= POP_JUMP_IF_TRUE
        bp_come_from    ::= POP_BLOCK COME_FROM
        """


    def p_stmt27(self, args):
        """
        # assert condition
        assert        ::= assert_expr jmp_true LOAD_ASSERT RAISE_VARARGS_1

        # assert condition, expr
        assert2       ::= assert_expr jmp_true LOAD_ASSERT expr RAISE_VARARGS_2

        withstmt ::= expr SETUP_WITH POP_TOP suite_stmts_opt
                POP_BLOCK LOAD_CONST COME_FROM
                WITH_CLEANUP END_FINALLY

        withasstmt ::= expr SETUP_WITH designator suite_stmts_opt
                POP_BLOCK LOAD_CONST COME_FROM
                WITH_CLEANUP END_FINALLY

        while1stmt ::= SETUP_LOOP l_stmts_opt JUMP_BACK POP_BLOCK COME_FROM

        # Common with 2.6
        while1stmt ::= SETUP_LOOP return_stmts bp_come_from
        while1stmt ::= SETUP_LOOP return_stmts COME_FROM
        """

class Python27ParserSingle(Python27Parser, PythonParserSingle):
    pass

if __name__ == '__main__':
    # Check grammar
    p = Python27Parser()
    p.checkGrammar()
    from uncompyle6 import PYTHON_VERSION, IS_PYPY
    if PYTHON_VERSION == 2.7:
        lhs, rhs, tokens, right_recursive = p.checkSets()
        from uncompyle6.scanner import get_scanner
        s = get_scanner(PYTHON_VERSION, IS_PYPY)
        opcode_set = set(s.opc.opname).union(set(
            """JUMP_BACK CONTINUE RETURN_END_IF COME_FROM
               LOAD_GENEXPR LOAD_ASSERT LOAD_SETCOMP LOAD_DICTCOMP
               LAMBDA_MARKER RETURN_LAST
            """.split()))
        remain_tokens = set(tokens) - opcode_set
        import re
        remain_tokens = set([re.sub('_\d+$','', t) for t in remain_tokens])
        remain_tokens = set([re.sub('_CONT$','', t) for t in remain_tokens])
        remain_tokens = set(remain_tokens) - opcode_set
        print(remain_tokens)
        # p.dumpGrammar()
