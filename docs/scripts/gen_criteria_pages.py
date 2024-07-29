"""Generate the code reference pages."""

from pathlib import Path

import mkdocs_gen_files

root = Path(__file__).parent.parent.parent
criteria_path = root.joinpath("assertive/criteria")
nav = mkdocs_gen_files.Nav()  # type: ignore

criteria_file_path = "criteria.md"


for path in sorted(criteria_path.glob("*.py")):
    module_path = path.relative_to(root).with_suffix("")
    doc_path = path.relative_to(criteria_path).with_suffix(".md")
    full_doc_path = Path("criteria", "in-built", doc_path)
    nav_path = Path("in-built", doc_path)

    module_parts = tuple(module_path.parts)

    module_name = module_parts[-1]

    if module_name in ("__init__", "__main__", "utils"):
        continue
    nav["in-built", module_name] = nav_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(module_parts)
        fd.write(f"::: {ident}")
        fd.write("""
    options:
        show_root_heading: true
        show_symbol_type_toc: true
        show_if_no_docstring: false
        members_order: source
    rendering:
        show_source: true
""")

    with mkdocs_gen_files.open(criteria_file_path, "a") as cd:
        cd.write(f"- [{module_name}]({module_name})")
        cd.write("\n")

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

with mkdocs_gen_files.open("criteria/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
