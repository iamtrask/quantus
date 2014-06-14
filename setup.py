from distutils.core import setup, Extension
setup(name='quantus',
      version='0.1',
      packages=['quantus',
                'quantus.main',
                'quantus.main.master',
                  'quantus.main.slave'],

      )