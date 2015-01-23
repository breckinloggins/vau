__author__ = 'bloggins'


class Env(dict):
    """An environment: a dict of {'var': val} pairs, with an outer Env"""
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def __setitem__(self, key, value):
        # NOTE: not perfect
        if key == '_':
            return

        super(Env, self).__setitem__(key, value)

    def find(self, var):
        """Find the innermost Env where var appears"""
        if var in self:
            return self
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            return None


def standard_env():
    """An environment with some vau standard procedures"""
    env = Env()

    # TODO: Expose host environment and do these within vau
    #env.update(vars(math))
    # env.update({
    #     '@op-add': op.add,
    #     '@op-sub': op.sub,
    #     '@op-mul': op.mul,
    #     '@op-div': op.div,
    #     '@op-gt': op.gt,
    #     '@op-lt': op.lt,
    #     '@op-ge': op.ge,
    #     '@op-le': op.le,
    #     '@op-eq': op.eq,
    #     '@append': op.add,
    # })
    return env


global_env = standard_env()
current_env = global_env
syntax_forms = []
