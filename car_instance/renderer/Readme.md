### Instruction for renderer
We modify the renderer based on the render crom from the code provided by [displet](http://www.cvlibs.net/projects/displets/)

Two things are modified: (1) we give the renderer a python wrapper (2) we provide an egl context so the the render can be performed off-screen.

Tested with Ubuntu 14.04 and Python 2.7. For other versions, we haven't tested it.

