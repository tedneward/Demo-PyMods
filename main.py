#!/usr/bin/env python3
import os
import types

def choose(prompt):
    print(prompt)
    return input(">>> ")

allowed_builtins = {
    "__builtins__": {
        "min": min,
        "len": len,
        "choose": choose,
        "print": print,
    }
}

modules = {}
def loadmodule(filename, modulename):
    def parsemd(mdfilename):
        pythoncode = ""
        with open(mdfilename) as mdfile:
            lines = mdfile.readlines()
            codeblock = False
            for line in lines:
                if line[0:3] == "```":
                    codeblock = not codeblock
                    continue

                if codeblock == True:
                    pythoncode += line

        if pythoncode == "":
            print("WARNING: No literate Python found")

        return pythoncode

    def builddict(codeobj):
        moduledict = {}; count = 0
        for name in codeobj.co_names:
            element = codeobj.co_consts[count]
            if isinstance(element, types.CodeType):
                moduledict[name] = types.FunctionType(element, globals=allowed_builtins)
            else:
                moduledict[name] = element
            count += 1
        return moduledict

    literatecode = parsemd(filename)
    codeobj = compile(literatecode, modulename, 'exec')
    return builddict(codeobj)

def main():
    files = os.listdir("plugins")
    for f in files:
        filename = "plugins/" + f
        if os.path.isfile(filename) and os.path.splitext(filename)[1] == '.md':
            modulename = os.path.splitext(f)[0]
            modules[modulename] = loadmodule(filename, modulename)

    print(modules['interactivestuff']['name'])
    print(modules['interactivestuff']['interact']())

main()
