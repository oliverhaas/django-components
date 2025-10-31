# Django Components - Streamlining Plan

## Goal
Streamline django-components to its core essentials: providing a simple way to define template tags as UI components, staying VERY close to Django's template tag and node render syntax.

## Repository Status
- Fork: `oliverhaas/django-components`
- Upstream: `django-components/django-components`
- Branch: `feat/streamline`
- Status: Up-to-date with upstream/master

## Core Features to KEEP

### 1. Basic Component System
**Why**: This is the foundation - registering components as template tags
- `@register("component_name")` decorator
- `Component` base class
- Component registry
- Autodiscovery of components
- Template file loading
- **Tests to keep**: `test_component.py`, `test_registry.py`, `test_autodiscover.py`, `test_loader.py`

### 2. Template Rendering
**Why**: Core component functionality
- `{% component "name" %}{% endcomponent %}` template tag
- Basic template rendering with `template_file` or `template` attribute
- `get_template_data()` method for passing data to templates
- **Tests to keep**: `test_templatetags_component.py`, `test_template.py`

### 3. File Organization / Loaders
**Why**: Needed for neat component organization
- Component file loaders/finders
- Directory structure support (e.g., `components/calendar/calendar.py`)
- **Tests to keep**: `test_finders.py`, `test_loader.py`

### 4. Basic Slots
**Why**: Essential for component composition
- `{% slot %}` and `{% fill %}` tags for basic composition
- Named slots
- **Tests to keep**: Parts of `test_slots.py`, `test_templatetags_slot_fill.py` (simplified)

### 5. JS/CSS File Loading (ESSENTIAL)
**Why**: Components need their associated assets
- `js_file` and `css_file` attributes
- Loading JS/CSS from separate files alongside templates
- Basic Media class integration
- **Tests to keep**: Parts of `test_component_media.py` (file loading only)

### 6. HTML Attributes Helper
**Why**: Useful for HTML generation in templates
- `{% html_attrs %}` template tag
- Basic attribute merging
- **Tests to keep**: `test_attributes.py`

## Features to REMOVE

### 1. Template Tag Expression Enhancements
**Why**: Adds complexity, moves away from Django's template syntax
- ❌ Spread operator `...dict`
- ❌ Template tags inside literal strings `"{{ first_name }} {{ last_name }}"`
- ❌ Literal lists and dictionaries in templates `[1, 2, 3]`, `{"key": "value"}`
- ❌ Pass dictionaries by key-value pairs `attr:key=val`
- ❌ Self-closing tags `{% component / %}`
- ❌ Multi-line template tags
- **Tests to remove**: Parts of `test_tag_parser.py`, `test_expression.py`, `test_templatetags_templating.py`

### 2. Inline Template/JS/CSS Strings
**Why**: We want file-based components only
- ❌ `template = "..."` as string
- ❌ `js = "..."` as string
- ❌ `css = "..."` as string
- ❌ `get_js_data()` and `get_css_data()` methods (template variables in JS/CSS)
- **Tests to remove**: Tests for inline template/js/css strings in `test_component.py`, `test_component_media.py`

### 3. Component Views/URLs
**Why**: Too opinionated, not core functionality
- ❌ `Component.View` class with HTTP methods
- ❌ `Component.as_view()`
- ❌ Auto-generated component URLs
- ❌ `get_component_url()`
- **Tests to remove**: `test_component_view.py`, `test_extension_view.py`

### 4. HTML Fragments / HTMX Integration
**Why**: Can be handled by users without framework support
- ❌ Fragment-specific rendering
- ❌ Automatic JS/CSS injection on fragment updates
- ❌ Special fragment handling
- **Tests to remove**: `test_component_highlight.py`, parts of `test_dependencies.py`

### 5. Provide/Inject System
**Why**: Too complex, not core to template tags
- ❌ `{% provide %}` template tag
- ❌ `Component.inject()` method
- ❌ Context provider system
- **Tests to remove**: `test_templatetags_provide.py`

### 6. Component Caching
**Why**: Can use Django's caching directly
- ❌ `Component.Cache` class
- ❌ Component-specific caching logic
- **Tests to remove**: `test_component_cache.py`, `test_cache.py`

### 7. Extensions System
**Why**: Over-engineered for simple needs
- ❌ Extension base classes
- ❌ Lifecycle hooks system
- ❌ Extension commands and URLs
- **Tests to remove**: `test_extension.py`, `test_command_ext.py`

### 8. Type Validation System
**Why**: Too opinionated, Python has typing already
- ❌ `Component.Args` class
- ❌ `Component.Kwargs` class
- ❌ `Component.Slots` class with types
- ❌ Runtime validation of inputs
- **Tests to remove**: `test_component_typing.py`

### 9. Component Defaults System
**Why**: Adds complexity
- ❌ Default value system for components
- **Tests to remove**: `test_component_defaults.py`

### 10. Dynamic Components
**Why**: Niche feature
- ❌ Dynamic component loading/creation
- **Tests to remove**: `test_component_dynamic.py`

### 11. Error Fallback Components
**Why**: Niche feature
- ❌ Error boundary components
- **Tests to remove**: `test_component_error_fallback.py`

### 12. Tag Formatters
**Why**: Unnecessary customization
- ❌ Custom tag formatter system
- **Tests to remove**: `test_tag_formatter.py`

### 13. Advanced Slot Features
**Why**: Keep slots simple
- ❌ Scoped slots with data passing
- ❌ Default slot content
- ❌ Slot data transformation
- Keep only: Basic named slots with fill

### 14. Component Highlighting/Debug Tools
**Why**: Development tools, not core
- ❌ Visual component highlighting
- ❌ Debug highlighting system

### 15. Dependency Management for JS/CSS
**Why**: Over-engineered, keep it simple
- ❌ Complex dependency tracking
- ❌ Deduplication logic
- ❌ `render_dependencies()` complexity
- Keep only: Simple JS/CSS file collection and output

### 16. Secondary/Third-party JS/CSS
**Why**: Users can add `<script>` and `<link>` tags manually
- ❌ `Media` class for third-party assets
- ❌ Multiple JS/CSS file support beyond component's own files
- Keep only: Single `js_file` and `css_file` per component

### 17. Template Tags Beyond Component
**Why**: Focus on components only
- ❌ Custom template tag creation helpers (`@template_tag`)
- ❌ `BaseNode` for custom tags
- Keep only: Component-related tags

### 18. Context Scope Management
**Why**: Too complex
- ❌ Special context isolation
- ❌ Context scope features

### 19. HTTP Request Integration
**Why**: Too opinionated
- ❌ `self.request` in components
- ❌ Request context processor integration
- Components should receive data via kwargs

## Implementation Strategy

### Phase 1: Analysis (Current)
1. ✅ Map all features
2. ✅ Identify tests for features to keep
3. Create list of files/modules to remove

### Phase 2: Test Cleanup
1. Delete tests for features we don't want
2. Keep only tests that validate core functionality
3. Run remaining tests to establish baseline

### Phase 3: Code Removal
1. Remove unused modules/files
2. Remove unused code from kept modules
3. Update remaining code to remove dependencies on removed features
4. Iterate until all tests pass

### Phase 4: Documentation
1. Update README
2. Simplify documentation
3. Update examples

## Design Decisions (CONFIRMED)

1. **Slots**: ✅ Support named slots AND default slot content
2. **JS/CSS**: ✅ SKIP for now - will implement later with proper collectstatic integration
3. **Context**: ✅ Components access parent template context (add "only" keyword later)
4. **Args**: ✅ Keep args support (needed for component name: `{% component "name" %}`)

## Revised Features Summary

### KEEP:
1. Basic Component System (register, Component class, registry, autodiscovery)
2. Template Rendering (`{% component "name" %}`, `template_file` only, `get_template_data()`)
3. File Organization / Loaders
4. Slots with Default Content (`{% slot %}`, `{% fill %}`, default content)
5. HTML Attributes Helper (`{% html_attrs %}`)
6. Parent template context access (default behavior)
7. Args support (component name is an arg)

### REMOVE:
1. Template tag expression enhancements (spread, literals, self-closing, multiline, etc.)
2. Inline template/JS/CSS strings (`template = "..."`, `js = "..."`, `css = "..."`)
3. Component Views/URLs (Component.View, as_view(), etc.)
4. HTML Fragments / HTMX integration
5. Provide/Inject system
6. Component Caching
7. Extensions System
8. Type Validation System (Component.Args, Component.Kwargs, runtime validation)
9. Component Defaults System
10. Dynamic Components
11. Error Fallback Components
12. Tag Formatters
13. Advanced Slot Features (scoped slots with data passing - keep default content!)
14. Component Highlighting/Debug Tools
15. ALL JS/CSS functionality (DEFERRED - will add back with collectstatic later)
16. Custom template tag creation helpers (@template_tag, BaseNode)
17. Context isolation features (keep parent context access)
18. HTTP Request integration (self.request, context processors)

## Expected Outcome

A minimal django-components that:
- Provides `@register()` decorator for components
- Supports `{% component "name" kwarg=value %}` template tag with args and kwargs
- Loads templates from files only (`template_file` attribute)
- Supports named slots with `{% slot %}` and `{% fill %}` plus default content
- Has simple autodiscovery
- Uses standard Django template syntax (no custom extensions)
- Components access parent template context
- Has a small, maintainable codebase
- NO JS/CSS support initially (will be added later)

## Next Steps

1. ✅ Plan reviewed and confirmed
2. **START HERE**: Phase 2 - Delete tests we don't need
3. Use remaining test failures to guide code removal
