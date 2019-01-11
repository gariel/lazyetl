
import importlib
import pkgutil

definition = {}

def executionStep(key="", input={}, output={}):
    def decorator(clzz):
        if not hasattr(clzz, "execute"):
            raise Exception("Method 'execute' does not exists in Step Class " + clzz.name)

        nkey = key
        if not nkey:
            name = clzz.__name__
            nkey = name.endswith("Step") and name[:-4] or name

        fields = input.copy()
        fields.update(output)
        definition[nkey] = clzz

        clzz.__step_input__ = input
        clzz.__step_output__ = output
        clzz.__step_key__ = nkey

        init = clzz.__init__
        def executionStepInit(self, *args, **kwargs):
            for field, valuefunc in fields.items():
                setattr(self, field, valuefunc())
            init(self, *args, **kwargs)
        clzz.__init__ = executionStepInit
        return clzz
    return decorator

__all__ = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    importlib.import_module(__name__ + '.' + name)
    __all__.append(name)
