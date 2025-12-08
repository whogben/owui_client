"""Generate the code reference pages and navigation."""

from pathlib import Path
import sys
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

root = Path(__file__).parent.parent
src = root / "src"

# Add src to sys.path to allow importing modules (if needed by mkdocs later,
# though this script just generates MD files)
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

    # Generate standard page for the module
    nav[nav_parts] = rel_doc_path.as_posix()
    final_doc_path = Path("reference", rel_doc_path)

    with mkdocs_gen_files.open(final_doc_path, "w") as fd:
        fd.write(f"::: {module_name}")

    mkdocs_gen_files.set_edit_path(final_doc_path, path.relative_to(root))

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
