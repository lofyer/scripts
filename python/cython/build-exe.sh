#!/bin/bash
C:\Python31\python.exe C:\Python31\Scripts\cython.py smalltest1.py --embed cl.exe  /nologo /Ox /MD /W3 /GS- /DNDEBUG -Ic:\Python31\include -Ic:\Python31\PC /Tcsmalltest1.c /link /OUT:"test.exe" /SUBSYSTEM:CONSOLE /MACHINE:X86 /LIBPATH:c:\Python31\libs /LIBPATH:c:\Python31\PCbuild
