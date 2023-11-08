
from .asts import BinaryExpression, Expression, GroupingExpression, LiteralExpression, UnaryExpression, Visitor

class DebugAstPrinter(Visitor[str]):
    def print(self, expression: Expression) -> str:
        return expression.accept(self)

    def visit_binary(self, expression: BinaryExpression) -> str:
        return self._parenthesize(expression.operator.lexeme, expression.left, expression.right)
    
    def visit_unary(self, expression: UnaryExpression) -> str:
        return self._parenthesize(expression.operator.lexeme, expression.right)

    def visit_literal(self, expression: LiteralExpression) -> str:
        if expression.value is None:
            return 'nil'
        else:
            return str(expression.value)

    def visit_grouping(self, expression: GroupingExpression) -> str:
        return self._parenthesize('group', expression.expression)

    def _parenthesize(self, name: str, *items: Expression) -> str:
        items_str = ' '.join(item.accept(self) for item in items)
        return f'({name} {items_str})'