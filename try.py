class IllyScriptInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.current_state = 'START'

    def run(self, code):
        lines = code.split('\n')
        for line in lines:
            line = line.strip().lower()

            if line.startswith('print'):
                self.print_statement(line[6:])
            elif '=' in line:
                self.assign_variable(line)
            elif line.startswith('fun'):
                self.define_function(lines, lines.index(line))
            elif line.startswith('call'):
                self.call_function(line[5:])
            elif line.startswith('help'):
                self.show_help()
            elif line.startswith('if'):
                self.handle_condition(line)
            elif line.startswith('for'):
                self.handle_for_loop(line[4:])

    def print_statement(self, statement):
        if statement.startswith('"') and statement.endswith('"'):
            print(statement.strip('"'))
        else:
            try:
                result = str(eval(statement, {}, self.variables))
                print(result)
            except (NameError, SyntaxError):
                print("Silly Error: Unknown expression or variable!")

    def assign_variable(self, line):
        var_name, value = map(lambda x: x.strip(), line.split('='))
        try:
            self.variables[var_name] = eval(value, {}, self.variables)
        except (NameError, SyntaxError):
            self.variables[var_name] = value

    def define_function(self, lines, index):
        func_line = lines[index]
        func_name = func_line.split('(')[0].split()[1]
        params = func_line.split('(')[1].split(')')[0].split(',')
        body = '\n'.join(lines[index + 1:]).lower()
        self.functions[func_name] = {
            'params': params,
            'body': body
        }

    def call_function(self, func_call):
        func_name, args = func_call.split('(')
        args = args.rstrip(')').split(',')
        if func_name in self.functions:
            func = self.functions[func_name]
            if len(args) == len(func['params']):
                local_vars = {param: arg.strip() for param, arg in zip(func['params'], args)}
                self.variables.update(local_vars)
                self.run(func['body'])
            else:
                print(f"Silly Error: Incorrect number of arguments for function '{func_name}'!")
        else:
            print(f"Silly Error: Function '{func_name}' is not defined!")

    def show_help(self):
        print("Available commands:")
        print("- print <expression>")
        print("- <variable_name> = <value>")
        print("- fun <function_name>(<parameters>):")
        print("    <function_body>")
        print("- call <function_name>(<arguments>)")
        print("- help")
        print("- if <condition>")
        print("    <body>")
        print("endif")
        print("- for <variable> in range(start, end[, step]):")
        print("    <body>")
        print("endfor")

    def handle_condition(self, condition):
        condition = condition[3:]
        if '==' in condition:
            left, right = map(lambda x: x.strip(), condition.split('=='))
            if left in self.variables and right in self.variables:
                if self.variables[left] == self.variables[right]:
                    self.run_body()

    def run_body(self):
        pass  # Placeholder for executing the body of a conditional statement

    def handle_for_loop(self, loop_statement):
        loop_var, loop_range = map(lambda x: x.strip(), loop_statement.split(' in '))
        loop_var = loop_var.strip()
        if 'range' in loop_range:
            loop_range = loop_range[6:].rstrip('):')
            range_args = list(map(int, loop_range.split(',')))
            if len(range_args) == 1:
                start, end, step = 0, range_args[0], 1
            elif len(range_args) == 2:
                start, end, step = range_args[0], range_args[1], 1
            elif len(range_args) == 3:
                start, end, step = range_args
            else:
                print("Silly Error: Incorrect range arguments in for loop!")
                return

            for i in range(start, end, step):
                self.variables[loop_var] = i
                self.run_body()

# Example usage:
interpreter = IllyScriptInterpreter()
interpreter.run(input('write code: '))
