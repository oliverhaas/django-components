from time import perf_counter

from django.template import Context, Template

from django_components import Component, registry, types
from tests.django_test_setup import *  # NOQA
from tests.testutils import BaseTestCase

from pytest import mark


class BasicallyEmptyComponent(Component):
    template: types.django_html = """
        hello world
    """

    def get_context_data(self):
        return {}

class SlottedComponent(Component):
    template: types.django_html = """
        {% load component_tags %}
        <custom-template>
            <header>{% slot "header" %}Default header{% endslot %}</header>
            <main>{% slot "main" %}Default main{% endslot %}</main>
            <footer>{% slot "footer" %}Default footer{% endslot %}</footer>
        </custom-template>
    """

class SimpleComponent(Component):
    template: types.django_html = """
        Variable: <strong>{{ variable }}</strong>
    """

    def get_context_data(self, variable, variable2="default"):
        return {
            "variable": variable,
            "variable2": variable2,
        }

@mark.benchmark
class RenderBenchmarks(BaseTestCase):
    def setUp(self):
        super().setUp()
        registry.clear()
        registry.register("basically_empty_component", BasicallyEmptyComponent)
        registry.register("simple_component", SimpleComponent)
        registry.register("slotted_component", SlottedComponent)
    
    @staticmethod
    def timed_loop(func, iterations=1000):
        """Run func iterations times, and return the time in ms per iteration."""
        start_time = perf_counter()
        for _ in range(iterations):
            func()
        end_time = perf_counter()
        total_elapsed = end_time - start_time  # NOQA
        return total_elapsed * 1000 / iterations

    def test_render_time_for_basically_empty_component(self):
        template_str: types.django_html = "{% load component_tags %}{% component 'basically_empty_component' / %}"
        template = Template(template_str)

        print(f"Basically empty component: {self.timed_loop(lambda: template.render(Context({})))} ms per iteration")

    def test_render_time_for_small_component(self):
        template_str: types.django_html = """
            {% load component_tags %}
            {% component 'simple_component' variable='foo' / %}
        """
        template = Template(template_str)

        print(f"Small component: {self.timed_loop(lambda: template.render(Context({})))} ms per iteration")

    def test_render_time_for_slotted_component(self):
        template_str: types.django_html = """
            {% load component_tags %}
            {% component 'slotted_component' %}
                {% fill "header" %}Header{% endfill %}
                {% fill "main" %}Main{% endfill %}
                {% fill "footer" %}Footer{% endfill %}
            {% endcomponent %}
        """
        template = Template(template_str)

        print(f"Slotted component: {self.timed_loop(lambda: template.render(Context({})))} ms per iteration")