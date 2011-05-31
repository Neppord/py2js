from distutils.core import setup
setup(name='py2js',
      version='unknown',
      data_files=[(".",["py-builtins.js"])],
      packages=['py2js', 'py2js.compiler'],
      scripts=["pyjs.py"],
      )
