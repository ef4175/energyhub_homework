import unittest

from echo import cartesian_product, parse


class CartesianProductUnitTests(unittest.TestCase):
    def test_string_with_string(self):
        left = 'a'
        right = 'b'
        expected = ['ab']
        self.assertEqual(cartesian_product(left, right), expected)

    def test_string_with_list(self):
        left = 'a'
        right = ['b', 'c']
        expected = ['ab', 'ac']
        self.assertEqual(cartesian_product(left, right), expected)

    def test_list_with_string(self):
        left = ['a', 'b']
        right = 'c'
        expected = ['ac', 'bc']
        self.assertEqual(cartesian_product(left, right), expected)

    def test_list_with_list(self):
        left = ['a', 'b']
        right = ['c', 'd']
        expected = ['ac', 'ad', 'bc', 'bd']
        self.assertEqual(cartesian_product(left, right), expected)


class ParseUnitTests(unittest.TestCase):
    def test_expr_without_braces(self):
        expr = 'foo'
        expected = 'foo'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_one_set_of_braces_with_no_trailing_characters(self):
        expr = 'foo{bar,baz}'
        expected = 'foobar foobaz'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_one_set_of_braces_with_trailing_characters(self):
        expr = 'foo{bar,baz}qux'
        expected = 'foobarqux foobazqux'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_nested_braces(self):
        expr = 'this{foo,bar{baz,qux}}'
        expected = 'thisfoo thisbarbaz thisbarqux'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_multiple_unnested_braces(self):
        expr = 'a{b,c}d{e,f,g}hi'
        expected = 'abdehi abdfhi abdghi acdehi acdfhi acdghi'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_nested_and_unnested_braces(self):
        expr = 'a{b,c{d,e,f}g,h}ij{k,l}'
        expected = 'abijk abijl acdgijk acdgijl acegijk acegijl acfgijk acfgijl ahijk ahijl'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_deeply_nested_braces(self):
        expr = 'a{b,c{d,e{f,g{h,i{j,k{l,m}}}}}}'
        expected = 'ab acd acef acegh acegij acegikl acegikm'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_braces_in_front(self):
        expr = '{foo,bar}baz'
        expected = 'foobaz barbaz'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_surrounding_braces(self):
        expr = '{a,b}c{d,e}'
        expected = 'acd ace bcd bce'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_braces_only(self):
        expr = '{a,b}{c,d}{f,g}'
        expected = 'acf acg adf adg bcf bcg bdf bdg'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_braces_without_comma(self):
        expr = 'foo{bar.baz}qux'
        expected = 'foo{bar.baz}qux'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_empty_braces(self):
        expr = 'foo{}bar'
        expected = 'foo{}bar'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_empty_and_nonempty_braces(self):
        expr = 'a{}b{c,d}e{}f'
        expected = 'a{}bce{}f a{}bde{}f'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_opening_braces_in_front(self):
        expr = '{{{foo'
        expected = '{{{foo'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_closing_braces_in_front(self):
        expr = '}}}foo'
        expected = '}}}foo'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_opening_braces_at_end(self):
        expr = 'foo{{{'
        expected = 'foo{{{'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_closing_braces_at_end(self):
        expr = 'foo}}}'
        expected = 'foo}}}'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_invalid_surrounding_braces(self):
        expr = '}}}foo{{{'
        expected = '}}}foo{{{'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_empty_string_between_commas_in_braces(self):
        expr = 'foo{,}bar'
        expected = 'foobar foobar'
        self.assertEqual(parse(expr), expected)

    def test_expr_with_empty_string_and_word_between_commas_in_braces(self):
        expr = 'foo{,bar,}baz'
        expected = 'foobaz foobarbaz foobaz'
        self.assertEqual(parse(expr), expected)
