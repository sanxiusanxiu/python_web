from setuptools import find_packages, setup

'''
packages 告诉 Python 包括哪些包目录（以及它们包含的 Python 文件）。
find_packages() 会自动找到这些目录，所以你不用逐个写出。
要加入其他文件，比如静态文件和模板目录，就要设置 include_package_data。
Python需要另外一个叫做 MANIFEST.in 的文件来指明具体的其他文件是哪些。

MANIFEST.in 会告诉 Python 复制 static 和 templates 目录下的所有文件以及 schema.sql 文件，
但是排除所有字节码（bytecode）文件。
'''

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
