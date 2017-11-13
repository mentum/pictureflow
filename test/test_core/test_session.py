from test.context import pf

import unittest


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
