import setuptools

with open('./README.md','r') as file:
    package_description = file.read()

setuptools.setup(
	name = 'TextCleanUp', #this should be unique
	version = '0.1.4',
	author = 'Suraj Yadav',
	author_email = 'sam124.sy@gmail.com',
	description = 'Simplify your text data cleaning process with TextCleanUp',
	long_description = package_description,
	long_description_content_type = 'text/markdown',
	packages = setuptools.find_packages(),
	classifiers = [
	'Programming Language :: Python :: 3',
	'License :: OSI Aproved :: MIT License',
	"Operating System :: OS Independent"],
	python_requires = '>=3.5',
    install_requires=[
        'contractions',
        'spacy',
        'beautifulsoup4',
        'textblob',
        'dask'
    ]
	)