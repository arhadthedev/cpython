#На Windows:
#    target_sources - добавить PC/python_nt.rc к каждой библиотеке в зависимостях цели modules
#    set_property(DIRECTORY Modules SUFFIX pyd) -  для тех же библиотек
cmake_minimum_required(...)

project(python VERSION 3.11 HOMEPAGE_URL https://bugs.python.org/ LANGUAGES C)

include(CheckSymbolExists)

check_symbol_exists(uuid_create uuid.h HAVE_UUID_CREATE)
check_symbol_exists(uuid_enc_be uuid.h HAVE_UUID_ENC_BE)
if(HAVE_UUID_CREATE and HAVE_UUID_ENC_BE)
    add_library(_uuid SHARED Modules/_uuidmodule.c)
    target_link_libraries(_uuid rpcrt4)
    add_library(uuid_lib INTERFACE Lib/uuid.py)
    add_library(uuid_test INTERFACE Lib/test_uuid.py)
endif()
