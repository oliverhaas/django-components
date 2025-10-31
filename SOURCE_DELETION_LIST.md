# Source Files to Delete

Based on deleted test files, here are the source files to remove:

## Step 1: Delete Extension Files (5 files)
1. `src/django_components/extensions/cache.py` - Component caching extension
2. `src/django_components/extensions/defaults.py` - Component defaults extension
3. `src/django_components/extensions/debug_highlight.py` - Debug highlighting extension
4. `src/django_components/extensions/dependencies.py` - Dependency extension
5. `src/django_components/extensions/view.py` - View/URL extension

## Step 2: Delete Built-in Component Files (2 files)
1. `src/django_components/components/dynamic.py` - Dynamic component
2. `src/django_components/components/error_fallback.py` - Error fallback component

## Step 3: Delete Core Feature Files (6 files)
1. `src/django_components/cache.py` - Caching infrastructure
2. `src/django_components/component_media.py` - ALL JS/CSS media handling
3. `src/django_components/dependencies.py` - JS/CSS dependency management
4. `src/django_components/expression.py` - Template expression enhancements
5. `src/django_components/provide.py` - Provide/Inject system
6. `src/django_components/extension.py` - Extension system base

## Step 4: Review and Clean Up (will need partial edits)
These files likely have code we need to remove but keep the files:
1. `src/django_components/component.py` - HUGE file, needs cleaning:
   - Remove Component.View
   - Remove Component.Cache
   - Remove Component.Args/Kwargs/Slots type validation
   - Remove get_js_data/get_css_data methods
   - Remove js/css/Media properties
   - Remove request integration
   - Keep: Core component registration, template_file, get_template_data()

2. `src/django_components/node.py` - Template node handling:
   - Remove expression parsing
   - Remove spread operator
   - Remove self-closing tags
   - Keep: Basic node rendering

3. `src/django_components/tag_formatter.py` - May need to keep basic functionality

4. `src/django_components/util/tag_parser.py` - Remove expression parsing

5. `src/django_components/__init__.py` - Remove exports for deleted features

## Strategy
Start with Steps 1-3 (complete file deletions), commit each step, run tests after each.
Then tackle Step 4 (partial cleanups) more carefully.
