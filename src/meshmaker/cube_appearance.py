"""
CubeAppearance - Defines the visual properties of a cube.
"""
from typing import Tuple, Optional


class CubeAppearance:
    """
    Defines the visual appearance properties of a cube in the mesh.
    
    Attributes:
        color: RGB color tuple (values between 0 and 1)
        alpha: Transparency value (0=transparent, 1=opaque)
        material: Material name/type (for future extensions)
    """
    
    def __init__(
        self, 
        color: Tuple[float, float, float] = (0.5, 0.5, 0.5),
        alpha: float = 1.0,
        material: Optional[str] = None
    ):
        """
        Initialize cube appearance.
        
        Args:
            color: RGB color tuple with values between 0 and 1
            alpha: Transparency value between 0 and 1
            material: Optional material type identifier
        """
        if not all(0 <= c <= 1 for c in color):
            raise ValueError("Color values must be between 0 and 1")
        if not 0 <= alpha <= 1:
            raise ValueError("Alpha must be between 0 and 1")
            
        self.color = color
        self.alpha = alpha
        self.material = material or "default"
    
    def __repr__(self):
        return f"CubeAppearance(color={self.color}, alpha={self.alpha}, material='{self.material}')"
    
    def __eq__(self, other):
        if not isinstance(other, CubeAppearance):
            return False
        return (self.color == other.color and 
                self.alpha == other.alpha and 
                self.material == other.material)
