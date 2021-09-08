from data import TreeNode

# TODO: fazer enum pra param operation
def check_valid_operation(left: TreeNode, right: TreeNode, operation: str, lineno: int) -> str:
    valid_operations = {
        "+": [
            {left: "int", right: "int", result: "int"},
            {left: "float", right: "float", result: "float"},
            {left: "string", right: "string", result: "string"},
            {left: "float", right: "int", result: "float"},
            {left: "int", right: "float", result: "float"},
        ],
        "-": [
            {left: "int", right: "int", result: "int"},
            {left: "float", right: "float", result: "float"},
            {left: "float", right: "int", result: "float"},
            {left: "int", right: "int", result: "float"},
        ],
        "*": [
            {left: "int", right: "int", result: "int"},
            {left: "float", right: "float", result: "float"},
            {left: "float", right: "int", result: "float"},
            {left: "int", right: "float", result: "float"},
        ],
        "/": [
            {left: "int", right: "int", result: "int"},
            {left: "float", right: "float", result: "float"},
            {left: "float", right: "int", result: "float"},
            {left: "int", right: "int", result: "float"},
        ],
        "%": [
            {left: "int", right: "int", result: "int"},
        ]
    }
    op_list = valid_operations.get(operation)
    result = filter(lambda op : op.left == left.result_type and op.right == right.result_type, op_list)
