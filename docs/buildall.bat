del .\source\pygeotoolbox.*.rst
del .\source\modules.rst

sphinx-apidoc -o ./source ../pygeotoolbox/

del .\source\pygeotoolbox.dataconnectors.*
del .\source\pygeotoolbox.deploy.*
del .\source\pygeotoolbox.workflow.*


call make.bat html
