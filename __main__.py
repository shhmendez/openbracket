import argparse 
import sys
from .Backend import Server

sys.dont_write_bytecode = True

parser = argparse.ArgumentParser()
parser.add_argument('-t','--test', action='store_true')
parser.add_argument('--serve', action='store_true')
args = parser.parse_args()

print(args)

if args.test:
  from .Backend.tests import test as back_test
  from .GameEngine.tests import test as ge_test

if args.serve:
  Server.app.serve(port=5000, use_reloader=False, use_meta=True, use_debugger=True)
