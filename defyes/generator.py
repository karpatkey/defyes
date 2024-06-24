import importlib.resources as pkg_resources
import itertools
import json
import keyword
import re
import textwrap
from pathlib import Path


def get_module_path(module_file):
    return Path(module_file).resolve().parent


current_module_path = get_module_path(__file__)


def get_defabipedia_path(protocol):
    try:
        with pkg_resources.path(f"defabipedia.{protocol}", "") as dir_path:
            if dir_path.exists() and dir_path.is_dir():
                return dir_path
    except (ModuleNotFoundError, FileNotFoundError):
        pass
    return None


def load_abi(module_file_path, abi_filename):
    protocol_path = get_module_path(module_file_path)
    defabipedia_path = get_defabipedia_path(protocol_path.name)

    path = protocol_path / "abis" / abi_filename
    if not path.exists():
        path = defabipedia_path / abi_filename if defabipedia_path else None
    if path is None:
        raise FileNotFoundError

    with open(path) as f:
        return f.read()


def snake_to_camel(snake_case):
    words = snake_case.split("_")
    camel_case = "".join(word.title() for word in words)
    return camel_case


def camel_to_snake(camel_case):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_case)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def args_name_gen(used_names: set, start: int = 0):
    used_names_ = set(used_names)
    for index in itertools.count(start=start):
        name = f"arg{index}"
        while name in used_names_:
            name += "_"
        yield name
        used_names_.add(name)


def filter_abi_items(abi_list, always_include_methods):
    for item in abi_list:
        inputs = item.get("inputs", None)
        method_name = item.get("name", None)
        if item["type"] in ["constructor", "receive", "error", "event"]:
            continue

        if (
            inputs is not None
            and method_name is not None
            and (method_name in always_include_methods or item.get("stateMutability") != "nonpayable")
            and method_name != "class"
        ):
            yield item


def process_method_name(method_name, method_names):
    method_name_snake = camel_to_snake(method_name)
    if method_name_snake == "list":
        method_name_snake = "_list"

    n = 1
    while method_name_snake in method_names:
        method_name_snake = f"{method_name_snake}_{n}"
        n += 1

    return method_name_snake


def process_arguments(inputs, type_conversion):
    args = []
    args_names = []
    awesome_names = args_name_gen(used_names=set(arg.get("name", "") for arg in inputs))
    for arg, auto_name in zip(inputs, awesome_names):
        arg_name = camel_to_snake(arg.get("name") or auto_name)
        if keyword.iskeyword(arg_name):
            arg_name += "_"
        arg_type = type_conversion.get(arg["type"], arg["type"])
        args.append(f"{arg_name}: {arg_type}")
        args_names.append(arg_name)
    return args, args_names


def process_return_types(outputs, type_conversion):
    if not outputs:
        return "", ""
    return_types = [type_conversion.get(output["type"], output["type"]) for output in outputs]
    return_names = [output.get("name", "") for output in outputs]
    return_str = f" -> {return_types[0]}" if len(return_types) == 1 else f' -> tuple[{", ".join(return_types)}]'
    return_docstring = (
        "\n            ".join(textwrap.wrap(f'Output: {", ".join(return_names)}')) if return_names[0] != "" else ""
    )
    return return_str, return_docstring


def construct_method_string(
    original_method_name, method_name, args, args_names, return_str, return_docstring, is_const_call
):
    args_str = ", " + ", ".join(args) if args else ""
    args_names = ", ".join(args_names) if args_names else ""
    method_str = "    @property\n" if not args else ""
    method_str += f"    def {method_name}(self{args_str}){return_str}:\n"
    method_str += f'        """\n            {return_docstring}\n        """\n' if return_docstring else ""
    if is_const_call:
        method_str += f"        return const_call(self.contract.functions.{original_method_name}({args_names}))\n"
    else:
        method_str += f"        return self.contract.functions.{original_method_name}({args_names}).call(block_identifier=self.block)\n"
    return method_str


def generate_methods_from_abi(abi_path, const_call_methods=[], always_include_methods=[]):
    TYPE_CONVERSION = {
        "uint8": "int",
        "uint64": "int",
        "uint16": "int",
        "uint32": "int",
        "uint96": "int",
        "uint256": "int",
        "uint112": "int",
        "int104": "int",
        "int256": "int",
        "uint128": "int",
        "uint208": "int",
        "uint40": "int",
        "uint64[]": "list[int]",
        "uint256[]": "list[int]",
        "int256[]": "list[int]",
        "address": "str",
        "address[]": "list[str]",
        "string": "str",
        "bytes32": "bytes",
        "bytes32[]": "list[bytes]",
        "bytes4": "bytes",
        "tuple[]": "list[tuple]",
    }
    with open(abi_path) as f:
        abi_list = json.load(f)

    methods = []
    method_names = []

    for item in filter_abi_items(abi_list, always_include_methods):
        method_name_snake = process_method_name(item["name"], method_names)
        method_names.append(method_name_snake)
        args, args_names = process_arguments(item["inputs"], TYPE_CONVERSION)
        return_str, return_docstring = process_return_types(item.get("outputs", []), TYPE_CONVERSION)
        method_str = construct_method_string(
            item["name"],
            method_name_snake,
            args,
            args_names,
            return_str,
            return_docstring,
            item["name"] in const_call_methods,
        )
        methods.append(method_str)

    return "\n".join(methods)


header_template = """
'''
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import %(classes)s

# Optionally
class %(first_class)s(%(first_class)s):
    ...
'''

from web3 import Web3

from defyes.generator import load_abi
from karpatkit.node import get_node
"""

contract_class_template = """

class %(name)s:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError(
                    "No default_addresses defined when trying to guess the address."
                ) from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, %(abi)r))\n
"""


def generate_contract_class(class_name, abi_path, const_call_methods=[], always_include_methods=[]):
    abi_filename = abi_path.name
    result = contract_class_template % dict(name=class_name, abi=abi_filename)
    result += generate_methods_from_abi(abi_path, const_call_methods, always_include_methods)
    return result


def generate_classes():
    import black  # Because it's used just during development
    import isort  # Because it's used just during development

    setup_paths = current_module_path.glob("**/autogen_config.json")
    black_config = get_black_config()

    for setup_path in setup_paths:
        is_const_call_used = False

        protocol_path = setup_path.parent
        autogenerated_module_path = protocol_path / "autogenerated.py"
        defabipedia_path = get_defabipedia_path(protocol_path.name)

        with open(setup_path) as f:
            abis_to_process = json.load(f)

        content = ""
        classes_name = []
        for abi_name, config in abis_to_process.items():
            abi_path = protocol_path / "abis" / f"{abi_name}.json"
            if not abi_path.exists():
                abi_path = defabipedia_path / f"{abi_name}.json" if defabipedia_path else None
            class_name = snake_to_camel(abi_name)
            classes_name.append(class_name)
            const_call_methods = config.get("const_call", [])
            always_include_methods = config.get("always_include", [])
            if const_call_methods:
                is_const_call_used = True
            content += generate_contract_class(class_name, abi_path, const_call_methods, always_include_methods)

        if not content:
            continue

        final_header_template = header_template
        if is_const_call_used:
            final_header_template += "from karpatkit.cache import const_call\n"

        content = final_header_template % dict(classes=", ".join(classes_name), first_class=classes_name[0]) + content
        content = isort.code(content)
        content = black.format_file_contents(content, fast=True, mode=black_config)
        with open(autogenerated_module_path, "w") as f:
            f.write(content)
        relative_module_path = autogenerated_module_path.relative_to(Path().resolve())
        print(f"{relative_module_path} was created/updated.")


def get_black_config():
    import black  # Because it's used just during development

    pyproject_toml = black.find_pyproject_toml(".")
    conf_dict = black.parse_pyproject_toml(pyproject_toml)
    target_versions_strings = conf_dict.pop("target_version", ["py310"])
    target_versions = set(
        next(t for t in black.TargetVersion if t.name.lower() == target_version_str)
        for target_version_str in target_versions_strings
    )
    return black.Mode(target_versions=target_versions, **conf_dict)


if __name__ == "__main__":
    generate_classes()
