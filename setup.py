from distutils.core import setup

setup(
    name='aux2mongodb',
    version='0.0.1',
    description='A module to read in fact aux data and put them into a mongodb',
    url='http://github.com/fact-project/aux2mongodb',
    author='Maximilian Noethe',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    packages=['aux2mongodb', 'aux2mongodb.auxservices'],
    package_data={
        '': ['resources/*', 'credentials/credentials.encrypted']},
    install_requires=[
        'astropy',
        'pandas',
        'yaml',
        'pymongo',
        'docopt',
    ],
    entry_points={
        'console_scripts': [
            'fact_aux2mongodb = aux2mongodb.__main__:main'
        ]
    },
    zip_safe=False,
)
