"""Tests for prompt management system."""

import pytest
from hypothesis import given, strategies as st

from src.ai_agent.prompts import PromptTemplate, PromptManager, PromptRenderer


class TestPromptTemplate:
    """Test PromptTemplate."""
    
    def test_template_creation(self):
        """Test creating a template."""
        template = PromptTemplate(
            name="test",
            template="Hello {name}!",
            variables=["name"],
        )
        
        assert template.name == "test"
        assert "name" in template.variables
    
    def test_template_render(self):
        """Test rendering a template."""
        template = PromptTemplate(
            name="test",
            template="Hello {name}, you are {age} years old.",
            variables=["name", "age"],
        )
        
        result = template.render(name="Alice", age=30)
        assert result == "Hello Alice, you are 30 years old."
    
    def test_template_missing_variable(self):
        """Test error on missing variable."""
        template = PromptTemplate(
            name="test",
            template="Hello {name}!",
            variables=["name"],
        )
        
        with pytest.raises(ValueError):
            template.render()
    
    def test_template_with_role(self):
        """Test template with role."""
        template = PromptTemplate(
            name="test",
            template="Task: {task}",
            variables=["task"],
            role="helpful assistant",
        )
        
        result = template.get_full_prompt(task="help me")
        assert "helpful assistant" in result
        assert "help me" in result


class TestPromptManager:
    """Test PromptManager."""
    
    def test_manager_initialization(self):
        """Test manager loads default templates."""
        manager = PromptManager()
        
        assert len(manager.templates) > 0
        assert "default_agent" in manager.list_templates()
    
    def test_register_template(self):
        """Test registering a template."""
        manager = PromptManager()
        
        template = PromptTemplate(
            name="custom",
            template="Custom {text}",
            variables=["text"],
        )
        
        manager.register_template(template)
        assert "custom" in manager.list_templates()
    
    def test_get_template(self):
        """Test getting a template."""
        manager = PromptManager()
        
        template = manager.get_template("default_agent")
        assert template is not None
        assert template.name == "default_agent"
    
    def test_delete_template(self):
        """Test deleting a template."""
        manager = PromptManager()
        
        template = PromptTemplate(
            name="temp",
            template="Temp {x}",
            variables=["x"],
        )
        
        manager.register_template(template)
        assert "temp" in manager.list_templates()
        
        manager.delete_template("temp")
        assert "temp" not in manager.list_templates()


class TestPromptRenderer:
    """Test PromptRenderer."""
    
    def test_render_simple(self):
        """Test simple rendering."""
        result = PromptRenderer.render(
            "Hello {name}!",
            {"name": "World"}
        )
        assert result == "Hello World!"
    
    def test_optimize_whitespace(self):
        """Test optimizing whitespace."""
        prompt = "Hello    world  \n\n\n  test"
        optimized = PromptRenderer.optimize(prompt)
        
        assert "    " not in optimized
        assert optimized.strip() == optimized
    
    def test_count_tokens(self):
        """Test token counting."""
        text = "Hello world, this is a test."
        count = PromptRenderer.count_approximate_tokens(text)
        
        assert count > 0
        assert isinstance(count, int)


# Property-based tests
class TestPromptTemplateProperties:
    """Property 20: Template variable substitution."""
    
    @given(
        var_name=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))),
        var_value=st.text(min_size=0, max_size=100),
    )
    def test_variable_substitution_property(self, var_name: str, var_value: str):
        """Test that variable substitution works for any variable name and value."""
        template = PromptTemplate(
            name="test",
            template=f"{{{var_name}}}",
            variables=[var_name],
        )
        
        result = template.render(**{var_name: var_value})
        assert result == var_value
    
    @given(
        text1=st.text(min_size=0, max_size=50),
        text2=st.text(min_size=0, max_size=50),
        text3=st.text(min_size=0, max_size=50),
    )
    def test_multiple_variable_substitution(self, text1: str, text2: str, text3: str):
        """Test substitution with multiple variables."""
        template = PromptTemplate(
            name="test",
            template="{a} {b} {c}",
            variables=["a", "b", "c"],
        )
        
        result = template.render(a=text1, b=text2, c=text3)
        assert text1 in result
        assert text2 in result
        assert text3 in result
