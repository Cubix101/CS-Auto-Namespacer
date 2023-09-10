# CS Auto Namespacer
A python script for adding namespaces to multiple .cs files without them all at once.

The script will recursively crawl a given input folder for all .cs files, and detect those without namespaces. It will then generate a namespace using the folder structure, relative to the input folder, plus a given root namespace (if supplied). A new file is then generated with the namespace added after the first line that is not a using statement, along with a final closing curly brace at the end of the file. This file is generated in the given output folder, with respect to relative directory structure.

This script is designed to be used as a command line tool. Input folder, output folder, and root namespace are supplied as command line arguments. All given directories are relative to the current working directory. Arguments are as follows:

**-r: The root namespace. This is a base namespace applied before folder any folder structures.**

**-i: The input folder, relative to the current working directory. This will be used to determine how to namespace a file. E.g, '/Scripts/Player/Movement.cs' relative to /Scripts will recieve 'namespace [Root Namespace].Player.Movement'**

**-o: The output folder, relative to the current working directory. Directory structure will mimic input folder, allowing for as clean as possible a transition when you decide to replace your original non-namespaced scripts.**

You can also use the **-h** argument to recieve an explanation of the arguments from the command line.

As an example of how you would use the script, you could have a ``C:/Me/Home/Stuff/Scripts`` folder, and you want all the scripts to go into the namespace ``MeStuff``. This could be achieved by opening ``C:/Me/Home/Stuff`` in the terminal, then running the command:

```C:/Me/Home/Stuff>py [ScriptPath]/AutoNamespacer.py -i Scripts -o ScriptsOutput -r MeStuff```

This would then search for all .cs files in the Scripts folder and add the namespace.
