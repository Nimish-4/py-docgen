import pathlib
from typing import List, Optional, Tuple

import libcst as cst

from libcst.metadata import PositionProvider

from docgen.templates import (
    DOCSTRING_FOR_CLASS,
    DOCSTRING_FOR_FUNCTION,
    DOCSTRING_FOR_CLASS_FULL,
    DOCSTRING_FOR_FUNCTION_FULL,
)


class FunctionAndClassVisitor(cst.CSTTransformer):
    """
    Class for parsing and modifying code inside a module.

    The code is parsed using the parser from libcst. CST in this context is a
    Concrete Syntax Tree. While parsing, we keep track of the indentation
    level using LibCST's MetaDataWrapper, which is used to correctly place the
    docstring inside the class or method.

    The visitor does not modify any function/class inside another function. Only
    outer level functions and classes (along with their methods) are modified.

    Arguments
    ---------
    file_path: pathlib.Path
        Path location of module.

    """

    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(
        self,
        file_path: pathlib.Path = pathlib.Path.cwd(),
        full_doc: bool = False,
    ):

        self.stack: List[Tuple[str, ...]] = []
        self.missing_docstrings = []
        self.indent_level = 0  # track no. of whitespaces at current level
        self.file_path = file_path
        self.full_doc = full_doc
        if full_doc is False:
            self.class_docstring = DOCSTRING_FOR_CLASS
            self.function_docstring = DOCSTRING_FOR_FUNCTION
        else:
            self.class_docstring = DOCSTRING_FOR_CLASS_FULL
            self.function_docstring = DOCSTRING_FOR_FUNCTION_FULL

    def _build_normal_docstring(self, raw_text: str, indent_ws: str) -> str:

        lines = raw_text.strip("\n").splitlines()
        formatted_lines = ['"""' + lines[0]]
        num_whitespaces = indent_ws
        for line in lines[1:]:

            if line.strip() == "":  # skip unnecessary indentation for empty lines
                formatted_lines.append(line)
            else:
                formatted_lines.append(num_whitespaces + line)

        formatted_lines.append(num_whitespaces + '"""')
        return "\n".join(formatted_lines)

    def _build_parametric_docstring(
        self, raw_text: str, indent_ws: str, parameters=None
    ):

        lines = raw_text.strip("\n").splitlines()
        formatted_lines = ['"""' + lines[0]]

        for line in lines[1:]:

            if not line.strip():  # skip unnecessary indentation for empty lines
                formatted_lines.append(line)

            elif line.strip() == "Parameters" and parameters is not None:
                formatted_lines.append(indent_ws + "Parameters")
                formatted_lines.append(indent_ws + "----------")

                if parameters == ():
                    formatted_lines.append("")
                    continue

                for p in parameters:
                    name = p.name.value
                    if name.strip() == "self":
                        continue
                    line_1 = indent_ws + f"{name}: type (default:)"
                    line_2 = indent_ws + f"    Explanation of {name}."
                    formatted_lines.append(line_1)
                    formatted_lines.append(line_2)
                    formatted_lines.append("")
            else:
                formatted_lines.append(indent_ws + line)

        formatted_lines.append(indent_ws + '"""')
        return "\n".join(formatted_lines)

    def _get_indent_level(self, node: cst.CSTNode) -> int:
        pos = self.get_metadata(PositionProvider, node.body)
        return pos.start.column

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.indent_level = self._get_indent_level(node)
        self.stack.append(node)
        return True

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.CSTNode:

        self.indent_level = self._get_indent_level(original_node)
        indent_ws = self.indent_level * " "

        if original_node.get_docstring() is not None:
            return updated_node

        self.missing_docstrings.append(("class", original_node.name.value))

        # Determine indentation based on the body
        if self.full_doc is False:
            final_docstring = self._build_normal_docstring(
                self.class_docstring, indent_ws
            )
        else:
            final_docstring = self._build_normal_docstring(
                self.class_docstring, indent_ws
            )

        docstring_stmt = cst.SimpleStatementLine(
            body=[cst.Expr(value=cst.SimpleString(final_docstring))],
        )
        new_body = updated_node.body.with_changes(
            body=[docstring_stmt] + list(updated_node.body.body)
        )

        return updated_node.with_changes(body=new_body)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.indent_level = self._get_indent_level(node)
        self.stack.append(node)
        # Do not visit functions/classes inside functions
        return False

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:

        self.indent_level = self._get_indent_level(original_node)
        indent_ws = self.indent_level * " "

        if original_node.get_docstring() is not None:
            return updated_node
        self.missing_docstrings.append(("function", original_node.name.value))

        if self.full_doc is False:
            final_docstring = self._build_parametric_docstring(
                self.function_docstring,
                indent_ws,
                parameters=original_node.params.params,
            )
        else:
            final_docstring = self._build_parametric_docstring(
                self.function_docstring,
                indent_ws,
                parameters=original_node.params.params,
            )

        docstring_stmt = cst.SimpleStatementLine(
            body=[cst.Expr(value=cst.SimpleString(final_docstring))],
        )
        new_body = updated_node.body.with_changes(
            body=[docstring_stmt] + list(updated_node.body.body)
        )
        return updated_node.with_changes(body=new_body)

    @classmethod
    def _store_missing_docstrings(cls, file_path: pathlib.Path) -> cst.Module:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        module = cst.parse_module(source_code)

        visitor = cls(file_path=file_path)
        module.visit(visitor)

        return visitor
