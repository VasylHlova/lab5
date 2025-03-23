from typing import Any
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for all geometric shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """
        Calculate the area of the shape.
        
        Returns:
            The area as a float value
        """
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """
        Calculate the perimeter of the shape.
        
        Returns:
            The perimeter as a float value
        """
        pass

class Movable(ABC):
    """Abstract base class for objects that can be moved in 2D space."""
    
    @abstractmethod
    def move(self, dx: float, dy: float) -> Any:
        """
        Move the object by the specified offsets.
        
        Args:
            dx: Offset in x direction
            dy: Offset in y direction
            
        Returns:
            Self reference for method chaining
        """
        pass

class Rotatable(ABC):
    """Abstract base class for objects that can be rotated."""
    
    @abstractmethod
    def rotate(self, angle_degrees: float) -> Any:
        """
        Rotate the object by the specified angle.
        
        Args:
            angle_degrees: Angle to rotate in degrees
            
        Returns:
            Self reference for method chaining
        """
        pass        

class ColorMixin:
    """Mixin class that adds color property to objects."""
    
    def __init__(self, color: str = 'black', **kwargs):
        """
        Initialize with color.
        
        Args:
            color: Color name or hex code (default: 'black')
            **kwargs: Additional keyword arguments to pass to parent class
        """
        self.color = color
        super().__init__(**kwargs)
        
    def set_color(self, color: str) -> Any:
        """
        Set the color of the object.
        
        Args:
            color: Color name or hex code
            
        Returns:
            Self reference for method chaining
        """
        self.color = color
        return self


class LabelMixin:
    """Mixin class that adds label property to objects."""
    
    def __init__(self, label: str = '', **kwargs):
        """
        Initialize with label.
        
        Args:
            label: Text label (default: empty string)
            **kwargs: Additional keyword arguments to pass to parent class
        """
        self.label = label
        super().__init__(**kwargs)
        
    def set_label(self, label: str) -> Any:
        """
        Set the label of the object.
        
        Args:
            label: Text label
            
        Returns:
            Self reference for method chaining
        """
        self.label = label
        return self        