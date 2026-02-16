"""
Unit tests for CubeAppearance class.
"""
import pytest
from meshmaker.cube_appearance import CubeAppearance


class TestCubeAppearance:
    """Test suite for CubeAppearance."""
    
    def test_default_appearance(self):
        """Test default appearance creation."""
        appearance = CubeAppearance()
        assert appearance.color == (0.5, 0.5, 0.5)
        assert appearance.alpha == 1.0
        assert appearance.material == "default"
    
    def test_custom_color(self):
        """Test custom color."""
        appearance = CubeAppearance(color=(1.0, 0.0, 0.0))
        assert appearance.color == (1.0, 0.0, 0.0)
        assert appearance.alpha == 1.0
    
    def test_custom_alpha(self):
        """Test custom alpha."""
        appearance = CubeAppearance(alpha=0.5)
        assert appearance.alpha == 0.5
    
    def test_custom_material(self):
        """Test custom material."""
        appearance = CubeAppearance(material="metal")
        assert appearance.material == "metal"
    
    def test_invalid_color_range(self):
        """Test that invalid color values raise error."""
        with pytest.raises(ValueError, match="Color values must be between 0 and 1"):
            CubeAppearance(color=(1.5, 0.0, 0.0))
        
        with pytest.raises(ValueError, match="Color values must be between 0 and 1"):
            CubeAppearance(color=(-0.1, 0.5, 0.5))
    
    def test_invalid_alpha_range(self):
        """Test that invalid alpha values raise error."""
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            CubeAppearance(alpha=1.5)
        
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            CubeAppearance(alpha=-0.1)
    
    def test_equality(self):
        """Test equality comparison."""
        app1 = CubeAppearance(color=(1.0, 0.0, 0.0), alpha=0.8)
        app2 = CubeAppearance(color=(1.0, 0.0, 0.0), alpha=0.8)
        app3 = CubeAppearance(color=(0.0, 1.0, 0.0), alpha=0.8)
        
        assert app1 == app2
        assert app1 != app3
        assert app1 != "not an appearance"
    
    def test_repr(self):
        """Test string representation."""
        appearance = CubeAppearance(color=(1.0, 0.0, 0.0), alpha=0.5, material="glass")
        repr_str = repr(appearance)
        assert "CubeAppearance" in repr_str
        assert "(1.0, 0.0, 0.0)" in repr_str
        assert "0.5" in repr_str
        assert "glass" in repr_str
