/*[clinic input]
preserve
[clinic start generated code]*/

PyDoc_STRVAR(sock_getsockopt__doc__,
"getsockopt($self, level, option, buffersize=0, /)\n"
"--\n"
"\n"
"Get a socket option.\n"
"\n"
"See the Unix manual for level and option. If a nonzero buffersize argument\n"
"is given, the return value is a string of that length; otherwise it is an\n"
"integer.");

#define SOCK_GETSOCKOPT_METHODDEF    \
    {"getsockopt", (PyCFunction)(void(*)(void))sock_getsockopt, METH_FASTCALL, sock_getsockopt__doc__},

static PyObject *
sock_getsockopt_impl(PySocketSockObject *self, int level, int option,
                     int buffersize);

static PyObject *
sock_getsockopt(PySocketSockObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject *return_value = NULL;
    int level;
    int option;
    int buffersize = 0;

    if (!_PyArg_CheckPositional("getsockopt", nargs, 2, 3)) {
        goto exit;
    }
    level = _PyLong_AsInt(args[0]);
    if (level == -1 && PyErr_Occurred()) {
        goto exit;
    }
    option = _PyLong_AsInt(args[1]);
    if (option == -1 && PyErr_Occurred()) {
        goto exit;
    }
    if (nargs < 3) {
        goto skip_optional;
    }
    buffersize = _PyLong_AsInt(args[2]);
    if (buffersize == -1 && PyErr_Occurred()) {
        goto exit;
    }
skip_optional:
    return_value = sock_getsockopt_impl(self, level, option, buffersize);

exit:
    return return_value;
}
/*[clinic end generated code: output=7b3dbf894e605052 input=a9049054013a1b77]*/
