#!/usr/bin/env python
"""
Script to convert inline templates to template_file references.

Usage:
    python convert_inline_templates.py <test_file.py>

Example:
    python convert_inline_templates.py tests/test_component.py --dry-run
    python convert_inline_templates.py tests/test_component.py --limit 5
"""

import argparse
import ast
import hashlib
import re
from pathlib import Path
from typing import List, Tuple, Optional


class InlineTemplateExtractor(ast.NodeVisitor):
    """Extract inline templates from Python AST."""

    def __init__(self, source: str):
        self.source = source
        self.source_lines = source.splitlines()
        self.templates: List[Tuple[int, int, str, str, Optional[str]]] = []  # (start_line, end_line, class_name, template_content, test_name)
        self.current_test_name: Optional[str] = None
        self.current_class_name: Optional[str] = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Track which test function we're in."""
        old_test_name = self.current_test_name
        if node.name.startswith('test_'):
            self.current_test_name = node.name
        self.generic_visit(node)
        self.current_test_name = old_test_name

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definitions to find Component classes."""
        old_class_name = self.current_class_name
        self.current_class_name = node.name

        # Look for template attribute in class body
        for item in node.body:
            # Handle regular assignment: template = """..."""
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == 'template':
                        # Found a template assignment
                        if isinstance(item.value, ast.Constant) and isinstance(item.value.value, str):
                            template_content = item.value.value
                            start_line = item.lineno
                            end_line = item.end_lineno or start_line

                            self.templates.append((
                                start_line,
                                end_line,
                                node.name,
                                template_content,
                                self.current_test_name
                            ))

            # Handle annotated assignment: template: types.django_html = """..."""
            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name) and item.target.id == 'template':
                    if item.value and isinstance(item.value, ast.Constant) and isinstance(item.value.value, str):
                        template_content = item.value.value
                        start_line = item.lineno
                        end_line = item.end_lineno or start_line

                        self.templates.append((
                            start_line,
                            end_line,
                            node.name,
                            template_content,
                            self.current_test_name
                        ))

        self.generic_visit(node)
        self.current_class_name = old_class_name


def extract_templates(test_file: Path) -> List[Tuple[int, int, str, str, Optional[str]]]:
    """Extract all inline templates from a test file."""
    source = test_file.read_text()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Error parsing {test_file}: {e}")
        return []

    extractor = InlineTemplateExtractor(source)
    extractor.visit(tree)

    return extractor.templates


def sanitize_filename(name: str) -> str:
    """Convert test/class name to safe filename."""
    # Remove test_ prefix if present
    if name.startswith('test_'):
        name = name[5:]

    # Convert to lowercase, replace spaces/underscores with hyphens
    name = name.lower().replace('_', '-').replace(' ', '-')

    # Remove any non-alphanumeric characters except hyphens
    name = re.sub(r'[^a-z0-9-]', '', name)

    return name


def generate_template_filename(class_name: str, test_name: Optional[str], template_content: str) -> str:
    """Generate a descriptive filename for the template."""
    # Try to extract meaningful name from class name
    base_name = sanitize_filename(class_name)

    # If class name is too generic, try to use test name
    if base_name in ('component', 'simplecomponent', 'testcomponent') and test_name:
        base_name = sanitize_filename(test_name)

    # If still too generic or empty, use content hash
    if not base_name or len(base_name) < 3:
        content_hash = hashlib.md5(template_content.encode()).hexdigest()[:8]
        base_name = f"template-{content_hash}"

    return f"{base_name}.html"


def create_template_file(
    template_dir: Path,
    filename: str,
    content: str,
    dry_run: bool = False
) -> Path:
    """Create a template file with the given content."""
    template_path = template_dir / filename

    # Handle filename collisions
    counter = 1
    original_stem = template_path.stem
    while template_path.exists():
        # Check if content is the same
        if template_path.read_text().strip() == content.strip():
            print(f"  ℹ️  Template already exists with same content: {template_path.name}")
            return template_path

        # Different content, use numbered suffix
        template_path = template_dir / f"{original_stem}-{counter}.html"
        counter += 1

    if not dry_run:
        template_path.write_text(content)
        print(f"  ✅ Created: {template_path.relative_to(template_path.parent.parent)}")
    else:
        print(f"  [DRY RUN] Would create: {template_path.relative_to(template_path.parent.parent)}")

    return template_path


def update_test_file(
    test_file: Path,
    replacements: List[Tuple[int, int, str]],
    dry_run: bool = False
) -> None:
    """Update test file to use template_file instead of inline templates."""
    source_lines = test_file.read_text().splitlines(keepends=True)

    # Process replacements in reverse order to maintain line numbers
    for start_line, end_line, template_file_path in sorted(replacements, reverse=True):
        # Convert to 0-based indexing
        start_idx = start_line - 1
        end_idx = end_line

        # Get indentation from the template line
        template_line = source_lines[start_idx]
        indent = len(template_line) - len(template_line.lstrip())

        # Create replacement line
        replacement = ' ' * indent + f'template_file = "{template_file_path}"\n'

        # Replace the lines
        source_lines[start_idx:end_idx] = [replacement]

    if not dry_run:
        test_file.write_text(''.join(source_lines))
        print(f"  ✅ Updated: {test_file.name}")
    else:
        print(f"  [DRY RUN] Would update: {test_file.name}")


def convert_file(test_file: Path, dry_run: bool = False, limit: Optional[int] = None) -> int:
    """Convert inline templates in a test file to template_file references."""
    print(f"\n📄 Processing: {test_file}")

    # Extract templates
    templates = extract_templates(test_file)

    if not templates:
        print("  ℹ️  No inline templates found")
        return 0

    print(f"  Found {len(templates)} inline template(s)")

    # Apply limit if specified
    if limit:
        templates = templates[:limit]
        print(f"  Limiting to first {limit} template(s)")

    # Create template directory
    test_name = test_file.stem  # e.g., "test_component"
    template_dir = test_file.parent / "templates" / test_name

    if not dry_run:
        template_dir.mkdir(parents=True, exist_ok=True)

    # Process each template
    replacements = []
    for start_line, end_line, class_name, content, test_name in templates:
        print(f"\n  Template in {class_name} (lines {start_line}-{end_line}):")

        # Generate filename
        filename = generate_template_filename(class_name, test_name, content)

        # Create template file
        template_path = create_template_file(template_dir, filename, content, dry_run)

        # Record replacement (use path relative to tests/templates/)
        relative_path = f"{test_file.stem}/{template_path.name}"
        replacements.append((start_line, end_line, relative_path))

    # Update test file
    if replacements:
        print(f"\n  Updating {test_file.name}:")
        update_test_file(test_file, replacements, dry_run)

    return len(replacements)


def main():
    parser = argparse.ArgumentParser(
        description="Convert inline templates to template_file references"
    )
    parser.add_argument(
        "test_file",
        type=Path,
        help="Path to test file to convert"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of templates to convert (for testing)"
    )

    args = parser.parse_args()

    if not args.test_file.exists():
        print(f"❌ Error: File not found: {args.test_file}")
        return 1

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")

    count = convert_file(args.test_file, args.dry_run, args.limit)

    print(f"\n✨ Done! Converted {count} template(s)")

    if args.dry_run:
        print("\n💡 Run without --dry-run to apply changes")
    else:
        print("\n💡 Run tests to verify: pytest", args.test_file)

    return 0


if __name__ == "__main__":
    exit(main())
