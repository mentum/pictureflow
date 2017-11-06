from copy import deepcopy


class PlaceholderGenerator(object):

    def __init__(self, vals):
        self.values = vals
        self._iterator = self._get_iterator()

    def _get_iterator(self):
        try:
            for val in self.values:
                yield deepcopy(val)

        except TypeError:
            # not iterable
            while True:
                yield deepcopy(self.values)

    def reset(self):
        pass

    def __iter__(self):
        return self._iterator

    def __next__(self):
        return next(self._iterator)


class SessionWrapper(object):

    """
    Session object used to execute transformation graphs. Do not instantiate directly, instead get one via
    a :py:class:`Session` context manager.

    Args:
        ctx: Placeholder context
    """

    def __init__(self, ctx):
        self._ctx = ctx

    def run(self, graph):
        """
        Do a lazy run of a transformation graph

        Args:
            graph (Node): Graph to execute

        Returns:
            iterator: Results iterator

        """

        for placeholder, values in self._ctx.items():
            # TODO: Check for iterable dimensions
            placeholder.parents = [PlaceholderGenerator(values)]

        graph.reset()

        for itm in graph:
            yield itm

        # Unregister ctx from graph
        for placeholder in self._ctx:
            placeholder.parents = []


    def run_sync(self, graph):
        """
        Do a synchronous run of a transformation graph.

        Args:
            graph (Node): Graph to execute

        Returns:
            list: List of results

        """
        out = []

        for itm in self.run(graph):
            out.append(itm)

        return out


class Session(object):

    """
    :py:class:`Session` is a context manager tasked with attaching and detaching a provided context to one (or multiple)
    transformation graph(s).

    Args:
        feed_dict (:code:`{Node: [values]}`): Dictionary providing context mapping
    """

    def __init__(self, feed_dict):
        self._ctx = feed_dict

    def __enter__(self):
        """
        Returns:
            SessionWrapper: Session object used to execute transformation graphs

        """
        return SessionWrapper(self._ctx)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
