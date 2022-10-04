import importlib
import inspect
from pathlib import Path

import pytest


route_features = [
    "route",
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "head",
    "options",
]
features = [
    f"{prefix}.{feature}"
    for prefix in ["app", "bp"]
    for feature in route_features
]


def get_all_handlers_and_tests():
    blueprints_folder = (
        Path(__file__).parent.parent / "bifolio" / "blueprints"
    )

    routes_handlers = []

    for script in filter(
        lambda x: x.is_file() and x.name != "__init__.py",
        blueprints_folder.rglob("*.py"),
    ):
        module = importlib.import_module(
            f"bifolio.blueprints.{script.stem}"
        )

        iterable = (
            obj
            for obj in inspect.getmembers(module, inspect.isfunction)
            if (obj[1].__module__ == module.__name__)
        )

        for name, func in iterable:
            if any(
                [
                    feature in inspect.getsource(func)
                    for feature in features
                ]
            ):
                routes_handlers.append(name)

    tests_folder = Path(__file__).parent.parent / "tests"

    exists_tests_functions = []

    for script in filter(
        lambda x: x.is_file() and x.name != "__init__.py",
        tests_folder.rglob("*.py"),
    ):
        module = importlib.import_module(f"tests.{script.stem}")

        iterable = (
            obj
            for obj in inspect.getmembers(module, inspect.isfunction)
            if (
                obj[1].__module__ == module.__name__
                and obj[0].startswith("test_")
            )
        )

        for name, func in iterable:
            exists_tests_functions.append(name)

    return routes_handlers, exists_tests_functions


ROUTES_HANDLERS, EXISTS_TESTS_FUNCTIONS = get_all_handlers_and_tests()


@pytest.mark.skip(reason="Was implemented completely in future")
@pytest.mark.parametrize("handler", ROUTES_HANDLERS)
def test_routes_handlers(handler):
    assert (
        f"test_{handler}" in EXISTS_TESTS_FUNCTIONS
    ), f"Not found test for {handler}"
