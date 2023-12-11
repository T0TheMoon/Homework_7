from setuptools import setup, find_namespace_packages

setup(name='Cleannerfolder777',
      version='0.0.3',
      description='Clean folder program by Python',
      url='https://github.com/T0TheMoon',
      author='Vorobyov Victor',
      author_email='vorobyov.vik06@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=['markdown'],
      include_package_data=True,
      entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
      )   