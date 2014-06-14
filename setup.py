from distutils.core import setup
setup(name='quantus',
      version='0.1',
      py_modules=['quantus.main.master.Master',
                  'quantus.main.master.matrix',
                  'quantus.main.master.subvector',
                  'quantus.main.master.vector',
                  'quantus.main.slave.Slave',
                  'quantus.main.slave.subvector'],
      )