import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='aquarel',
    packages=['aquarel'],
    version='0.0.6',
    license='MIT',
    description='Lightweight templating engine for matplotlib',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Lukas Gienapp',
    author_email='lukas@gien.app',
    url='https://github.com/lgienapp/aquarel',
    project_urls={
        "Bug Tracker": "https://github.com/lgienapp/aquarel/issues"
    },
    package_data={'aquarel': ['themes/*.json']},
    include_package_data=True,
    python_requires='>3.7',
    install_requires=['matplotlib>=3.4.0', 'cycler'],
    keywords=["theme", "plotting", "visualization", "styling", "matplotlib"],
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    download_url="https://github.com/lgienapp/aquarel/archive/refs/tags/v0.0.6.tar.gz",
)