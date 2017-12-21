from copy import deepcopy

from queue import Queue

import pictureflow as pf


class _PlaceholderGenerator(object):

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
        ctx (dict): Placeholder context
    """

    _EXCLUDED_DEBUG_NODES = []

    def __init__(self, ctx):
        self._ctx = ctx

    @staticmethod
    def _attach_debug_outputs(graph):
        queue = Queue()
        queue.put(graph)

        while not queue.empty():
            node = queue.get()

            if hasattr(node, 'parents'):
                for i, parent in enumerate(node.parents):
                    if hasattr(parent, '_output_type') and parent._output_type == pf.Image:
                        disk = pf.output.DiskOutput(parent, pf.Constant('debug/'))
                        disk._debug = True
                        node.parents[i] = disk

                    queue.put(parent)

    @staticmethod
    def _detach_debug_outputs(graph):
        queue = Queue()
        queue.put(graph)

        while not queue.empty():
            node = queue.get()

            if hasattr(node, 'parents'):
                for i, parent in enumerate(node.parents):
                    if isinstance(parent, pf.output.DiskOutput) and hasattr(parent, '_debug'):
                        node.parents[i] = parent.parents[0]

                    queue.put(parent)

    def run(self, graph, debug=False):
        """
        Do a lazy run of a transformation graph

        Args:
            graph (Node): Graph to execute
            debug (bool): Debug mode

        Returns:
            iterator: Results iterator

        """

        for placeholder, values in self._ctx.items():
            # TODO: Check for iterable dimensions
            placeholder.parents = [_PlaceholderGenerator(values)]

        if debug:
            self._attach_debug_outputs(graph)

        graph.reset()

        for itm in graph:
            yield itm

        # Unregister ctx from graph
        for placeholder in self._ctx:
            placeholder.parents = []

        if debug:
            self._detach_debug_outputs(graph)

    def run_sync(self, graph, debug=False):
        """
        Do a synchronous run of a transformation graph.

        Args:
            graph (Node): Graph to execute
            debug (bool): Debug mode

        Returns:
            list: List of results

        """
        out = []

        for itm in self.run(graph, debug):
            out.append(itm)

        return out


class Session(object):

    """
    :py:class:`Session` is a context manager tasked with attaching and detaching a provided context to one (or multiple)
    transformation graph(s).

    Args:
        feed_dict (dict): Dictionary providing context mapping
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
