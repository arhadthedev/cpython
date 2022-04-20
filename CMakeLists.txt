#На Windows:
#    target_sources - добавить PC/python_nt.rc к каждой библиотеке в зависимостях цели modules
#    set_property(DIRECTORY Modules SUFFIX pyd) -  для тех же библиотек
cmake_minimum_required(...)

project(python VERSION 3.11 HOMEPAGE_URL https://bugs.python.org/ LANGUAGES C)

####################################################
#
# Python Extension Libraries.
#
# To disable some, pass -DUSE_{MODULENAME}=NO flags to CMake
#
####################################################

include(CheckSymbolExists)

set(USE_CTYPES YES CACHE BOOL "Build and ship ctypes module")
if(USE_CTYPES)
    add_library(_ctypes SHARED
        Modules/_ctypes/_ctypes.c
        Modules/_ctypes/callbacks.c
        Modules/_ctypes/callproc.c
        Modules/_ctypes/cfield.c
        Modules/_ctypes/ctypes.h
        Modules/_ctypes/ctypes_dlfcn.h
        Modules/_ctypes/malloc_closure.c
        Modules/_ctypes/stgdict.c)
    target_compile_definitions(_ctypes PRIVATE USING_MALLOC_CLOSURE_DOT_C=1)
    # TODO: AdditionalOptions:/EXPORT:DllGetClassObject,PRIVATE /EXPORT:DllCanUnloadNow,PRIVATE
    add_library(lib_ctypes INTERFACE
        ctypes/macholib/dyld.py
        ctypes/macholib/dylib.py
        ctypes/macholib/framework.py
        ctypes/macholib/__init__.py)
    add_library(lib_ctypes INTERFACE
        ctypes/util.py
        ctypes/wintypes.py
        ctypes/_endian.py
        ctypes/__init__.py)
    add_library(test_ctypes SHARED
        Modules/_ctypes/_ctypes_test.h
        Modules/_ctypes/_ctypes_test.c
        ctypes/test/test_anon.py
        ctypes/test/test_arrays.py
        ctypes/test/test_array_in_pointer.py
        ctypes/test/test_as_parameter.py
        ctypes/test/test_bitfields.py
        ctypes/test/test_buffers.py
        ctypes/test/test_bytes.py
        ctypes/test/test_byteswap.py
        ctypes/test/test_callbacks.py
        ctypes/test/test_cast.py
        ctypes/test/test_cfuncs.py
        ctypes/test/test_checkretval.py
        ctypes/test/test_delattr.py
        ctypes/test/test_errno.py
        ctypes/test/test_find.py
        ctypes/test/test_frombuffer.py
        ctypes/test/test_funcptr.py
        ctypes/test/test_functions.py
        ctypes/test/test_incomplete.py
        ctypes/test/test_init.py
        ctypes/test/test_internals.py
        ctypes/test/test_keeprefs.py
        ctypes/test/test_libc.py
        ctypes/test/test_loading.py
        ctypes/test/test_macholib.py
        ctypes/test/test_memfunctions.py
        ctypes/test/test_numbers.py
        ctypes/test/test_objects.py
        ctypes/test/test_parameters.py
        ctypes/test/test_pep3118.py
        ctypes/test/test_pickling.py
        ctypes/test/test_pointers.py
        ctypes/test/test_prototypes.py
        ctypes/test/test_python_api.py
        ctypes/test/test_random_things.py
        ctypes/test/test_refcounts.py
        ctypes/test/test_repr.py
        ctypes/test/test_returnfuncptrs.py
        ctypes/test/test_simplesubclasses.py
        ctypes/test/test_sizes.py
        ctypes/test/test_slicing.py
        ctypes/test/test_stringptr.py
        ctypes/test/test_strings.py
        ctypes/test/test_structures.py
        ctypes/test/test_struct_fields.py
        ctypes/test/test_unaligned_structures.py
        ctypes/test/test_unicode.py
        ctypes/test/test_values.py
        ctypes/test/test_varsize_struct.py
        ctypes/test/test_win32.py
        ctypes/test/test_wintypes.py
        ctypes/test/__init__.py
        ctypes/test/__main__.py
        test/leakers/test_ctypes.py
        test/test_ctypes.py)
endif()

set(USE_GETPATH YES CACHE BOOL "Build and ship getpath module")
if(USE_GETPATH)
    add_library(getpath SHARED Modules/getpath.c)
    target_compile_definitions(getpath PRIVATE VPATH="$PyVPath")
endif()

set(USE_UUID YES CACHE BOOL "Build and ship uuid module")
if(USE_UUID)
    check_symbol_exists(uuid_create uuid.h HAVE_UUID_CREATE)
    check_symbol_exists(uuid_enc_be uuid.h HAVE_UUID_ENC_BE)
    if(HAVE_UUID_CREATE and HAVE_UUID_ENC_BE)
        add_library(_uuid SHARED Modules/_uuidmodule.c)
        target_link_libraries(_uuid rpcrt4)
        add_library(lib_uuid INTERFACE Lib/uuid.py)
        add_library(test_uuid INTERFACE Lib/test_uuid.py)
    endif()
endif()

set(USE_ZONEINFO YES CACHE BOOL "Build and ship zoneinfo module")
if(USE_UUID)
    add_library(_zoneinfo SHARED Modules/_zoneinfo.c)
    add_library(lib_zoneinfo INTERFACE
        zoneinfo/_common.py
        zoneinfo/__init__.py
        zoneinfo/_tzpath.py
        zoneinfo/_zoneinfo.py
    target_sources(test_zoneinfo PUBLIC
        test/test_zoneinfo/__init__.py
        test/test_zoneinfo/__main__.py
        test/test_zoneinfo/_support.py
        test/test_zoneinfo/test_zoneinfo.py)
endif()

####################################################
#
# Python Executable and Tools.
#
####################################################

add_library(pythoncore STATIC
    Include/Python.h
    Include/abstract.h
    Include/boolobject.h
    Include/bytearrayobject.h
    Include/bytesobject.h
    Include/ceval.h
    Include/codecs.h
    Include/compile.h
    Include/complexobject.h
    Include/cpython/abstract.h
    Include/cpython/bytearrayobject.h
    Include/cpython/bytesobject.h
    Include/cpython/cellobject.h
    Include/cpython/ceval.h
    Include/cpython/classobject.h
    Include/cpython/code.h
    Include/cpython/compile.h
    Include/cpython/complexobject.h
    Include/cpython/context.h
    Include/cpython/descrobject.h
    Include/cpython/dictobject.h
    Include/cpython/fileobject.h
    Include/cpython/fileutils.h
    Include/cpython/floatobject.h
    Include/cpython/frameobject.h
    Include/cpython/funcobject.h
    Include/cpython/genobject.h
    Include/cpython/import.h
    Include/cpython/initconfig.h
    Include/cpython/listobject.h
    Include/cpython/longintrepr.h
    Include/cpython/longobject.h
    Include/cpython/methodobject.h
    Include/cpython/object.h
    Include/cpython/objimpl.h
    Include/cpython/odictobject.h
    Include/cpython/parser_interface.h
    Include/cpython/picklebufobject.h
    Include/cpython/pyarena.h
    Include/cpython/pyctype.h
    Include/cpython/pydebug.h
    Include/cpython/pyerrors.h
    Include/cpython/pyfpe.h
    Include/cpython/pylifecycle.h
    Include/cpython/pymem.h
    Include/cpython/pystate.h
    Include/cpython/pythonrun.h
    Include/cpython/pytime.h
    Include/cpython/setobject.h
    Include/cpython/sysmodule.h
    Include/cpython/traceback.h
    Include/cpython/tupleobject.h
    Include/cpython/unicodeobject.h
    Include/cpython/warnings.h
    Include/cpython/weakrefobject.h
    Include/datetime.h
    Include/descrobject.h
    Include/dictobject.h
    Include/dynamic_annotations.h
    Include/enumobject.h
    Include/errcode.h
    Include/fileobject.h
    Include/fileutils.h
    Include/floatobject.h
    Include/frameobject.h
    Include/import.h
    Include/internal/pycore_abstract.h
    Include/internal/pycore_accu.h
    Include/internal/pycore_asdl.h
    Include/internal/pycore_ast.h
    Include/internal/pycore_ast_state.h
    Include/internal/pycore_atomic.h
    Include/internal/pycore_atomic_funcs.h
    Include/internal/pycore_bitutils.h
    Include/internal/pycore_bytes_methods.h
    Include/internal/pycore_bytesobject.h
    Include/internal/pycore_call.h
    Include/internal/pycore_ceval.h
    Include/internal/pycore_code.h
    Include/internal/pycore_compile.h
    Include/internal/pycore_condvar.h
    Include/internal/pycore_context.h
    Include/internal/pycore_dtoa.h
    Include/internal/pycore_exceptions.h
    Include/internal/pycore_fileutils.h
    Include/internal/pycore_floatobject.h
    Include/internal/pycore_format.h
    Include/internal/pycore_function.h
    Include/internal/pycore_gc.h
    Include/internal/pycore_genobject.h
    Include/internal/pycore_getopt.h
    Include/internal/pycore_gil.h
    Include/internal/pycore_global_objects.h
    Include/internal/pycore_hamt.h
    Include/internal/pycore_hashtable.h
    Include/internal/pycore_import.h
    Include/internal/pycore_initconfig.h
    Include/internal/pycore_interp.h
    Include/internal/pycore_interpreteridobject.h
    Include/internal/pycore_list.h
    Include/internal/pycore_long.h
    Include/internal/pycore_moduleobject.h
    Include/internal/pycore_namespace.h
    Include/internal/pycore_object.h
    Include/internal/pycore_pathconfig.h
    Include/internal/pycore_pyarena.h
    Include/internal/pycore_pyerrors.h
    Include/internal/pycore_pyhash.h
    Include/internal/pycore_pylifecycle.h
    Include/internal/pycore_pymem.h
    Include/internal/pycore_pystate.h
    Include/internal/pycore_runtime.h
    Include/internal/pycore_runtime_init.h
    Include/internal/pycore_sliceobject.h
    Include/internal/pycore_strhex.h
    Include/internal/pycore_structseq.h
    Include/internal/pycore_sysmodule.h
    Include/internal/pycore_symtable.h
    Include/internal/pycore_traceback.h
    Include/internal/pycore_tuple.h
    Include/internal/pycore_typeobject.h
    Include/internal/pycore_ucnhash.h
    Include/internal/pycore_unionobject.h
    Include/internal/pycore_unicodeobject.h
    Include/internal/pycore_warnings.h
    Include/intrcheck.h
    Include/iterobject.h
    Include/listobject.h
    Include/longobject.h
    Include/marshal.h
    Include/memoryobject.h
    Include/methodobject.h
    Include/modsupport.h
    Include/moduleobject.h
    Include/object.h
    Include/objimpl.h
    Include/opcode.h
    Include/osdefs.h
    Include/osmodule.h
    Include/patchlevel.h
    Include/py_curses.h
    Include/pybuffer.h
    Include/pycapsule.h
    Include/pyerrors.h
    Include/pyexpat.h
    Include/pyframe.h
    Include/pyhash.h
    Include/pylifecycle.h
    Include/pymacro.h
    Include/pymath.h
    Include/pymem.h
    Include/pyport.h
    Include/pystate.h
    Include/pystrcmp.h
    Include/pystrtod.h
    Include/pythonrun.h
    Include/pythread.h
    Include/pytypedefs.h
    Include/rangeobject.h
    Include/setobject.h
    Include/sliceobject.h
    Include/structmember.h
    Include/structseq.h
    Include/symtable.h
    Include/sysmodule.h
    Include/token.h
    Include/traceback.h
    Include/tracemalloc.h
    Include/tupleobject.h
    Include/unicodeobject.h
    Include/weakrefobject.h
    Objects/stringlib/count.h
    Objects/stringlib/fastsearch.h
    Objects/stringlib/find.h
    Objects/stringlib/partition.h
    Objects/stringlib/replace.h
    Objects/stringlib/split.h
    Objects/unicodetype_db.h
    Parser/tokenizer.h
    Parser/string_parser.h
    Parser/pegen.h
    PC/errmap.h
    PC/pyconfig.h
    Python/ceval_gil.h
    Python/condvar.h
    Python/importdl.h
    Python/stdlib_module_names.h
    Python/thread_nt.h

    Objects/abstract.c
    Objects/accu.c
    Objects/boolobject.c
    Objects/bytearrayobject.c
    Objects/bytes_methods.c
    Objects/bytesobject.c
    Objects/call.c
    Objects/capsule.c
    Objects/cellobject.c
    Objects/classobject.c
    Objects/codeobject.c
    Objects/complexobject.c
    Objects/descrobject.c
    Objects/dictobject.c
    Objects/enumobject.c
    Objects/exceptions.c
    Objects/fileobject.c
    Objects/floatobject.c
    Objects/frameobject.c
    Objects/funcobject.c
    Objects/genericaliasobject.c
    Objects/genobject.c
    Objects/interpreteridobject.c
    Objects/iterobject.c
    Objects/listobject.c
    Objects/longobject.c
    Objects/memoryobject.c
    Objects/methodobject.c
    Objects/moduleobject.c
    Objects/namespaceobject.c
    Objects/object.c
    Objects/obmalloc.c
    Objects/odictobject.c
    Objects/picklebufobject.c
    Objects/rangeobject.c
    Objects/setobject.c
    Objects/sliceobject.c
    Objects/structseq.c
    Objects/tupleobject.c
    Objects/typeobject.c
    Objects/unicodectype.c
    Objects/unicodeobject.c
    Objects/unionobject.c
    Objects/weakrefobject.c
    Parser/myreadline.c
    Parser/tokenizer.c
    Parser/token.c
    Parser/pegen.c
    Parser/pegen_errors.c
    Parser/action_helpers.c
    Parser/parser.c
    Parser/string_parser.c
    Parser/peg_api.c
    PC/invalid_parameter_handler.c
    PC/winreg.c
    PC/config.c
    PC/msvcrtmodule.c
    Python/pyhash.c
    Python/_warnings.c
    Python/asdl.c
    Python/ast.c
    Python/ast_opt.c
    Python/ast_unparse.c
    Python/bltinmodule.c
    Python/bootstrap_hash.c
    Python/ceval.c
    Python/codecs.c
    Python/compile.c
    Python/context.c
    Python/dynamic_annotations.c
    Python/dynload_win.c
    Python/errors.c
    Python/fileutils.c
    Python/formatter_unicode.c
    Python/frame.c
    Python/frozen.c
    Python/future.c
    Python/getargs.c
    Python/getcompiler.c
    Python/getcopyright.c
    Python/getopt.c
    Python/getplatform.c
    Python/getversion.c
    Python/hamt.c
    Python/hashtable.c
    Python/import.c
    Python/importdl.c
    Python/initconfig.c
    Python/marshal.c
    Python/modsupport.c
    Python/mysnprintf.c
    Python/mystrtoul.c
    Python/pathconfig.c
    Python/preconfig.c
    Python/pyarena.c
    Python/pyctype.c
    Python/pyfpe.c
    Python/pylifecycle.c
    Python/pymath.c
    Python/pytime.c
    Python/pystate.c
    Python/pystrcmp.c
    Python/pystrhex.c
    Python/pystrtod.c
    Python/dtoa.c
    Python/Python-ast.c
    Python/Python-tokenize.c
    Python/pythonrun.c
    Python/specialize.c
    Python/suggestions.c
    Python/structmember.c
    Python/symtable.c
    Python/sysmodule.c
    Python/thread.c
    Python/traceback.c)
target_link_pymodules(pythoncore)
target_compile_definitions(pythoncore PRIVATE Py_BUILD_CORE)
target_compile_definitions(pythoncore PRIVATE Py_BUILD_CORE_BUILTIN)
target_compile_definitions(pythoncore PRIVATE Py_ENABLE_SHARED)
target_compile_definitions(pythoncore PRIVATE VPATH="$PyVPath")

if(WINDOWS)
    set_source_files_properties(SOURCE Python/sysmodule.c PROPERTIES 
        COMPILE_DEFINITIONS VPATH="$PyVPath")
    add_executable(venvlauncher PC/launcher.c PC/pylauncher.rc)
    target_compile_definitions(venvlauncher PRIVATE VENV_REDIRECT PY_ICON)
    target_link_libraries(venvlauncher version)

    add_executable(venvwlauncher PC/launcher.c PC/pylauncher.rc)
    target_compile_definitions(venvlauncher PRIVATE VENV_REDIRECT PYW_ICON)
    target_link_libraries(venvlauncher version)

    add_library(python3 DINAMIC PC/python3dll.c PC/python_nt.rc)
    target_link_library(pythoncore)
endif()
