import inspect


class Debug:
    allowed = ['default','debug','warning','error'] + ["casestudy", "vis"]
    last_context = None

    @classmethod
    def print(cls, *args, label="default", depth=1, **kw):
        if label.lower() in Debug.allowed:
            last_call = inspect.stack()[depth]
            file_name = last_call.filename.split("\\")[-1]

            if label.lower() == "warning":
                if cls.last_context != last_call.function:
                    print()
                    print("================================")
                    cls.last_context = last_call.function
                w_txt = f"Warning, {last_call.function}() at {file_name}, line {last_call.lineno}: "
                print(w_txt)
                print(' ' * (len(w_txt) + 1), *args, **kw)
            else:
                if cls.last_context != last_call.function:
                    if cls.last_context == "warning":
                        print("================================")
                    print()
                    cls.last_context = last_call.function
                print(f'({label}, {last_call.function}() at {file_name}, line {last_call.lineno}):', *args, **kw)

    @classmethod
    def labeld_print(cls, label: str):
        def lprint(*args, **kw):
            return Debug.print(*args, label=label, depth=2, **kw)
        return lprint