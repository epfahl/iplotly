from setuptools import setup, find_packages

setup(name='iplotly',
      version='0.1',
      description='An object-oriented interface to Plotly.',
      url='https://github.com/epfahl/iplotly',
      author='Eric Pfahl',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['plotly', 'pyyaml'],
      package_data={'iplotly': ['defaults.yml']})
