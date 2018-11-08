from setuptools import setup

dependencies = ['PyInquirer']

setup(
    name='albus',
    version='0.1.0',
    url='https://github.com/mbloom/albus',
    author='Matt Bloom, Manit Hirani, Brandon May',
    author_email='',
    description='Troubleshooting wizard',
    long_description=__doc__,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'albus = albus.main:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
