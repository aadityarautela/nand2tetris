import CompilationEngine, JackTokenizer
import sys, glob

class JackAnalyzer(object):
    def __init__(self,infile, outfile):
        self.compengine = CompilationEngine.CompilationEngine(infile, outfile)


if len(sys.argv) < 2:
    print("Missing File or Directory")
    sys.exit(0)

filename_or_dir = sys.argv[1]
isfile = False
isslashdir = False

filelist = []

if filename_or_dir.endswith(".jack"):
    isfile = True
    filelist.append(filename_or_dir)

elif filename_or_dir.endswith("/"):
    isslashdir = True

if not isfile:
    if isslashdir:
        filelist = glob.glob(filename_or_dir + "*.jack")
    else:
        filelist = glob.glob(filename_or_dir + "/*.jack")

for fname in filelist:
    J = JackAnalyzer(fname, fname.replace(".jack", ".xml"))
