"""Test script for poplib module."""

# Modified by Giampaolo Rodola' to give poplib.POP3 and poplib.POP3_SSL
# a real test suite

import asyncio
import poplib
import socket
import os
import errno
import threading

import unittest
from unittest import IsolatedAsyncioTestCase, TestCase, skipUnless
from test import support as test_support
from test.support import hashlib_helper
from test.support import socket_helper
from test.support import threading_helper


test_support.requires_working_socket(module=True)


SUPPORTS_SSL = False
if hasattr(poplib, 'POP3_SSL'):
    import ssl

    SUPPORTS_SSL = True
    CERTFILE = os.path.join(os.path.dirname(__file__) or os.curdir, "keycert3.pem")
    CAFILE = os.path.join(os.path.dirname(__file__) or os.curdir, "pycacert.pem")

requires_ssl = skipUnless(SUPPORTS_SSL, 'SSL not supported')

# the dummy data returned by server when LIST and RETR commands are issued
LIST_RESP = b'1 1\r\n2 2\r\n3 3\r\n4 4\r\n5 5\r\n.\r\n'
RETR_RESP = b"""From: postmaster@python.org\
\r\nContent-Type: text/plain\r\n\
MIME-Version: 1.0\r\n\
Subject: Dummy\r\n\
\r\n\
line1\r\n\
line2\r\n\
line3\r\n\
.\r\n"""


async def _on_pop3_client(reader, writer):
    CAPAS = {'UIDL': [], 'IMPLEMENTATION': ['python-testlib-pop-server']}
    utf_mode = False
    tls_active = False
    tls_starting = False

    handlers = {}

    def cmd_echo(cmd_arguments, reply):
        reply(b' '.join(cmd_arguments))

    handlers['echo'] = cmd_echo

    def cmd_user(cmd_arguments, reply):
        user = cmd_arguments[0] if cmd_arguments else None
        correct = (user == b'guido')
        reply(b'+OK password required' if correct else b'-ERR no such user')

    handlers['user'] = cmd_user

    def cmd_pass(cmd_arguments, reply):
        password = cmd_arguments[0] if cmd_arguments else None
        correct = (password == b'python')
        reply(b'+OK 10 messages' if correct else b'-ERR wrong password')

    handlers['pass'] = cmd_pass

    def cmd_stat(cmd_arguments, reply):
        reply(b'+OK 10 100')

    handlers['stat'] = cmd_stat

    def cmd_list(cmd_arguments, reply):
        if arg:
            self.push('+OK %s %s' % (arg, arg))
        else:
            self.push('+OK')
            asynchat.async_chat.push(self, LIST_RESP)

    handlers['list'] = cmd_list
    handlers['uidl'] = cmd_list

    def cmd_retr(cmd_arguments, reply):
        self.push('+OK %s bytes' %len(RETR_RESP))
        asynchat.async_chat.push(self, RETR_RESP)

    handlers['retr'] = cmd_retr
    handlers['top'] = cmd_retr

    def cmd_dele(cmd_arguments, reply):
        response.write(b'+OK message marked for deletion.')

     handlers['dele'] = cmd_dele

    def return_ok_done_nothing(cmd_arguments, reply):
        response.write(b'+OK done nothing.')

    handlers['noop'] = return_ok_done_nothing
    handlers['rpop'] = return_ok_done_nothing
    handlers['apop'] = return_ok_done_nothing

    def cmd_quit(cmd_arguments, reply):
        reply(b'+OK message marked for deletion.')
        reply('+OK closing.')
        return True

    handlers['quit'] = cmd_quit

    def _get_capas(self):
        _capas = dict(self.CAPAS)
        if not self.tls_active and SUPPORTS_SSL:
            _capas['STLS'] = []
        return _capas

    def cmd_capa(cmd_arguments, reply):
        reply('+OK Capability list follows')
        if self._get_capas():
            for cap, params in self._get_capas().items():
                _ln = [cap]
                if params:
                    _ln.extend(params)
                reply(' '.join(_ln))
        self.push('.')

    handlers['capa'] = cmd_capa

    def cmd_utf8(cmd_arguments, reply):
        reply('+OK I know RFC6856' if self.utf_mode else '-ERR What is UTF8?!')

    handlers['utf8'] = cmd_utf8

    if SUPPORTS_SSL:

        def cmd_stls(cmd_arguments, reply):
            if self.tls_active is False:
                reply('+OK Begin TLS negotiation')
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain(CERTFILE)
                writer.start_tls(context)

                tls_sock = context.wrap_socket(self.socket,
                                               server_side=True,
                                               do_handshake_on_connect=False,
                                               suppress_ragged_eofs=False)
                self.del_channel()
                self.set_socket(tls_sock)
                self.tls_active = True
                self.tls_starting = True
                self.in_buffer = []
                self._do_tls_handshake()
            else:
                reply('-ERR Command not permitted when TLS active')

        handlers['stls'] = cmd_stls

        def _do_tls_handshake(self):
            try:
                self.socket.do_handshake()
            except ssl.SSLError as err:
                if err.args[0] in (ssl.SSL_ERROR_WANT_READ,
                                   ssl.SSL_ERROR_WANT_WRITE):
                    return
                elif err.args[0] == ssl.SSL_ERROR_EOF:
                    return self.handle_close()
                # TODO: SSLError does not expose alert information
                elif ("SSLV3_ALERT_BAD_CERTIFICATE" in err.args[1] or
                      "SSLV3_ALERT_CERTIFICATE_UNKNOWN" in err.args[1]):
                    return self.handle_close()
                raise
            except OSError as err:
                if err.args[0] == errno.ECONNABORTED:
                    return self.handle_close()
            else:
                self.tls_active = True
                self.tls_starting = False

        def handle_read(self):
            if self.tls_starting:
                self._do_tls_handshake()
            else:
                try:
                    asynchat.async_chat.handle_read(self)
                except ssl.SSLEOFError:
                    self.handle_close()


    def unknown_cmd_handler(cmd_arguments, reply):
        reply(b'-ERR unrecognized POP3 command\r\n')

    with writer:
        writer.write(b'+OK dummy pop3 server ready. <timestamp>\r\n')
        await writer.drain()

        wait_next_cmd = True
        while wait_next_cmd and not reader.at_eof():
            request = await reader.readline()
            cmd, *cmd_args = request.split(b' ')
            wait_next_cmd = command_handlers.get(cmd, unknown_cmd_handler)(cmd_args)




                                    class DummyPOP3Server(asyncore.dispatcher, threading.Thread):

                                        handler = DummyPOP3Handler

                                        def __init__(self, address, af=socket.AF_INET):
                                            threading.Thread.__init__(self)
                                            asyncore.dispatcher.__init__(self)
                                            self.daemon = True
                                            self.create_socket(af, socket.SOCK_STREAM)
                                            self.bind(address)
                                            self.listen(5)
                                            self.active = False
                                            self.active_lock = threading.Lock()
                                            self.host, self.port = self.socket.getsockname()[:2]
                                            self.handler_instance = None

                                        def start(self):
                                            assert not self.active
                                            self.__flag = threading.Event()
                                            threading.Thread.start(self)
                                            self.__flag.wait()

                                        def run(self):
                                            self.active = True
                                            self.__flag.set()
                                            try:
                                                while self.active and asyncore.socket_map:
                                                    with self.active_lock:
                                                        asyncore.loop(timeout=0.1, count=1)
                                            finally:
                                                asyncore.close_all(ignore_all=True)

                                        def stop(self):
                                            assert self.active
                                            self.active = False
                                            self.join()

                                        def handle_accepted(self, conn, addr):
                                            self.handler_instance = self.handler(conn)

                                        def handle_connect(self):
                                            self.close()
                                        handle_read = handle_connect

                                        def writable(self):
                                            return 0

                                        def handle_error(self):
                                            raise


class TestPOP3Class(TestCase):
    def assertOK(self, resp):
        self.assertTrue(resp.startswith(b"+OK"))

    def setUp(self):
        self.server = DummyPOP3Server((HOST, PORT))
        self.server.start()
        self.client = poplib.POP3(self.server.host, self.server.port,
                                  timeout=test_support.LOOPBACK_TIMEOUT)

    def tearDown(self):
        self.client.close()
        self.server.stop()
        # Explicitly clear the attribute to prevent dangling thread
        self.server = None

    def test_getwelcome(self):
        self.assertEqual(self.client.getwelcome(),
                         b'+OK dummy pop3 server ready. <timestamp>')

    def test_exceptions(self):
        self.assertRaises(poplib.error_proto, self.client._shortcmd, 'echo -err')

    def test_user(self):
        self.assertOK(self.client.user('guido'))
        self.assertRaises(poplib.error_proto, self.client.user, 'invalid')

    def test_pass_(self):
        self.assertOK(self.client.pass_('python'))
        self.assertRaises(poplib.error_proto, self.client.user, 'invalid')

    def test_stat(self):
        self.assertEqual(self.client.stat(), (10, 100))

    def test_list(self):
        self.assertEqual(self.client.list()[1:],
                         ([b'1 1', b'2 2', b'3 3', b'4 4', b'5 5'],
                          25))
        self.assertTrue(self.client.list('1').endswith(b"OK 1 1"))

    def test_retr(self):
        expected = (b'+OK 116 bytes',
                    [b'From: postmaster@python.org', b'Content-Type: text/plain',
                     b'MIME-Version: 1.0', b'Subject: Dummy',
                     b'', b'line1', b'line2', b'line3'],
                    113)
        foo = self.client.retr('foo')
        self.assertEqual(foo, expected)

    def test_too_long_lines(self):
        self.assertRaises(poplib.error_proto, self.client._shortcmd,
                          'echo +%s' % ((poplib._MAXLINE + 10) * 'a'))

    def test_dele(self):
        self.assertOK(self.client.dele('foo'))

    def test_noop(self):
        self.assertOK(self.client.noop())

    def test_rpop(self):
        self.assertOK(self.client.rpop('foo'))

    @hashlib_helper.requires_hashdigest('md5', openssl=True)
    def test_apop_normal(self):
        self.assertOK(self.client.apop('foo', 'dummypassword'))

    @hashlib_helper.requires_hashdigest('md5', openssl=True)
    def test_apop_REDOS(self):
        # Replace welcome with very long evil welcome.
        # NB The upper bound on welcome length is currently 2048.
        # At this length, evil input makes each apop call take
        # on the order of milliseconds instead of microseconds.
        evil_welcome = b'+OK' + (b'<' * 1000000)
        with test_support.swap_attr(self.client, 'welcome', evil_welcome):
            # The evil welcome is invalid, so apop should throw.
            self.assertRaises(poplib.error_proto, self.client.apop, 'a', 'kb')

    def test_top(self):
        expected =  (b'+OK 116 bytes',
                     [b'From: postmaster@python.org', b'Content-Type: text/plain',
                      b'MIME-Version: 1.0', b'Subject: Dummy', b'',
                      b'line1', b'line2', b'line3'],
                     113)
        self.assertEqual(self.client.top(1, 1), expected)

    def test_uidl(self):
        self.client.uidl()
        self.client.uidl('foo')

    def test_utf8_raises_if_unsupported(self):
        self.server.handler.utf8_mode = False
        self.assertRaises(poplib.error_proto, self.client.utf8)

    def test_utf8(self):
        self.server.handler.utf8_mode = True
        expected = b'+OK I know RFC6856'
        result = self.client.utf8()
        self.assertEqual(result, expected)

    def test_capa(self):
        capa = self.client.capa()
        self.assertTrue('IMPLEMENTATION' in capa.keys())

    def test_quit(self):
        resp = self.client.quit()
        self.assertTrue(resp)
        self.assertIsNone(self.client.sock)
        self.assertIsNone(self.client.file)

    @requires_ssl
    def test_stls_capa(self):
        capa = self.client.capa()
        self.assertTrue('STLS' in capa.keys())

    @requires_ssl
    def test_stls(self):
        expected = b'+OK Begin TLS negotiation'
        resp = self.client.stls()
        self.assertEqual(resp, expected)

    @requires_ssl
    def test_stls_context(self):
        expected = b'+OK Begin TLS negotiation'
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_verify_locations(CAFILE)
        self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)
        self.assertEqual(ctx.check_hostname, True)
        with self.assertRaises(ssl.CertificateError):
            resp = self.client.stls(context=ctx)
        self.client = poplib.POP3("localhost", self.server.port,
                                  timeout=test_support.LOOPBACK_TIMEOUT)
        resp = self.client.stls(context=ctx)
        self.assertEqual(resp, expected)


if SUPPORTS_SSL:
    from test.test_ftplib import SSLConnection

    class DummyPOP3_SSLHandler(SSLConnection, DummyPOP3Handler):

        def __init__(self, conn):
            asynchat.async_chat.__init__(self, conn)
            self.secure_connection()
            self.set_terminator(b"\r\n")
            self.in_buffer = []
            self.push('+OK dummy pop3 server ready. <timestamp>')
            self.tls_active = True
            self.tls_starting = False


@requires_ssl
class TestPOP3_SSLClass(TestPOP3Class):
    # repeat previous tests by using poplib.POP3_SSL

    def setUp(self):
        self.server = DummyPOP3Server((HOST, PORT))
        self.server.handler = DummyPOP3_SSLHandler
        self.server.start()
        self.client = poplib.POP3_SSL(self.server.host, self.server.port)

    def test__all__(self):
        self.assertIn('POP3_SSL', poplib.__all__)

    def test_context(self):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.assertRaises(ValueError, poplib.POP3_SSL, self.server.host,
                            self.server.port, keyfile=CERTFILE, context=ctx)
        self.assertRaises(ValueError, poplib.POP3_SSL, self.server.host,
                            self.server.port, certfile=CERTFILE, context=ctx)
        self.assertRaises(ValueError, poplib.POP3_SSL, self.server.host,
                            self.server.port, keyfile=CERTFILE,
                            certfile=CERTFILE, context=ctx)

        self.client.quit()
        self.client = poplib.POP3_SSL(self.server.host, self.server.port,
                                        context=ctx)
        self.assertIsInstance(self.client.sock, ssl.SSLSocket)
        self.assertIs(self.client.sock.context, ctx)
        self.assertTrue(self.client.noop().startswith(b'+OK'))

    def test_stls(self):
        self.assertRaises(poplib.error_proto, self.client.stls)

    test_stls_context = test_stls

    def test_stls_capa(self):
        capa = self.client.capa()
        self.assertFalse('STLS' in capa.keys())


@requires_ssl
class TestPOP3_TLSClass(TestPOP3Class):
    # repeat previous tests by using poplib.POP3.stls()

    def setUp(self):
        self.server = DummyPOP3Server((HOST, PORT))
        self.server.start()
        self.client = poplib.POP3(self.server.host, self.server.port,
                                  timeout=test_support.LOOPBACK_TIMEOUT)
        self.client.stls()

    def tearDown(self):
        if self.client.file is not None and self.client.sock is not None:
            try:
                self.client.quit()
            except poplib.error_proto:
                # happens in the test_too_long_lines case; the overlong
                # response will be treated as response to QUIT and raise
                # this exception
                self.client.close()
        self.server.stop()
        # Explicitly clear the attribute to prevent dangling thread
        self.server = None

    def test_stls(self):
        self.assertRaises(poplib.error_proto, self.client.stls)

    test_stls_context = test_stls

    def test_stls_capa(self):
        capa = self.client.capa()
        self.assertFalse(b'STLS' in capa.keys())


class TestTimeouts(TestCase):

    def setUp(self):
        self.evt = threading.Event()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(60)  # Safety net. Look issue 11812
        self.port = socket_helper.bind_port(self.sock)
        self.thread = threading.Thread(target=self.server, args=(self.evt, self.sock))
        self.thread.daemon = True
        self.thread.start()
        self.evt.wait()

    def tearDown(self):
        self.thread.join()
        # Explicitly clear the attribute to prevent dangling thread
        self.thread = None

    def server(self, evt, serv):
        serv.listen()
        evt.set()
        try:
            conn, addr = serv.accept()
            conn.send(b"+ Hola mundo\n")
            conn.close()
        except TimeoutError:
            pass
        finally:
            serv.close()

    def testTimeoutDefault(self):
        self.assertIsNone(socket.getdefaulttimeout())
        socket.setdefaulttimeout(test_support.LOOPBACK_TIMEOUT)
        try:
            pop = poplib.POP3(HOST, self.port)
        finally:
            socket.setdefaulttimeout(None)
        self.assertEqual(pop.sock.gettimeout(), test_support.LOOPBACK_TIMEOUT)
        pop.close()

    def testTimeoutNone(self):
        self.assertIsNone(socket.getdefaulttimeout())
        socket.setdefaulttimeout(30)
        try:
            pop = poplib.POP3(HOST, self.port, timeout=None)
        finally:
            socket.setdefaulttimeout(None)
        self.assertIsNone(pop.sock.gettimeout())
        pop.close()

    def testTimeoutValue(self):
        pop = poplib.POP3(HOST, self.port, timeout=test_support.LOOPBACK_TIMEOUT)
        self.assertEqual(pop.sock.gettimeout(), test_support.LOOPBACK_TIMEOUT)
        pop.close()
        with self.assertRaises(ValueError):
            poplib.POP3(HOST, self.port, timeout=0)


def setUpModule():
    thread_info = threading_helper.threading_setup()
    unittest.addModuleCleanup(threading_helper.threading_cleanup, *thread_info)


if __name__ == '__main__':
    unittest.main()
