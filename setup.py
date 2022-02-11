from setuptools import setup, find_packages, Distribution

Distribution().fetch_build_eggs('versiontag')

from versiontag import get_version, cache_git_tag

cache_git_tag()

setup(
    name="pg_to_evalscript",
    version=get_version(pypi=True),
    packages=["pg_to_evalscript"],
    package_data={"pg_to_evalscript": ["javascript_datacube/*.js", "javascript_processes/*.js"]},
)
