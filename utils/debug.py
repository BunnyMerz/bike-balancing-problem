import inspect


class Debug:
    allowed = ['default','debug','warning','error'] + ["CaseStudy"]
    last_context = None

    @classmethod
    def print(cls, *args, label="default", depth=1, **kw):
        if label in Debug.allowed:
            last_call = inspect.stack()[depth]
            file_name = last_call.filename.split("\\")[-1]

            if cls.last_context != last_call.function:
                print()
                cls.last_context = last_call.function
            print(f'({label}, {last_call.function}() at {file_name}, line {last_call.lineno}):', *args, **kw)

    @classmethod
    def labeld_print(cls, label: str):
        def lprint(*args, **kw):
            return Debug.print(*args, label=label, depth=2, **kw)
        return lprint