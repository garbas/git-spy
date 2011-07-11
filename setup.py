from setuptools import setup

version = '0.1'

setup(
    name='git-spy',
    version=version,
    description="Spy / Monitor git repositories.",
    long_description=open("README.rst").read(),
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        #"Programming Language :: Python :: 2.7",
        #"Programming Language :: Python :: 3.2",
        ],
    keywords='git monitor',
    author='Rok Garbas',
    author_email='rok@garbas.si',
    url='https://github.com/garbas/git-spy',
    license='BSD',
    packages=['gitspy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'argparse',
        'argh',
        'GitPython',
        ],
    entry_points="""
        [console_scripts]
        git-spy = gitspy:main
        git-spy-daemon = gitspy.daemon:main
        """,
    )
