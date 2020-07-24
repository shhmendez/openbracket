cd ..; 
find Backend GameEngine | grep -v __pycache__ | entr -rc nosetests
