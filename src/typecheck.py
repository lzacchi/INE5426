#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi

# Structures used to check if binary operations
# are made using valid types


from data import TreeNode
from output import InvalidBinaryOperation, parse_arguments


def check_valid_operation(
    left: TreeNode, right: TreeNode, operation: str, lineno: int
) -> str:
    valid_operations = {
        "+": [
            {"left": "int", "right": "int", "result": "int"},
            {"left": "float", "right": "float", "result": "float"},
            {"left": "string", "right": "string", "result": "string"},
            {"left": "float", "right": "int", "result": "float"},
            {"left": "int", "right": "float", "result": "float"},
        ],
        "-": [
            {"left": "int", "right": "int", "result": "int"},
            {"left": "float", "right": "float", "result": "float"},
            {"left": "float", "right": "int", "result": "float"},
            {"left": "int", "right": "float", "result": "float"},
        ],
        "*": [
            {"left": "int", "right": "int", "result": "int"},
            {"left": "float", "right": "float", "result": "float"},
            {"left": "float", "right": "int", "result": "float"},
            {"left": "int", "right": "float", "result": "float"},
        ],
        "/": [
            {"left": "int", "right": "int", "result": "int"},
            {"left": "float", "right": "float", "result": "float"},
            {"left": "float", "right": "int", "result": "float"},
            {"left": "int", "right": "float", "result": "float"},
        ],
        "%": [
            {"left": "int", "right": "int", "result": "int"},
        ],
    }
    op_list = valid_operations.get(operation)
    if op_list is None:
        raise InvalidBinaryOperation(f"invalid operation {operation}")
    result = list(
        filter(
            lambda op: op["left"] == left.res_type and op["right"] == right.res_type,
            op_list,
        )
    )
    if len(result) == 0:
        raise InvalidBinaryOperation(
            f"\nCan't operate [{left.res_type}] ({left.value}) '{operation}' [{right.res_type}] ({right.value})] at line {lineno}"
        )
    if parse_arguments().print_typecheck:
        print(
            f"Line {lineno}: [{left.res_type}] ({left.value}) '{operation}' [{right.res_type}] ({right.value})] is a VALID operation"
        )
    return result[0]["result"]
