from setuptools import setup

setup(name='aleph_ner',
      version='0.1.0',
      packages=['aleph_ner'],
      install_requires=[
          'Click',
      ],
      entry_points='''
          [console_scripts]
          aleph_ner=aleph_ner.cli:annotate
      ''',
)
