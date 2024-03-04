""" """

from dagster import load_assets_from_package_module

from . import core, recommenderer

core_assets = load_assets_from_package_module(
    package_module=core,
    group_name="core",
)

recommender_assets = load_assets_from_package_module(
    package_module=recommenderer,
    group_name="recommender",
)
