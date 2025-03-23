from typing import List, Tuple
from .base import Shape, Movable, Rotatable
import math

class Polygon(Shape, Movable, Rotatable):
    """A polygon defined by a list of vertices."""
    
    def __init__(self, vertices: List[Tuple[float, float]], angle: float = 0):
        """
        Initialize a polygon.
        
        Args:
            vertices: List of (x, y) vertex coordinates
            angle: Rotation angle in degrees
            
        Raises:
            ValueError: If polygon has fewer than 3 vertices
        """
        if len(vertices) < 3:
            raise ValueError('Polygon must have at least 3 vertices')
        self.vertices = vertices
        self.angle = angle
    
    def perimeter(self) -> float:
        """
        Calculate the perimeter of the polygon.
        
        Returns:
            The sum of all side lengths
            
        Raises:
            ValueError: If polygon has fewer than 3 vertices
        """
        if len(self.vertices) < 3:
            raise ValueError('Polygon must have at least 3 vertices')
        p = 0
        for i in range(len(self.vertices)):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % len(self.vertices)]  
            p += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) 
        return p
    
    def area(self) -> float:
        """
        Calculate the area of the polygon using the Shoelace formula.
        
        Returns:
            Area of the polygon
        """
        s = abs(sum([self.vertices[i][0] * self.vertices[(i+1) % len(self.vertices)][1] -  self.vertices[i][1] * self.vertices[(i+1) % len(self.vertices)][0] for i in range(len(self.vertices))])) / 2
        return s
    
    def _calculate_centroid(self) -> Tuple[float, float]:
        """
        Calculate the centroid (center of mass) of the polygon.
        
        Returns:
            Tuple of (x, y) coordinates of the centroid
        """
        n = len(self.vertices)
        area = self.area()
       
        if area == 0:
            x_sum = sum(v[0] for v in self.vertices)
            y_sum = sum(v[1] for v in self.vertices)
            return (x_sum / n, y_sum / n)
        
        cx = sum([(self.vertices[i][0] + self.vertices[(i+1)%n][0]) * (self.vertices[i][0] * self.vertices[(i+1)%n][1] - self.vertices[(i+1)%n][0] * self.vertices[i][1]) for i in range(n)])
        cy = sum([(self.vertices[i][1] + self.vertices[(i+1)%n][1]) * (self.vertices[i][0] * self.vertices[(i+1)%n][1] - self.vertices[(i+1)%n][0] * self.vertices[i][1]) for i in range(n)])
        cx /= (6 * area)
        cy /= (6 * area)
        
        return (cx, cy)
   
    def move(self, dx: float, dy: float) -> 'Polygon':
        """
        Move the polygon by shifting all vertices.
        
        Args:
            dx: Offset in x direction
            dy: Offset in y direction
            
        Returns:
            Self reference for method chaining
        """
        self.vertices = [(x + dx, y + dy) for x, y in self.vertices]
        return self
    
    def rotate(self, angle_degrees: float) -> 'Polygon':
        """
        Rotate the polygon around its centroid.
        
        Args:
            angle_degrees: Angle to rotate in degrees
            
        Returns:
            Self reference for method chaining
        """
        self.angle = (self.angle + angle_degrees) % 360
        
        angle_rad = math.radians(angle_degrees)
        
        centroid = self._calculate_centroid()
        cx, cy = centroid

        new_vertices = []
        for x, y in self.vertices:
            # Translate to origin
            x_translated = x - cx
            y_translated = y - cy
            
            # Rotate
            x_rotated = x_translated * math.cos(angle_rad) - y_translated * math.sin(angle_rad)
            y_rotated = x_translated * math.sin(angle_rad) + y_translated * math.cos(angle_rad)
            
            # Translate back
            new_x = x_rotated + cx
            new_y = y_rotated + cy
            
            new_vertices.append((new_x, new_y))
        
        self.vertices = new_vertices
        return self