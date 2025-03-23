from typing import Tuple
from .base import Shape, ColorMixin, LabelMixin, Movable, Rotatable


class Triangle(Shape, Movable, Rotatable):
    """Triangle shape with position, angle and dimensions."""
    
    def __init__(self, a: float, b: float, c: float, x: float, y: float, angle: float):
        """
        Initialize a triangle.
        
        Args:
            a: Length of first side
            b: Length of second side
            c: Length of third side
            x: X-coordinate of position
            y: Y-coordinate of position
            angle: Rotation angle in degrees
        """
        self.a = a
        self.b = b
        self.c = c
        self.x = x
        self.y = y
        self.angle = angle
        
    def area(self) -> float:
        """Calculate the area of the triangle using Heron's formula.
        
        Returns:
            Area of the triangle
        """
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5
    
    def perimeter(self) -> float:
        """Calculate the perimeter of the triangle.
        
        Returns:
            Perimeter of the triangle
        """
        return self.a + self.b + self.c
    
    def move(self, dx: float, dy: float) -> 'Triangle':
        """Move the triangle by the specified offsets.
        
        Args:
            dx: Offset in x direction
            dy: Offset in y direction
            
        Returns:
            Self reference for method chaining
        """
        self.x += dx
        self.y += dy
        
        return self
    
    def rotate(self, angle_degrees: float) -> 'Triangle':
        """Rotate the triangle by the specified angle.
        
        Args:
            angle_degrees: Angle to rotate in degrees
            
        Returns:
            Self reference for method chaining
        """
        self.angle = (self.angle + angle_degrees) % 360

        return self
    
class Rectangle(Shape, Movable, Rotatable):
    """Rectangle shape with position, angle and dimensions."""
    
    def __init__(self, a: float, b: float, x: float, y: float, angle: float):
        """
        Initialize a rectangle.
        
        Args:
            a: Width of rectangle
            b: Height of rectangle
            x: X-coordinate of position
            y: Y-coordinate of position
            angle: Rotation angle in degrees
        """
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.angle = angle
        
    def area(self) -> float:
        """Calculate the area of the rectangle.
        
        Returns:
            Area of the rectangle
        """
        return self.a * self.b
    
    def perimeter(self) -> float:
        """Calculate the perimeter of the rectangle.
        
        Returns:
            Perimeter of the rectangle
        """
        return 2 * (self.a + self.b)
    
    def move(self, dx: float, dy: float) -> 'Rectangle':
        """Move the rectangle by the specified offsets.
        
        Args:
            dx: Offset in x direction
            dy: Offset in y direction
            
        Returns:
            Self reference for method chaining
        """
        self.x += dx
        self.y += dy
        
        return self
    
    def rotate(self, angle_degrees: float) -> 'Rectangle':
        """Rotate the rectangle by the specified angle.
        
        Args:
            angle_degrees: Angle to rotate in degrees
            
        Returns:
            Self reference for method chaining
        """
        self.angle = (self.angle + angle_degrees) % 360
        
        return self
    
class Circle(Shape, Movable, Rotatable):
    """Circle shape with position, angle and radius."""
    
    def __init__(self, r: float, x: float, y: float, angle: float):
        """
        Initialize a circle.
        
        Args:
            r: Radius of the circle
            x: X-coordinate of center
            y: Y-coordinate of center
            angle: Rotation angle in degrees
        """
        self.r = r
        self.x = x
        self.y = y  
        self.angle = angle
        
    @property
    def center(self) -> Tuple[float, float]:
        """Get the center coordinates of the circle.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return (self.x, self.y)
        
    @property
    def radius(self) -> float:
        """Get the radius of the circle.
        
        Returns:
            Radius value
        """
        return self.r
        
    def area(self) -> float:
        """Calculate the area of the circle.
        
        Returns:
            Area of the circle
        """
        return 3.14 * self.r ** 2
    
    def perimeter(self) -> float:
        """Calculate the perimeter (circumference) of the circle.
        
        Returns:
            Circumference of the circle
        """
        return 2 * 3.14 * self.r
    
    def move(self, dx: float, dy: float) -> 'Circle':
        """Move the circle by the specified offsets.
        
        Args:
            dx: Offset in x direction
            dy: Offset in y direction
            
        Returns:
            Self reference for method chaining
        """
        self.x += dx
        self.y += dy
        
        return self
    
    def rotate(self, angle_degrees: float) -> 'Circle':
        """Rotate the circle by the specified angle.
        
        Args:
            angle_degrees: Angle to rotate in degrees
            
        Returns:
            Self reference for method chaining
        """
        self.angle = (self.angle + angle_degrees) % 360
        
        return self

class LabelledColoredRectangle(Rectangle, ColorMixin, LabelMixin):
    """Rectangle with additional color and label attributes."""
    
    def __init__(self, a: float, b: float, x: float = 0, y: float = 0, angle: float = 0, 
                 color: str = 'black', label: str = ''):
        """
        Initialize a labeled and colored rectangle.
        
        Args:
            a: Width of rectangle
            b: Height of rectangle
            x: X-coordinate of position
            y: Y-coordinate of position
            angle: Rotation angle in degrees
            color: Color name or hex code
            label: Text label for the rectangle
        """
        Rectangle.__init__(self, a=a, b=b, x=x, y=y, angle=angle)
        ColorMixin.__init__(self, color=color)
        LabelMixin.__init__(self, label=label)

class LabelledColoredCircle(Circle, ColorMixin, LabelMixin):
    """Circle with additional color and label attributes."""
    
    def __init__(self, r: float, x: float = 0, y: float = 0, angle: float = 0, 
                 color: str = 'black', label: str = ''):
        """
        Initialize a labeled and colored circle.
        
        Args:
            r: Radius of the circle
            x: X-coordinate of center
            y: Y-coordinate of center
            angle: Rotation angle in degrees
            color: Color name or hex code
            label: Text label for the circle
        """
        Circle.__init__(self, r=r, x=x, y=y, angle=angle)
        ColorMixin.__init__(self, color=color)
        LabelMixin.__init__(self, label=label)

class LabelledColoredTriangle(Triangle, ColorMixin, LabelMixin):
    """Triangle with additional color and label attributes."""
    
    def __init__(self, a: float, b: float, c: float, x: float = 0, y: float = 0, angle: float = 0, 
                 color: str = 'black', label: str = ''):
        """
        Initialize a labeled and colored triangle.
        
        Args:
            a: Length of first side
            b: Length of second side
            c: Length of third side
            x: X-coordinate of position
            y: Y-coordinate of position
            angle: Rotation angle in degrees
            color: Color name or hex code
            label: Text label for the triangle
        """
        Triangle.__init__(self, a=a, b=b, c=c, x=x, y=y, angle=angle)
        ColorMixin.__init__(self, color=color)
        LabelMixin.__init__(self, label=label)                          