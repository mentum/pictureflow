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
