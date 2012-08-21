import sys
import linecache
import inspect

def traceit(frame, event, arg):
    global depth
    global counter
    global f
    # print event, frame, arg
    # print inspect.getframeinfo(frame)
    # print '\n'
    # for attr in [x for x in dir(frame) if not callable(getattr(frame, x))]:
    #     print attr, getattr(frame, attr)
    # for func in [x for x in dir(frame) if callable(getattr(frame, x))]:
    #     code = 'frame.' + func
    #     print func, eval(code) # note we are not actually calling the function
    # print '\n'
    if event == 'line':
        linenum = frame.f_lineno
        linetext = linecache.getline('recursionexplorer.py', linenum)
        f.write('    '*depth+linetext)
        print 'line', linenum, linetext
    if event == 'call':
        print inspect.getframeinfo(frame)
        _, _, function, _, _ = inspect.getframeinfo(frame)
        if function == 'example':
            depth += 1 
    print "Function calls: ", depth
    counter += 1


    return traceit


def example(array):
    if len(array) == 0:
        return
    array.pop()
    example(array)



def main():
    example(range(10))


sys.settrace(traceit)
depth = 0
counter = 0 

if __name__ == '__main__':
    f = open('example_function.txt', 'w')
    main()
    print "Trace function executed %s times" %(counter)
    f.close()

