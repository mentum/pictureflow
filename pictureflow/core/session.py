class _SessionWrapper(object):

    def __init__(self, ctx):
        self._ctx = ctx

    def run(self, graph):
        def value_feed(vals):
            # Determine if vals is single-value or an iterable
            try:
                for val in vals:
                    yield val

            except TypeError:
                # not iterable
                while True:
                    yield vals

        for placeholder, values in self._ctx.items():
            # TODO: Check for iterable dimensions
            placeholder.parent = value_feed(values)

        for itm in graph:
            yield itm

        # Unregister ctx from graph
        for placeholder in self._ctx:
            placeholder.parent = None

    def run_sync(self, graph):
        out = []

        for itm in self.run(graph):
            out.append(itm)

        return out


class Session(object):

    def __init__(self, feed_dict):
        self._ctx = feed_dict

    def __enter__(self):
        return _SessionWrapper(self._ctx)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
