from decimal import Decimal, getcontext, InvalidOperation
import math
from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    PAREN_LEFT = auto()
    PAREN_RIGHT = auto()

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

def validate_expression(expression):
    """Validate the expression contains only allowed characters"""
    allowed_chars = set("0123456789+-*/.() ")
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Invalid characters in expression")

def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        c = expression[i]
        if c.isspace():
            i += 1
            continue
            
        # Handle negative numbers
        if c == '-' and (i == 0 or 
                        (tokens and tokens[-1].type in [TokenType.OPERATOR, TokenType.PAREN_LEFT])):
            i += 1
            if i >= len(expression):
                raise ValueError("Incomplete negative number")
                
            num_str = ['-']
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num_str.append(expression[i])
                i += 1
            if len(num_str) == 1:
                raise ValueError("Incomplete negative number")
            tokens.append(Token(TokenType.NUMBER, ''.join(num_str)))
            continue
            
        if c.isdigit() or c == '.':
            num_str = []
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num_str.append(expression[i])
                i += 1
            tokens.append(Token(TokenType.NUMBER, ''.join(num_str)))
        elif c in '+-*/':
            tokens.append(Token(TokenType.OPERATOR, c))
            i += 1
        elif c == '(':
            tokens.append(Token(TokenType.PAREN_LEFT, c))
            i += 1
        elif c == ')':
            tokens.append(Token(TokenType.PAREN_RIGHT, c))
            i += 1
        else:
            # This should never be reached because of validate_expression
            raise ValueError(f"Invalid character: {c}")
    return tokens

def shunting_yard(tokens):
    output = []
    operators = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    for token in tokens:
        if token.type == TokenType.NUMBER:
            output.append(token)
        elif token.type == TokenType.OPERATOR:
            while (operators and operators[-1].type == TokenType.OPERATOR and
                   precedence[operators[-1].value] >= precedence[token.value]):
                output.append(operators.pop())
            operators.append(token)
        elif token.type == TokenType.PAREN_LEFT:
            operators.append(token)
        elif token.type == TokenType.PAREN_RIGHT:
            while operators and operators[-1].type != TokenType.PAREN_LEFT:
                output.append(operators.pop())
            if not operators:
                raise ValueError("Mismatched parentheses")
            operators.pop()  # Remove the left parenthesis
    
    while operators:
        if operators[-1].type == TokenType.PAREN_LEFT:
            raise ValueError("Mismatched parentheses")
        output.append(operators.pop())
    
    return output

def evaluate_rpn(tokens):
    stack = []
    for token in tokens:
        if token.type == TokenType.NUMBER:
            stack.append(Decimal(token.value))
        elif token.type == TokenType.OPERATOR:
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            b = stack.pop()
            a = stack.pop()
            if token.value == '+':
                stack.append(a + b)
            elif token.value == '-':
                stack.append(a - b)
            elif token.value == '*':
                stack.append(a * b)
            elif token.value == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.append(a / b)
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]

def calculate(expression):
    """
    Evaluate a mathematical expression with precise decimal handling
    Args:
        expression (str): Mathematical expression to evaluate
    Returns:
        int/float: Result of the calculation
    Raises:
        ValueError: For invalid characters or empty input
        SyntaxError: For invalid syntax
        ZeroDivisionError: For division by zero
    """
    if not expression or not expression.strip():
        raise ValueError("Empty expression")

    # Validate characters first
    validate_expression(expression)

    # Set sufficient precision for large numbers
    getcontext().prec = 28  # Increased precision for very large numbers

    try:
        tokens = tokenize(expression)
        rpn = shunting_yard(tokens)
        decimal_result = evaluate_rpn(rpn)
        
        # Convert to appropriate type while maintaining precision
        if decimal_result == decimal_result.to_integral_value():
            int_result = int(decimal_result)
            # For very large numbers that fit in Python int, return int
            if abs(int_result) < 2**63:  # Within standard Python int range
                return int_result
            return decimal_result  # Return Decimal for huge integers
        else:
            # For floating point results, return the most appropriate type
            float_result = float(decimal_result)
            if math.isclose(float_result, decimal_result, rel_tol=1e-15):
                return float_result
            return decimal_result
    
    except ZeroDivisionError:
        raise ZeroDivisionError("Division by zero")
    except (ValueError, InvalidOperation, IndexError) as e:
        raise SyntaxError(f"Invalid expression: {str(e)}")