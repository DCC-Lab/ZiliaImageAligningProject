import time

class TimeOut:

    def __init__(self, func, timeOut):
        self.timeOut = timeOut
        self.func = func

    def __call__(self, *funcargs, **funckwargs):
        startTime = time.time()
        go = True
        while go:
            actualTime = time.time()
            if actualTime - startTime > self.timeOut:
                raise RuntimeError("The function took too long to return something.")
            elif func(*funcargs, **funckwargs) is not None:
                break
            else:
                continue



# @TimeOut(timeOut=120)
# def 