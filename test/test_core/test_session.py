from queue import Queue

from test.context import pf

from unittest.mock import patch

import unittest


def count_debug_nodes(graph):

    queue = Queue()
    queue.put(graph)

    actual_debug_out_count = 0

    while not queue.empty():
        node = queue.get()

        if isinstance(node, pf.output.DiskOutput) and hasattr(node, '_debug'):
            actual_debug_out_count += 1

        if hasattr(node, 'parents'):
            for parent in node.parents:
                queue.put(parent)

    return actual_debug_out_count



class TestSessionInitialize(unittest.TestCase):

    def test_session_initalize_sets_context(self):
        ctx_dict = {'hello': 'world'}

        s = pf.Session(ctx_dict)

        self.assertEqual(s._ctx, ctx_dict)


class TestSessionContextManager(unittest.TestCase):

    def test_session_enter_returns_sessionwrapper(self):

        with pf.Session({}) as sess:
            self.assertIsInstance(sess, pf.core.session.SessionWrapper)

    def test_session_exit_doesnt_raise_exception(self):

        try:
            with pf.Session({}) as sess:
                pass

        except Exception:
            self.fail('Session exit should not raise an exception')


class TestSessionWrapperInitialize(unittest.TestCase):

    def test_sessionwrapper_initialize_sets_context(self):
        ctx_dict = {'hello': 'world'}

        s = pf.core.session.SessionWrapper(ctx_dict)

        self.assertEqual(s._ctx, ctx_dict)


class TestSessionWrapperRun(unittest.TestCase):

    def test_sessionwrapper_run_attaches_generators_to_placeholders(self):
        placeholder = pf.Placeholder(out_type=int)

        ctx = {placeholder: [1, 2, 3]}

        self.assertEqual(len(placeholder.parents), 0)

        with pf.Session(ctx) as sess:
            generator = sess.run(placeholder)
            next(generator)
            self.assertEqual(len(placeholder.parents), 1)

    @patch('pictureflow.core.session.SessionWrapper._attach_debug_outputs')
    def test_sessionwrapper_run_calls_attach_debug_when_in_debug(self, mock_attach):
        placeholder = pf.Placeholder(out_type=int)

        ctx = {placeholder: [1, 2, 3]}

        with pf.Session(ctx) as sess:
            generator = sess.run(placeholder, debug=True)
            next(generator)
            self.assertTrue(mock_attach.called)

    @patch('pictureflow.core.session.SessionWrapper._attach_debug_outputs')
    def test_sessionwrapper_run_doesnt_call_attach_debug_when_not_in_debug(self, mock_attach):
        placeholder = pf.Placeholder(out_type=int)

        ctx = {placeholder: [1, 2, 3]}

        with pf.Session(ctx) as sess:
            generator = sess.run(placeholder, debug=False)
            next(generator)
            self.assertFalse(mock_attach.called)

    @patch('pictureflow.core.session.SessionWrapper._detach_debug_outputs')
    def test_sessionwrapper_run_calls_detach_debug_when_in_debug(self, mock_detach):
        placeholder = pf.Placeholder(out_type=int)

        ctx = {placeholder: [1, 2, 3]}

        with pf.Session(ctx) as sess:
            generator = sess.run(placeholder, debug=True)
            _ = [x for x in generator]
            self.assertTrue(mock_detach.called)

    @patch('pictureflow.core.session.SessionWrapper._detach_debug_outputs')
    def test_sessionwrapper_run_doesnt_call_detach_debug_when_not_in_debug(self, mock_detach):
        placeholder = pf.Placeholder(out_type=int)

        ctx = {placeholder: [1, 2, 3]}

        with pf.Session(ctx) as sess:
            generator = sess.run(placeholder, debug=False)
            _ = [x for x in generator]

            self.assertFalse(mock_detach.called)

    def test_sessionwrapper_run_removes_generators_after_run(self):

        placeholder = pf.Placeholder(out_type=int)
        ctx = {placeholder: [1, 2, 3]}

        self.assertEqual(len(placeholder.parents), 0)

        with pf.Session(ctx) as sess:
            for _ in sess.run(placeholder):
                pass

        self.assertEqual(len(placeholder.parents), 0)

    def test_sessionwrapper_yields_item_from_graph(self):
        placeholder = pf.Placeholder(out_type=int)
        ctx = {placeholder: [1, 2, 3]}

        output = []
        with pf.Session(ctx) as sess:
            for i in sess.run(placeholder):
                output.append(i)

        self.assertEqual(output, ctx[placeholder])


class TestSessionWrapperRunSync(unittest.TestCase):

    def test_sessionwrapper_run_sync_returns_all_values_synchronously(self):
        placeholder = pf.Placeholder(out_type=int)
        ctx = {placeholder: [1, 2, 3]}

        with pf.Session(ctx) as sess:
            output = sess.run_sync(placeholder)

        self.assertEqual(output, ctx[placeholder])


class TestSessionWrapperAttachOutputs(unittest.TestCase):

    @staticmethod
    def _get_graph():
        graph = pf.Placeholder(out_type=pf.Image)

        graph = pf.transform.Rotate(graph, rot_angle=pf.Constant(90))
        graph = pf.transform.Scale(graph, scale_factor=pf.Constant(0.1))

        graph = pf.output.DiskOutput(graph, base_path=pf.Constant('data/output/'))

        return graph

    def test_attach_debug_outputs_appends_the_correct_number_of_disk_outputs(self):
        graph = TestSessionWrapperAttachOutputs._get_graph()
        expected_debug_out_count = 3

        pf.core.session.SessionWrapper._attach_debug_outputs(graph)

        self.assertEqual(count_debug_nodes(graph), expected_debug_out_count)


class TestSessionWrapperDetachDebugOutput(unittest.TestCase):

    @staticmethod
    def _get_graph():
        graph = pf.Placeholder(out_type=pf.Image)

        graph = pf.transform.Rotate(graph, rot_angle=pf.Constant(90))
        graph = pf.transform.Scale(graph, scale_factor=pf.Constant(0.1))

        graph = pf.output.DiskOutput(graph, base_path=pf.Constant('data/output/'))

        return graph

    def test_detach_debug_outputs_removes_all_disk_outputs(self):
        graph = TestSessionWrapperAttachOutputs._get_graph()
        expected_debug_out_count = 3

        pf.core.session.SessionWrapper._attach_debug_outputs(graph)

        self.assertEqual(count_debug_nodes(graph), expected_debug_out_count)

        pf.core.session.SessionWrapper._detach_debug_outputs(graph)

        self.assertEqual(count_debug_nodes(graph), 0)
