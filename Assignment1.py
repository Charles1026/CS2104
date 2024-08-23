import re

def scheme_lexer(code):
    # Define regex patterns
    patterns = [
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('NAME', r'[a-zA-Z+\-*\/=<>][a-zA-Z0-9+\-*\/=<>]*'),
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

# Test the template

# scheme_code = '(()()())'
# scheme_code = 'abc +add var1 a+b *multiply 123var 42 3.14 7. .5 10.5a 5..5'

# tokens = scheme_lexer(scheme_code)

# for token in tokens:
#     print(token)


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
        
        if token[0] == 'LPAREN':
            return self.parse_list()
        
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
        
        if not elements:
            return ('list', [])
        
        if elements[0] == ('symbol', 'define'):

            if len(elements) < 3:
                raise SyntaxError("Additional variables or expressions required")

            # define-func
            if elements[1][0] == 'list':
                list_elements = elements[1][1]

                if len(list_elements) == 0:
                    raise SyntaxError("Function signature cannot be empty")

                for parameter in list_elements:
                    if parameter[0] != 'symbol':
                        raise SyntaxError("Function signature have to be symbols")
                
                elements[0] = 'define-func'

                return tuple(elements)

            # define
            if elements[1][0] == 'symbol': 
                if len(elements) > 3:
                    raise SyntaxError("Only 1 expression can be assigned to variable.")
                elements[0] = 'define'

                return tuple(elements)
            
            if elements[1][0] == 'number':
                raise SyntaxError("Invalid data type for variable, it can not be a number. It has to be a symbol")
            
            raise SyntaxError("Place variable or function signature in paranthesis after 'define'")

        if elements[0] == ('symbol', 'if'):
            # must have 'if' and 3 more expressions
            if len(elements) != 4: 
                raise SyntaxError(f"Invalid number of expressions. Currently have {len(elements) - 1} expressions instead of 3")
            
            elements[0] = 'if'

            return tuple(elements)
        
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
(()()()) (a b c) ((a b) (c d)) ()
'''

scheme_code_2 = '''
42 3.14 abc 
'''

scheme_code_3 = '''
(define x 10) (define (add x y) (+ x y))
'''

scheme_code_4 = '''
(if (> x 0) x (- x)) (if (< y 5) (if (= y 2) 3 4) 5)
'''

scheme_code_5 = '''
123var (a b (a 1b@ c) (define 123x 10) (define (add x y) + x y)) (if (> x 0) x) (if (> x 0) x (- x)
'''

# Running a test
tokens_list = [scheme_lexer(scheme_code_1), scheme_lexer(scheme_code_2), 
          scheme_lexer(scheme_code_3), scheme_lexer(scheme_code_4), 
          scheme_lexer(scheme_code_5)]

for tokens in tokens_list:
    parser = SchemeParser(tokens)
    ast = parser.parse()

    print_ast(ast)

 

'''
By analyzing the function print_ast and the given context-free grammar,
you can infer the structure of the abstract syntax trees that need to
be generated by the parser. Describe the structure of these abstract
syntax trees clearly in English or in any other suitable formalism.

These abstract syntax trees always starts with a program that contains 
any number of expressions. If these expressions are atomic (numbers/symbols), 
that expression would be the final leaf. If the expression is non-atomic, 
such as 'list's as well as 'define' and 'if' statements, they would contain 
more expressions that would further branch out until it reaches the atomic 
expression. Each level of containment is expressed in the tree with 
indentations. As such, the program will be the root, with any expressions
contained in it having an identation of 2 spaces, and any expressions 
contained within subsequent expressions being further idented by 2 spaces.

For example, (()()()) would be parsed as a program containing 1 expression 
(a list). This list would contain 3 expressions (3 lists) that each contain 
nothing. Therefore, 'program' has no identation, the overarching list has 
1 identation, and the lists within this overarching list are all further
idented by 2 spaces.
'''

'''
Reflection: Write a brief (1-2 paragraphs) reflection on the challenges
you faced and what you learned from this assignment. If you used LLMs,
write down which system you used, and summarize how you prompted the system.

Understanding Regex was difficult at first but after explaining the specifications
of what a symbol and number were to ChatGPT, I was able to easily get the Regex and
understand how it worked. I learnt more about the existence of characters that
were specially used in regex, thus required a \ to make it literal.

Additionally, understanding the specific format of <define> and <if> was tedious at 
first. However, after understanding how the parse_list() function works, it was 
much easier to craft out the specific cases for define, define-func and if.


I used ChatGPT and I provided it information on the task given to us, specifically 
the Regex already provided to us and the grammar rules. I then asked it to provide
good test cases for me to try out on my code.
'''