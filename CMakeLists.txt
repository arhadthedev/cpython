#На Windows:
#    target_sources - добавить PC/python_nt.rc к каждой библиотеке в зависимостях цели modules
#    set_property(DIRECTORY Modules SUFFIX pyd) -  для тех же библиотек
cmake_minimum_required(...)

project(python VERSION 3.11 HOMEPAGE_URL https://bugs.python.org/ LANGUAGES C)

include(CheckSymbolExists)

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

check_symbol_exists(uuid_create uuid.h HAVE_UUID_CREATE)
check_symbol_exists(uuid_enc_be uuid.h HAVE_UUID_ENC_BE)
if(HAVE_UUID_CREATE and HAVE_UUID_ENC_BE)
    add_library(_uuid SHARED Modules/_uuidmodule.c)
    target_link_libraries(_uuid rpcrt4)
    add_library(lib_uuid INTERFACE Lib/uuid.py)
    add_library(test_uuid INTERFACE Lib/test_uuid.py)
endif()

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
