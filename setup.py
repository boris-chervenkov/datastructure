import os
import setuptools
from setuptools.command import sdist
import subprocess
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, CURRENT_DIR)

DOCS_FILENAME = 'docs.md'


class Sdist(sdist.sdist):
    '''Generate Markdown documentation '''

    def run(self):
        docs_filename = os.path.join(CURRENT_DIR, DOCS_FILENAME)

        docs_process = subprocess.run(
            [
                'pdoc',
                os.path.join(CURRENT_DIR, 'datastructure.py')
            ],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        docs_output_str = docs_process.stdout

        try:
            with open(docs_filename, 'r', encoding='utf-8') as f:
                docs_from_file = f.read()
        except:
            print("! Docs do not exist", file=sys.stderr)
            docs_from_file = ''

        # only save docs if changed
        if docs_from_file != docs_output_str:
            with open(docs_filename, 'w', encoding='utf-8') as f:
                f.write(docs_output_str)

        super().run()



if __name__ == "__main__":
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="datastructure",
        version="1.6.0",
        author="Boris Chervenkov",
        author_email="boris.chervenkov@gmail.com",
        description="Easy manipulation of nested data structures",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=['.'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: Proprietary",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        extras_require={
            'dev': [
                'pdoc'
            ]
        },
        cmdclass={
            'sdist': Sdist,
        },
        include_package_data=True,
    )