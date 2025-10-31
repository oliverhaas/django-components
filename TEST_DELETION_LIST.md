# Test Files to Delete

Based on the streamlining plan, here are the test files to DELETE entirely:

## Complete Deletion (Features we're removing entirely)

1. **test_component_view.py** - Component Views/URLs feature
2. **test_component_cache.py** - Component caching feature
3. **test_cache.py** - General caching
4. **test_extension.py** - Extensions system
5. **test_command_ext.py** - Extension commands
6. **test_templatetags_provide.py** - Provide/Inject system
7. **test_component_typing.py** - Type validation system
8. **test_component_defaults.py** - Component defaults system
9. **test_component_dynamic.py** - Dynamic components
10. **test_component_error_fallback.py** - Error fallback components
11. **test_tag_formatter.py** - Tag formatters
12. **test_component_highlight.py** - Debug highlighting
13. **test_component_media.py** - ALL JS/CSS functionality (deferred)
14. **test_dependencies.py** - JS/CSS dependency management
15. **test_dependency_manager.py** - JS/CSS dependency management
16. **test_dependency_rendering.py** - JS/CSS dependency rendering
17. **test_dependency_rendering_e2e.py** - JS/CSS E2E tests
18. **test_expression.py** - Template expression enhancements
19. **test_templatetags_templating.py** - Custom templating features

## Partial Deletion (Need to review and simplify)

These files need manual review to keep only core tests:

1. **test_component.py** - KEEP but remove:
   - Inline template/js/css string tests
   - get_js_data/get_css_data tests
   - Component.View tests
   - Type validation tests
   - Request integration tests
   - Keep: Basic component registration, template_file loading, get_template_data()

2. **test_slots.py** - KEEP but remove:
   - Scoped slots with data passing tests
   - Keep: Basic named slots, fill, default content

3. **test_templatetags_slot_fill.py** - KEEP but remove:
   - Advanced slot features
   - Keep: Basic slot/fill functionality

4. **test_tag_parser.py** - KEEP but remove:
   - Spread operator tests
   - Literal lists/dicts tests
   - Self-closing tag tests
   - Multiline tag tests
   - Template tags in strings tests
   - attr:key=value tests
   - Keep: Basic arg/kwarg parsing

5. **test_context.py** - KEEP but remove:
   - Context isolation tests
   - Keep: Parent context access tests

6. **test_node.py** - KEEP but simplify
   - Remove advanced node features
   - Keep: Basic node rendering

## Files to KEEP as-is

These files test core functionality we're keeping:

1. **test_registry.py** - Component registration
2. **test_autodiscover.py** - Autodiscovery
3. **test_loader.py** - Template loading
4. **test_finders.py** - Component file finding
5. **test_attributes.py** - HTML attributes helper
6. **test_template.py** - Template handling
7. **test_templatetags_component.py** - Component template tag (may need minor cleanup)
8. **test_signals.py** - Basic signals (if we keep them)
9. **test_settings.py** - Settings
10. **test_utils.py** - Utility functions

## Command Test Files

Review these for removal:
1. **test_command_components.py** - Keep if it tests basic component commands
2. **test_command_create.py** - Keep if useful for component creation
3. **test_command_list.py** - Keep if useful for listing components

## Benchmark Files

Can be removed or updated later:
1. **test_benchmark_django.py**
2. **test_benchmark_django_small.py**
3. **test_benchmark_djc.py**
4. **test_benchmark_djc_small.py**

## Other Test Files

Review:
1. **test_html_parser.py** - Keep if used for template parsing
2. **test_template_parser.py** - Keep if used for template parsing
3. **test_templatetags.py** - Review for core functionality
4. **test_templatetags_extends.py** - Review template inheritance
5. **test_integration_template_partials.py** - Review
