# import ctypes
#
# # Load DLL into memory.
# dll = ctypes.WinDLL("kernel32.dll")
#
# GetStdHandle_p    = ctypes.WINFUNCTYPE(ctypes.c_uint8, ctypes.c_uint8)
# # dllApiParams = (1, "p1", 0), (1, "p2", 0),
#
# ReadFile_p        = ctypes.WINFUNCTYPE(ctypes.c_uint8, ctypes.c_uint8, ctypes.c_wchar_p, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8)
# WriteFile_p       = ctypes.WINFUNCTYPE(ctypes.c_uint8, ctypes.c_uint8, ctypes.c_wchar_p, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8)
# SetConsoleMode_p  = ctypes.WINFUNCTYPE(ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8)
# # dllApiParams = (1, "p1", 0), (1, "p2", 0),
#
# # dllApiParams = (1, "p1", 0), (1, "p2", 0),
#
# GetStdHandleParams = (0)
#
#
# # Actually map the call (setDACValue) to a Python name.
# GetStdHandle = GetStdHandle_p(("GetStdHandle", dll))
# SetConsoleMode = SetConsoleMode_p(("SetConsoleMode", dll))
# ReadFile = ReadFile_p(("ReadFile", dll))
# WriteFile = WriteFile_p(("WriteConsoleW", dll))
# x = GetStdHandle(-11)
# ox = GetStdHandle(-10)
# xx = SetConsoleMode(ox, 0x0004)
# # xxx = ReadFile(x, 0)
# i = 1
#
# print(WriteFile(ox, "Enter your name: ", 17, 0, 0))
# ReadFile(ox, "Enter your name: ", 17, 0, 0)
#
# # Set up the variables and call the Python name with them.
# # p1 = ctypes.c_uint8(1)
# # p2 = ctypes.c_double(4)
#
# # dllApi(p1, p2)
#
#
# # class Console
# #     declare function GetStdHandle(handleKind as int) as int lib kernel32
# #     declare function SetConsoleMode(handle as int, mode as int) as int lib kernel32
# #     declare function ReadFile(handle as int, buff as char(), count as int, taken as int(), reserved as int) as int lib kernel32
# #     declare function WriteFile(handle as int, buff as char(), count as int, taken as int(), reserved as int) as int lib kernel32
# #     private hIn, hOut as int
# #     function Console()
# #         hIn = GetStdHandle(-11);
# #         SetConsoleMode(hId, 0);
# #         // hOut = ...
# #     end function
# #     public function Write(s as String)
# #     end function
# #     public function WriteLine(s as String)
# #     end function
# #     public function ReadLine() as String
# #     end function
# # end class
# #
# # function main()
# #
# # dim con as Console
# # con = Console();
# # con.Write(String("Enter your name: ", 17));
# #
# # dim name as String
# # name = con.ReadLine();
# #
# # dim msg as String
# # msg = String("hello ", 6);
# # msg.Add(name);
# # msg.Add("!", 1);
# #
# # con.WriteLine(msg);
# #
# # con.ReadLine();
#
# # end function


#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" https://stackoverflow.com/questions/878972/windows-cmd-encoding-change-causes-python-crash#answer-3259271
"""
import ctypes
import sys
from ctypes import WINFUNCTYPE, windll, POINTER, byref, c_int
from ctypes.wintypes import BOOL, HANDLE, DWORD, LPWSTR, LPCWSTR, LPVOID

original_stderr = sys.stderr

# GetStdHandle = WINFUNCTYPE(HANDLE, DWORD)(("GetStdHandle", windll.kernel32))
# dll1 = ctypes.WinDLL("kernel32.dll")
dll = ctypes.WinDLL("user32.dll")
args = [ctypes.c_int, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_int]
external_func = WINFUNCTYPE(ctypes.c_int, *args)(("MessageBoxW", dll))
external_func(0, "My New Title", "Test", 1)


#     os.chdir("C:\\Program Files\\Compact Automated Testing System V2.0")
#
# # Load DLL into memory.
# dll = ctypes.WinDLL ("CATS.dll")
#
# # Set up prototype and parameters for the desired function call.
# dllApiProto = ctypes.WINFUNCTYPE (ctypes.c_uint8, ctypes.c_double)
#
# dllApiParams = (1, "p1", 0), (1, "p2", 0),
#
# # Actually map the call (setDACValue) to a Python name.
# dllApi = dllApiProto (("setDACValue", dll), dllApiParams)
#
# # Set up the variables and call the Python name with them.
# p1 = ctypes.c_uint8 (1)
# p2 = ctypes.c_double (4)
#
# dllApi(p1,p2)


# GetStdHandle_p    = ctypes.WINFUNCTYPE(ctypes.c_uint8, ctypes.c_uint8)

# gh = GetStdHandle_p(("GetStdHandle", dll1))

# ReadFile_p        = ctypes.WINFUNCTYPE(ctypes.c_uint8, ctypes.c_uint8, ctypes.c_wchar_p, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8)
# WriteFile_p       = ctypes.WINFUNCTYPE(ctypes.c_uint8, ctypes.c_uint8, ctypes.c_wchar_p, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8)
# SetConsoleMode_p  = ctypes.WINFUNCTYPE(ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8)

# GetStdHandle = GetStdHandle_p(("GetStdHandle", dll1))
# SetConsoleMode = SetConsoleMode_p(("SetConsoleMode", dll1))
# ReadFile = ReadFile_p(("ReadFile", dll1))
# WriteFile = WriteFile_p(("WriteConsoleW", dll1))
# x = GetStdHandle(-11)
# ox = GetStdHandle(-10)
# xx = SetConsoleMode(ox, 0x0004)
# xxx = ReadFile(x, 0)



# STD_OUTPUT_HANDLE = DWORD(-11)
# STD_ERROR_HANDLE = DWORD(-12)
# FILE_TYPE_CHAR = 0x0002
# FILE_TYPE_REMOTE = 0x8000
# GetConsoleMode = WINFUNCTYPE(BOOL, HANDLE, POINTER(DWORD))(("GetConsoleMode", windll.kernel32))
# INVALID_HANDLE_VALUE = DWORD(-1).value
#
# x = GetStdHandle(STD_OUTPUT_HANDLE)
# y = GetConsoleMode(x, byref(DWORD()))
# INVALID_HANDLE_VALUE = DWORD(-1).value
#
# old_stdout_fileno = None
# old_stderr_fileno = None
# if hasattr(sys.stdout, 'fileno'):
#     old_stdout_fileno = sys.stdout.fileno()
# if hasattr(sys.stderr, 'fileno'):
#     old_stderr_fileno = sys.stderr.fileno()
#
# STDOUT_FILENO = 1
# STDERR_FILENO = 2
# real_stdout = (old_stdout_fileno == STDOUT_FILENO)
# real_stderr = (old_stderr_fileno == STDERR_FILENO)
#
# hStdout = GetStdHandle(STD_OUTPUT_HANDLE)
# hStderr = GetStdHandle(STD_ERROR_HANDLE)
#
# WriteConsoleW = WINFUNCTYPE(BOOL, HANDLE, LPWSTR, DWORD, POINTER(DWORD), LPVOID)(("WriteConsoleW", windll.kernel32))
# retval = WriteConsoleW(STD_OUTPUT_HANDLE, '123456', 6, byref(6), None)


# GetCommandLineW = WINFUNCTYPE(LPWSTR)(("GetCommandLineW", windll.kernel32))
# CommandLineToArgvW = WINFUNCTYPE(POINTER(LPWSTR), LPCWSTR, POINTER(c_int))(("CommandLineToArgvW", windll.shell32))
#
# argc = c_int(0)
# argv_unicode = CommandLineToArgvW(GetCommandLineW(), byref(argc))

#