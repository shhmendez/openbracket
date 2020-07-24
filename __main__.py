import argparse 
import sys
from openbracket.Backend import Server

sys.dont_write_bytecode = True

parser = argparse.ArgumentParser()
parser.add_argument('-t','--test', action='store_true')
parser.add_argument('--serve', action='store_true')
args = parser.parse_args()

print(args)

if args.test:
  import unittest
  print("="*40)
  print("running backend tests...")
  from .Backend.tests import test as back_test
  suite = unittest.TestSuite()
  suite.addTest(back_test.Tests)
  print("done running backend tests")
  print("="*40)
  print("="*40)
  print("running Engine tests...")
  from .GameEngine.tests import test as ge_test
  print("done running Engine tests")
  print("="*40)
 
if args.serve:
  Server.app.serve(port=5000, use_reloader=False, use_meta=True, use_debugger=True)
