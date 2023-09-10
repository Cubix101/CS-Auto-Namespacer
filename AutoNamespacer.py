import os, sys, getopt

# Tool for automatically adding namespaces to C# files without one. Uses the running directory as script root.
# The script works by inserting the 'namespace' line after the final using statement, then a closing curly brace at the end of the file, wrapping all the file contents in the namespace.

namespaceTemplate = "namespace {0}\n{{"

def SanitiseDirectory (originalDirectory:str, runningDirectory):
    originalDirectory = os.path.join(runningDirectory, originalDirectory)
    return originalDirectory

def WalkRecursively(directory:str, relativeTo:str, rootNamespace:str, inputDirectory:str, outputDirectory:str):
    for root, dirs, files in os.walk(directory):
        for name in files:
            if (name.split(".")[-1] == "cs"):
                fullDirectory = os.path.join(root, name)
                relativeDirectory = os.path.relpath(fullDirectory, relativeTo)
                InsertNamespace(relativeDirectory, fullDirectory, rootNamespace, inputDirectory, outputDirectory)
        for dir in dirs:
            WalkRecursively(dir, relativeTo, rootNamespace, inputDirectory, outputDirectory)

def InsertNamespace(relativeFilePath:str, fullFilePath:str, rootNamespace:str, inputDirectory:str, outputDirectory:str):
    print(f"Namespacing file {relativeFilePath}")

    fileName = "\\" + relativeFilePath.split("\\")[-1]
    namespace = relativeFilePath.removesuffix(fileName).replace("\\", ".")
    if (rootNamespace != ""):
        namespace = rootNamespace + "." + namespace

    fileRead = open(fullFilePath, "r")
    entireContents = fileRead.read()

    if ("namespace" in entireContents):
        print("File already contains a namespace!")
        return

    fileContentsByLine = entireContents.split("\n")
    fileRead.close()

    # Get line to add namespace
    namespaceInsertionLine = -1
    currentLineIndex = 0
    while (namespaceInsertionLine == -1):
        if not fileContentsByLine[currentLineIndex].startswith("using"):
            namespaceInsertionLine = currentLineIndex + 1
        
        currentLineIndex += 1

    # Indent all following lines
    for i in range(namespaceInsertionLine, len(fileContentsByLine)):
        fileContentsByLine[i] = "\t" + fileContentsByLine[i]

    # Insert namespace line
    fileContentsByLine.insert(namespaceInsertionLine, namespaceTemplate.format(namespace))
    # Add closing curly brace
    fileContentsByLine.append("}")
    fullOutputPath = os.path.join(outputDirectory, relativeFilePath)

    os.makedirs(os.path.dirname(fullOutputPath), exist_ok=True)
    fileWrite = open(fullOutputPath, "w")
    fileWrite.write("\n".join(fileContentsByLine))

def Run (inputDirectory, outputDirectory, rootNamespace):
    runningDirectory = os.getcwd()
    inputDirectory = SanitiseDirectory(inputDirectory, runningDirectory)
    outputDirectory = SanitiseDirectory(outputDirectory, runningDirectory)
    WalkRecursively(inputDirectory, inputDirectory, rootNamespace, inputDirectory, outputDirectory)

def Help():
    print("This is a tool for automatically adding namespaces to non-namespaced .cs files. It converts relative folder structure into a namespace, and surrounds all the contents of the script from the final using statement.")
    print("Make sure your output folder is different to your input folder, to ensure you don't damage any files or cause issues should the script go wrong (I'm not a python dev, this was just the quickest way i could think to do this.)")
    print("Args:")
    print("-r: The root namespace. This is a base namespace applied before folder any folder structures. See below for more info.")
    print("-i: The input folder, relative to the current running directory. This will be used to determine how to namespace a file. E.g, '/Scripts/Player/Movement.cs' relative to /Scripts will recieve 'namespace [Root Namespace].Player.Movement'")
    print("-o: The output folder, relative to the current running directory. Directory structure will mimic input folder, allowing for as clean as possible a transition when you decide to replace your original non-namespaced scripts.")

def Main():
    # Inputs are supplied via command line args.
    rootNamespace = ""
    outputDirectory = ""
    inputDirectory = ""

    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "i:o:r:h:")
    for opt, arg in opts:
        if opt in ['-h']:
            Help()
            return
        elif opt in ['-i']:
            inputDirectory = arg
        elif opt in ['-o']:
            outputDirectory = arg
        elif opt in ['-r']:
            rootNamespace = arg

    if (inputDirectory == ""):
        print ("No input directory supplied!")
        return
    
    if (outputDirectory == ""):
        print("No output directory supplied!")
        return

    if (rootNamespace == ""):
        print("No root namespace supplied!")
        return

    Run(inputDirectory, outputDirectory, rootNamespace)

Main()