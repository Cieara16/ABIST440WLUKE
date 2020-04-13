import time
#this is a template for how to calculate time
#pieces of this code should be placed until the brewing process
#you want to calculate to calculate the time

#estimate time left by giving percentages of how far through the process you are
n = 10000
t0 = time.time()
for i in range(n):
    t1 = time.time()
    print("Processing file {} ({}%)".format(i, 100*i//n), end="")
    INSERT-NAME-OF-FILE-BEING-PROCESSED(i)
    t2 = time.time()
    print(" {}s (total: {}s)".format(t2-t1, t2-t0))

#calc time for all brewing processes
def allbrewingprocesses(process=0):
    if process == 0:
        start = time.time()
        duration = time.time() - start
        print(f'took {duration:.2f}s')
#calc time for process 1
def brewingprocess1(process=1):
    if process == 1:
        start = time.time()
        duration = time.time() - start
        print(f'took {duration:.2f}s')

#calc time for process 2
def brewingprocess2(process=2):
    if process == 2:
        start = time.time()
        duration = time.time() - start
        print(f'took {duration:.2f}s')

#calc time for process 3
def brewingprocess3(process=3):
    if process == 3:
        start = time.time()
        duration = time.time() - start
        print(f'took {duration:.2f}s')
