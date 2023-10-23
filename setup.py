from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "project",
        ["projectcopy.py"],
        extra_compile_args=['/openmp'],
        extra_link_args=['/openmp'],
    )
]

setup(
    name='project',
    ext_modules=cythonize(ext_modules),
)
