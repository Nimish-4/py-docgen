from pathlib import Path

import libcst as cst

from docstrings.generator import FunctionAndClassVisitor


def process_module(file_path: str) -> bool:
    try:
        path = Path(file_path)
        source_code = path.read_text(encoding="utf-8")

        try:
            module = cst.parse_module(source_code)
        except Exception as parse_err:
            print(f"Skipping {file_path} (parse error): {parse_err}")
            return False

        visitor = FunctionAndClassVisitor(file_path=file_path)
        modified_module = module.visit(visitor)

        # check if the code has been modified
        if modified_module.code != source_code:
            path.write_text(modified_module.code, encoding="utf-8")
            print(f"Updated {file_path}")
        else:
            print(f"No changes in {file_path}")

        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def check_module(file_path: str) -> bool:
    try:
        path = Path(file_path)

        try:
            module = FunctionAndClassVisitor()._store_missing_docstrings(path)
            if module and module.missing_docstrings:
                print(f"Missing docstrings in {module.file_path}:")
                for kind, name in module.missing_docstrings:
                    print(f"  {kind} '{name}'")

        except Exception as parse_err:
            print(f"Skipping {file_path} (parse error): {parse_err}")
            return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False
