# Pylox (tree-walk interpreter)
A Python port of the "jlox" Java interpreter from the Crafting Interpreters book by Robert Nystrom.

Grammar rules: -

expression → literal
| unary
| binary
| grouping;

literal → NUMBER | STRING | "true" | "false" | "nil" ;

grouping → "(" expression ")" ;

unary → ( "-" | "!" ) expression ;

binary → expression operator expression ;

operator → "==" | "!=" | "<" | "<=" | ">" | ">="
| "+" | "-" | "*" | "/" ;