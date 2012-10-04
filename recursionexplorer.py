import sys
import linecache
import inspect

class Tracer(object):

    def __init__(self, file_out, functions, program):
        self.depth = 0
        self.counter = 0
        self.function = functions
        self.file_out = file_out
        self.program = program

    def traceit(self, frame, event, arg):
        print event, frame, arg
        print inspect.getframeinfo(frame)
        print '\n'
        if event == 'line':
            linenum = frame.f_lineno
            linetext = linecache.getline(self.program, linenum)
            self.file_out.write('    '*self.depth+linetext)
            print 'line', linenum, linetext
        if event == 'call':
            # print inspect.getframeinfo(frame)
            currentfunc = inspect.getframeinfo(frame)[2]
            if currentfunc in self.function:
                self.depth += 1 
        if event == 'return':
            self.depth -= 1
        # print "Function calls: ", depth
        self.counter += 1

        return self.traceit


def example(array, value):
    if len(array) == 0:
        return array, 0
    array.pop()
    example(array, value)
    value += 1
    return array, value

def trace_setup(filename, function, program):
    file_out = open(filename, 'w')
    
    trace_obj = Tracer(file_out, function, program)
    
    sys.settrace(trace_obj.traceit)

if __name__ == '__main__':
    program_name = __file__

    trace_setup('example_function.txt', ['example'], program_name)
    
    example(range(10),0)



