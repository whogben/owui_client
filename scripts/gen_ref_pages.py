"""Generate the code reference pages and navigation."""

from pathlib import Path
import sys
import importlib
import inspect
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

root = Path(__file__).parent.parent
src = root / "src"

# Add src to sys.path to allow importing modules
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

# Copy README.md to index.md
with mkdocs_gen_files.open("index.md", "w") as fd:
    fd.write(Path(root, "README.md").read_text())

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    # Strip 'owui_client' from navigation and file structure if present
    if parts and parts[0] == "owui_client":
        nav_parts = parts[1:]
    else:
        nav_parts = parts

    # Strip 'owui_client' from doc path
    doc_parts = doc_path.parts
    if doc_parts and doc_parts[0] == "owui_client":
        rel_doc_path = Path(*doc_parts[1:])
    else:
        rel_doc_path = doc_path

    # Skip if it was the top level init (which becomes empty nav_parts)
    if not nav_parts:
        continue

    module_name = ".".join(parts)

    try:
        # Import the module to inspect it
        mod = importlib.import_module(module_name)

        # Find classes defined in this module
        classes = []
        for name, obj in inspect.getmembers(mod):
            if inspect.isclass(obj) and obj.__module__ == module_name:
                classes.append(name)

        if classes:
            # If there are classes, create a folder for the module
            # The module index page will list the classes

            # 1. Create the module index page
            # We use the original path logic but make it an index.md in a folder
            # e.g. reference/models/ollama/index.md

            # Adjust paths for folder structure
            if rel_doc_path.name == "index.md":
                # It's already an index (from __init__.py), so we use it as is
                mod_index_path = rel_doc_path
                mod_folder = rel_doc_path.parent
            else:
                # It's a file like ollama.md. Turn it into ollama/index.md
                mod_folder = rel_doc_path.with_suffix("")
                mod_index_path = mod_folder / "index.md"

            full_mod_index_path = Path("reference", mod_index_path)

            # Write the module index
            nav[nav_parts] = mod_index_path.as_posix()

            with mkdocs_gen_files.open(full_mod_index_path, "w") as fd:
                fd.write(f"# {parts[-1]}\n\n")
                fd.write(f"::: {module_name}\n")
                fd.write("    options:\n")
                fd.write(
                    "      members: []\n\n"
                )  # Don't show members on index, just docstring?
                # Actually, maybe show functions here?
                # For now let's just show docstring and list classes

                fd.write("## Classes\n\n")
                for cls_name in sorted(classes):
                    fd.write(f"- [{cls_name}]({cls_name}.md)\n")

            mkdocs_gen_files.set_edit_path(full_mod_index_path, path.relative_to(root))

            # 2. Create pages for each class
            for cls_name in sorted(classes):
                cls_doc_path = mod_folder / f"{cls_name}.md"
                full_cls_doc_path = Path("reference", cls_doc_path)

                # Add to nav: Module -> Class
                nav[nav_parts + (cls_name,)] = cls_doc_path.as_posix()

                with mkdocs_gen_files.open(full_cls_doc_path, "w") as fd:
                    fd.write(f"::: {module_name}.{cls_name}\n")

                mkdocs_gen_files.set_edit_path(
                    full_cls_doc_path, path.relative_to(root)
                )

        else:
            # No classes, just generate standard page
            nav[nav_parts] = rel_doc_path.as_posix()
            final_doc_path = Path("reference", rel_doc_path)
            with mkdocs_gen_files.open(final_doc_path, "w") as fd:
                fd.write(f"::: {module_name}")
            mkdocs_gen_files.set_edit_path(final_doc_path, path.relative_to(root))

    except Exception as e:
        print(f"Failed to inspect {module_name}: {e}")
        # Fallback to standard page
        nav[nav_parts] = rel_doc_path.as_posix()
        final_doc_path = Path("reference", rel_doc_path)
        with mkdocs_gen_files.open(final_doc_path, "w") as fd:
            fd.write(f"::: {module_name}")
        mkdocs_gen_files.set_edit_path(final_doc_path, path.relative_to(root))

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
