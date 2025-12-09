import importlib
import inspect
from pathlib import Path
from typing import Any, get_args, get_origin

import pytest
from pydantic import BaseModel


def test_dict_attributes_are_documented():
    """
    Test function that iterates through all model modules and shortcuts,
    finding all classes that descend from BaseModel and printing their names.
    """
    # Get the path to the models directory
    models_dir = Path(__file__).parent.parent / "src" / "owui_client" / "models"

    # Import all model modules
    model_modules = []
    for file_path in models_dir.glob("*.py"):
        if file_path.name != "__init__.py":
            module_name = f"owui_client.models.{file_path.stem}"
            try:
                module = importlib.import_module(module_name)
                model_modules.append(module)
            except ImportError as e:
                print(f"Failed to import {module_name}: {e}")

    # Import shortcuts module
    try:
        shortcuts_module = importlib.import_module("owui_client.shortcuts")
        model_modules.append(shortcuts_module)
    except ImportError as e:
        print(f"Failed to import owui_client.shortcuts: {e}")

    dictattrs_without_documentation: dict[str, list[dict]] = {}

    # Iterate through all modules and find BaseModel subclasses
    for module in model_modules:
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Check if it's a BaseModel subclass but not BaseModel itself
            if (
                issubclass(obj, BaseModel)
                and obj.__module__ == module.__name__
                and obj is not BaseModel
            ):
                attrs = extract_attributes(obj)

                # Iterate through each attribute locating dict attrs that lack documentation
                for attr_info in attrs.values():
                    if (
                        attr_info["base_type"] == "dict"
                        or attr_info["sub_type"] == "dict"
                    ):
                        if not has_dict_fields_documentation(attr_info["docstr"]):
                            key = module.__name__ + "." + name
                            if key not in dictattrs_without_documentation:
                                dictattrs_without_documentation[key] = []
                            dictattrs_without_documentation[key].append(attr_info)

    # Raise descriptive error if any dict attributes are missing documentation
    if dictattrs_without_documentation:
        # Calculate stats
        total_classes = len(dictattrs_without_documentation)
        total_attributes = sum(len(attrs) for attrs in dictattrs_without_documentation.values())
        
        modules_set = set()
        for key in dictattrs_without_documentation:
            # key is like "owui_client.models.module_name.ClassName"
            module_name = key.rsplit(".", 1)[0]
            modules_set.add(module_name)
        total_modules = len(modules_set)

        issue_description = f"\nMissing 'Dict Fields:' documentation stats:\n"
        issue_description += f"- Modules: {total_modules}\n"
        issue_description += f"- Classes: {total_classes}\n"
        issue_description += f"- Attributes: {total_attributes}\n"

        for modclass, dictattrs in dictattrs_without_documentation.items():
            issue_description += f"\n- Module {modclass}\n"
            for dictattr in dictattrs:
                issue_description += f"  - Attribute {dictattr['name']}: {str(dictattr['annotation'])} missing 'Dict Fields:' section to describe valid key/value pairs\n"
        
        pytest.fail(issue_description, pytrace=False)


def test_doc_inheritance_resolution():
    """Verify that extract_attributes correctly resolves the defining class for documentation."""
    class Parent(BaseModel):
        parent_only: dict
        """Parent doc."""
        
        overridden: dict
        """Parent overridden doc."""

    class Child(Parent):
        overridden: dict
        """Child doc."""
        
        child_only: dict
        """Child only doc."""

    class GrandChild(Child):
        pass

    # Test Parent
    parent_attrs = extract_attributes(Parent)
    assert "Parent doc" in parent_attrs["parent_only"]["docstr"]
    assert "Parent overridden doc" in parent_attrs["overridden"]["docstr"]

    # Test Child
    child_attrs = extract_attributes(Child)
    # parent_only should come from Parent
    assert "Parent doc" in child_attrs["parent_only"]["docstr"]
    # overridden should come from Child
    assert "Child doc" in child_attrs["overridden"]["docstr"]
    # child_only from Child
    assert "Child only doc" in child_attrs["child_only"]["docstr"]

    # Test GrandChild
    gc_attrs = extract_attributes(GrandChild)
    # parent_only from Parent
    assert "Parent doc" in gc_attrs["parent_only"]["docstr"]
    # overridden from Child (closest definition)
    assert "Child doc" in gc_attrs["overridden"]["docstr"]
    # child_only from Child
    assert "Child only doc" in gc_attrs["child_only"]["docstr"]


def extract_attributes(from_class: type[BaseModel]) -> dict[str, dict[str, Any]]:
    """Extract detailed attribute information from a Pydantic model.

    Args:
        from_class: The Pydantic BaseModel class to extract attributes from.

    Returns:
        Dictionary mapping attribute names to their metadata dictionaries.
    """
    result = {}

    # Iterate through Pydantic model fields
    for field_name, field_info in from_class.model_fields.items():
        annotation = field_info.annotation

        # Find which class in the MRO actually defines this field
        defining_class = from_class
        for base_class in inspect.getmro(from_class):
            if (
                issubclass(base_class, BaseModel)
                and base_class is not BaseModel
                and field_name in base_class.__annotations__
            ):
                defining_class = base_class
                break

        # Get the source code from the DEFINING class, not the current class
        try:
            source_lines = inspect.getsourcelines(defining_class)[0]
            source_text = "".join(source_lines)
        except (OSError, TypeError):
            source_lines = []
            source_text = ""

        # Determine if optional
        origin = get_origin(annotation)
        args = get_args(annotation)

        # Check for Optional (Union with None)
        is_optional = False
        unwrapped_annotation = annotation
        if origin is type(None) or (
            hasattr(origin, "__name__") and origin.__name__ == "UnionType"
        ):
            # Handle Optional[X] which is Union[X, None]
            if type(None) in args:
                is_optional = True
                # Get the non-None type
                unwrapped_annotation = next(
                    (arg for arg in args if arg is not type(None)), annotation
                )

        # Handle typing.Union explicitly
        from typing import Union

        if origin is Union:
            if type(None) in args:
                is_optional = True
                unwrapped_annotation = next(
                    (arg for arg in args if arg is not type(None)), annotation
                )

        # Get base_type and sub_type
        unwrapped_origin = get_origin(unwrapped_annotation)
        unwrapped_args = get_args(unwrapped_annotation)

        if unwrapped_origin is not None:
            # Has a generic origin like List, Dict, etc.
            base_type = getattr(unwrapped_origin, "__name__", str(unwrapped_origin))

            # Get sub_type (first generic argument)
            if unwrapped_args:
                first_arg = unwrapped_args[0]
                sub_origin = get_origin(first_arg)
                if sub_origin is not None:
                    sub_type = getattr(sub_origin, "__name__", str(sub_origin))
                else:
                    sub_type = getattr(first_arg, "__name__", str(first_arg))
            else:
                sub_type = None
        else:
            # Simple type like str, int, etc.
            base_type = getattr(
                unwrapped_annotation, "__name__", str(unwrapped_annotation)
            )
            sub_type = None

        # Extract docstring from Field description
        field_description = field_info.description or ""

        # Extract documentation comment following the attribute
        attribute_docstring = ""
        if source_lines:
            # Look for the attribute definition and check next line for docstring
            for i, line in enumerate(source_lines):
                stripped_line = line.strip()
                if stripped_line.startswith(f"{field_name}:") or stripped_line.startswith(f"{field_name} =") or stripped_line.startswith(f"{field_name}="):
                    # Check if next line contains a string literal (docstring)
                    if i + 1 < len(source_lines):
                        next_line = source_lines[i + 1].strip()
                        # Match triple-quoted or single-quoted strings
                        if (
                            next_line.startswith('"""')
                            or next_line.startswith("'''")
                            or next_line.startswith('"')
                            or next_line.startswith("'")
                        ):
                            # Extract the string content
                            # This is simplified - would need more robust parsing for multi-line
                            quote_char = (
                                '"""'
                                if next_line.startswith('"""')
                                else (
                                    "'''"
                                    if next_line.startswith("'''")
                                    else next_line[0]
                                )
                            )
                            if len(quote_char) == 3:
                                # Triple-quoted string
                                start_idx = i + 1
                                docstring_lines = []
                                for j in range(start_idx, len(source_lines)):
                                    line_content = source_lines[j]
                                    docstring_lines.append(line_content)
                                    if quote_char in line_content and j > start_idx:
                                        break
                                # Join and clean
                                full_docstring = "".join(docstring_lines)
                                # Remove quotes and strip
                                attribute_docstring = full_docstring.replace(
                                    quote_char, ""
                                ).strip()
                            else:
                                # Single line string
                                attribute_docstring = (
                                    next_line.strip('"').strip("'").strip()
                                )
                    break

        # Combine docstrings
        combined_docstring = ""
        if attribute_docstring and field_description:
            combined_docstring = f"{attribute_docstring}\n{field_description}"
        elif attribute_docstring:
            combined_docstring = attribute_docstring
        elif field_description:
            combined_docstring = field_description

        # Get default value
        default_value = field_info.default
        if default_value is None and is_optional:
            default_value = None
        elif (
            hasattr(field_info, "default_factory")
            and field_info.default_factory is not None
        ):
            # Has a default factory, don't evaluate it
            default_value = f"<factory: {field_info.default_factory}>"

        # Build result dictionary
        result[field_name] = {
            "name": field_name,
            "annotation": annotation,
            "optional": is_optional or not field_info.is_required(),
            "base_type": base_type,
            "sub_type": sub_type,
            "docstr": combined_docstring,
            "default": default_value if field_info.is_required() is False else None,
        }

    return result


def has_dict_fields_documentation(docstr: str) -> bool:
    """Check if a docstring contains Dict Fields documentation.

    This function verifies that a dictionary attribute has been documented
    by checking for the presence of a "Dict Fields:" section header.
    The section can contain either:
    - A list of field definitions with types and descriptions
    - A reference/link to external documentation
    - An explanation of where the dict structure is defined

    Args:
        docstr: The docstring to check.

    Returns:
        True if "Dict Fields:" section is present, False otherwise.
    """
    if not docstr:
        return False

    # Look for "Dict Fields:" section header (case-insensitive for flexibility)
    # Allow for variations in spacing
    import re

    # Match "Dict Fields:" at start of line (potentially with leading whitespace)
    # This follows Google-style convention where sections start at beginning of line
    pattern = r"^\s*Dict Fields:\s*$"

    # Search multiline
    return bool(re.search(pattern, docstr, re.MULTILINE | re.IGNORECASE))
