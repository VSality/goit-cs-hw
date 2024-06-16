from lexer import TokenType
from parser import BinOp


class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if isinstance(node, BinOp):
            if node.op.type == TokenType.PLUS:
                return self.visit(node.left) + self.visit(node.right)
            elif node.op.type == TokenType.MINUS:
                return self.visit(node.left) - self.visit(node.right)
            elif node.op.type == TokenType.MUL:
                return self.visit(node.left) * self.visit(node.right)
            elif node.op.type == TokenType.DIV:
                return self.visit(node.left) / self.visit(node.right)
        elif isinstance(node, Num):
            return node.value
     

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"Немає методу visit_{type(node).__name__}")


