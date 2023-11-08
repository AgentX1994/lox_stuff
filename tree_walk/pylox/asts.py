from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from .scanner import Token

R = TypeVar('R')

class Visitor(ABC, Generic[R]):
    @abstractmethod
    def visit_binary(self, expression: 'BinaryExpression') -> R:
        ...
    
    @abstractmethod
    def visit_unary(self, expression: 'UnaryExpression') -> R:
        ...

    @abstractmethod
    def visit_literal(self, expression: 'LiteralExpression') -> R:
        ...

    @abstractmethod
    def visit_grouping(self, expression: 'GroupingExpression') -> R:
        ...

class Expression(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor[R]) -> R:
        ...

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_binary(self)

@dataclass
class UnaryExpression(Expression):
    operator: Token
    right: Expression

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_unary(self)

@dataclass
class LiteralExpression(Expression):
    value: Any

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_literal(self)

@dataclass
class GroupingExpression(Expression):
    expression: Expression

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_grouping(self)