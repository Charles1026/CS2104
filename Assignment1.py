import re

'''
Objective
Your task is to implement a parser for a subset of the Scheme programming language. You will be given a template that includes a basic lexer and parser structure. Your goal is to complete the template to create a working parser that can handle the language defined by the given grammar.

You are allowed to use A.I. tools to complete this assignment. You are expected to be able to explain all aspects of your solution during the tutorial in Week 3.

Template
Below is the Python template you will be working with. Some parts are already implemented, and you need to complete the rest:

'''

def scheme_lexer(code):
    # Define regex patterns
    patterns = [
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('NAME', r'[a-zA-Z+\*\/=\-<>][a-zA-Z0-9+\*\/=\-<>]*'),
        ('NUMBER', r'\d+(\.\d+)?'),
        ('WHITESPACE', r'\s+')
    ]
    
    # Combine patterns
    regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
    
    # Tokenize
    tokens = []
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind != 'WHITESPACE':
            tokens.append((kind, value))
    
    return tokens

# parser

class SchemeParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        expressions = []
        while self.current < len(self.tokens):
            expressions.append(self.parse_expression())
        return ('program', expressions)

    def parse_expression(self):
        if self.current >= len(self.tokens):
            return None
        
        token = self.tokens[self.current]
        
        # List
        if token[0] == 'LPAREN':
            return self.parse_list()
        
        # Atomic
        elif token[0] == 'NUMBER':
            self.current += 1
            return ('number', float(token[1]))
        
        elif token[0] == 'NAME':
            self.current += 1
            return ('symbol', token[1])
      
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_list(self):
        self.current += 1  # Skip LPAREN
        elements = []
        
        while self.current < len(self.tokens) and self.tokens[self.current][0] != 'RPAREN':
            elements.append(self.parse_expression())
        
        if self.current >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        
        self.current += 1  # Skip RPAREN
        
        # If no elements, is empty list
        if not elements:
            return ('list', [])
                
        # Define
        elif elements[0][1] == 'define':
            # Ensure min size of define statement
            if len(elements) < 3: 
                raise SyntaxError("Unexpected end of define")
              
            # Define Var
            if elements[1][0] == "symbol" or elements[1][0] == "number":
                return ('define', elements[1:])
            
            # Define Func
            if elements[1][0] == "list":
                return ('define-func', elements[1:])
        
        # If
        elif elements[0][1] == 'if':
            if len(elements) != 4: # 4 as (if exp exp exp)
                raise SyntaxError("Invalid if syntax")
          
            return ('if', elements[1:])
        
        # if first elem not define or if, it is a list
        return ('list', elements)

def print_ast(node, indent=0):
    if isinstance(node, tuple):
        if node[0] == 'program':
            print('program')
            for expr in node[1]:
                print_ast(expr, indent + 1)
        elif node[0] in ('define', 'define-func', 'if'):
            print('  ' * indent + node[0])
            for child in node[1:]:
                print_ast(child, indent + 1)
        elif node[0] == 'list':
            print('  ' * indent + 'list')
            for element in node[1]:
                print_ast(element, indent + 1)
        else:
            print('  ' * indent + f"{node[0]}: {node[1]}")
    elif isinstance(node, list):
        for item in node:
            print_ast(item, indent)
    else:
        print('  ' * indent + str(node))

# Testing the template

scheme_code_1 = '''
(()()())
'''

scheme_code_2 = '''
(define first car)
(define second cadr)

(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))
'''

scheme_code_3 = '''
(define (max a b)
  (if (> a b)
      a
      b))
'''

# scheme_code_4 = '''
# ...
# '''

# scheme_code_5 = '''
# ...
# '''

CODE_SNIPPET = scheme_code_2

# Test the template
tokens = scheme_lexer(CODE_SNIPPET)

for token in tokens:
    print(token)

# Running a test
tokens = scheme_lexer(CODE_SNIPPET)
parser = SchemeParser(tokens)
ast = parser.parse()

print_ast(ast)

'''
Grammar

Here's the context-free grammar for the subset of Scheme that your parser should handle:

<program> ::= <expression>*

<expression> ::= <atomic> | <list> | <define> | <if>

<atomic> ::= <number> | <symbol>

<list> ::= "(" <expression>* ")"

<define> ::= "(" "define" <variable> <expression> ")" | "(" "define" "(" <symbol> <variable>* ")" <expression>+ ")"

<if> ::= "(" "if" <expression> <expression> <expression> ")"

<variable> ::= <symbol>

<number> ::= A sequence of digits, optionally followed by a decimal point and another sequence of digits

<symbol> ::= A sequence of characters that starts with a letter or certain special characters, followed by letters, digits, or certain special characters

<string> ::= '"' [^"]* '"'

As "certain special characters" we allow +, *, -, /, =, <, >.
'''

'''
Tasks
1. Complete the scheme_lexer function:
  Implement the regex pattern for NAME tokens. Remember to include all allowed special characters for Scheme symbols.
  Implement the regex pattern for NUMBER tokens, handling both integers and floating-point numbers.
  
2. Analyze the print_ast function and write a specification that describes how syntax trees of the Scheme sublanguage are represented.

3. Extend the SchemeParser class to handle special forms:
  Implement parsing for define expressions (both variable and function definitions).
  Implement parsing for if expressions.
  Update the parse_list method to recognize these special forms.
  Do not change the function print_ast.
  
4. Test your parser with various Scheme expressions.
  (Optional) Extend the parser to handle additional Scheme constructs not included in the original grammar (e.g., let, lambda, cond).
'''

'''
By analyzing the function print_ast and the given context-free grammar,
you can infer the structure of the abstract syntax trees that need to
be generated by the parser. Describe the structure of these abstract
syntax trees clearly in English or in any other suitable formalism.

The root node of an ast should be a <program>, which contains zero or more <expression>. Each expression is either an <atomic>, <list>, <define> or <if>.

An <atomic> is either a <number>, integer or floating point, or a <symbol> which is in essence a name, staring with an alphabet or a certain special character(CSC) followed by alphabets, digits and/or CSCs.

A <list> is zero or more <expression> enclosed by () brackets.

A <define> is enclosed by () brackets and starts with the text "define". It is followed by a one more more <variable>(which is a <symbol>) and then one or more <expression>. 
If there are more than one <symbol>, they have to be enclosed by () brackets.

An <if> is enclosed by () brackets and starts with the text "if". It is then followed by 3 <expression>.

'''

'''
Reflection: Write a brief (1-2 paragraphs) reflection on the challenges
you faced and what you learned from this assignment. If you used LLMs,
write down which system you used, and summarize how you prompted the system.

<your reflection goes here>
'''