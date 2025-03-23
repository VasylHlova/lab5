from typing import List, Tuple
from shapes.primitives import Triangle, Rectangle, Circle
from shapes.poligons import Polygon
from utils.geometry import ShapeUtils
from shapes.base import Shape
from enum import Enum

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Map:
    """Class for managing a collection of shapes."""
    
    def __init__(self):
        self.shapes: List[Shape] = []  

    def add_shape(self, shape: Shape) -> None:
        """
        Add a new shape to the collection.
        
        Args:
            shape: The shape to add
            
        Raises:
            TypeError: If the object is not an instance of Shape or its subclass
        """
        if not isinstance(shape, Shape):
            raise TypeError("Object must be an instance of Shape or its subclass")
        self.shapes.append(shape)

    def remove_shape(self, shape: Shape) -> None:
        """
        Remove a shape from the collection.
        
        Args:
            shape: The shape to remove
        """
        if shape in self.shapes:
            self.shapes.remove(shape)

    def total_area(self) -> float:
        """
        Calculate the total area of all shapes.
        
        Returns:
            The sum of all shape areas
        """
        return sum(shape.area() for shape in self.shapes)

    def total_perimeter(self) -> float:
        """
        Calculate the total perimeter of all shapes.
        
        Returns:
            The sum of all shape perimeters
        """
        return sum(shape.perimeter() for shape in self.shapes)

    def list_shapes(self) -> None:
        """Print a list of all shapes with their areas and perimeters."""
        for i, shape in enumerate(self.shapes, 1):
            print(f"{i}. {shape.__class__.__name__} - Area: {shape.area()}, Perimeter: {shape.perimeter()}")


class ShapeActions(Enum):
    """Enumeration of possible actions on shapes."""
    CROSSING = 'crossing'
    DISTANCE = 'distance'
    SEARCH_BY_AREA = 'search_by_area'
    SEARCH_BY_POSITION = 'search_by_position'
    

def check_crossing(shape1: Shape, shape2: Shape) -> bool:
    """
    Check if two shapes intersect.
    
    Args:
        shape1: First shape
        shape2: Second shape
        
    Returns:
        True if shapes intersect, False otherwise
    """
    
    # Circle - Circle
    if isinstance(shape1, Circle) and isinstance(shape2, Circle):
        center1 = shape1.center
        center2 = shape2.center
        distance_between_centers = ((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)**0.5
        return distance_between_centers <= shape1.radius + shape2.radius
    
    # Rectangle - Rectangle
    elif isinstance(shape1, Rectangle) and isinstance(shape2, Rectangle):
        # Check if one rectangle is to the left of the other
        if (shape1.x + shape1.a < shape2.x or shape2.x + shape2.a < shape1.x):
            return False
        # Check if one rectangle is above the other
        if (shape1.y + shape1.b < shape2.y or shape2.y + shape2.b < shape1.y):
            return False
        return True
    
    # Circle - Rectangle
    elif isinstance(shape1, Circle) and isinstance(shape2, Rectangle):
        return ShapeUtils.circle_rectangle_intersection(shape1, shape2)
    elif isinstance(shape1, Rectangle) and isinstance(shape2, Circle):
        return ShapeUtils.circle_rectangle_intersection(shape2, shape1)
    
    # Triangle handling
    elif isinstance(shape1, Triangle) or isinstance(shape2, Triangle):
        vertices1 = ShapeUtils.shape_to_vertices(shape1)
        vertices2 = ShapeUtils.shape_to_vertices(shape2)
        
        if vertices1 and vertices2:
            return polygons_intersect(vertices1, vertices2)
    
    return False

def distance_between_shapes(shape1: Shape, shape2: Shape) -> float:
    """
    Find the minimum distance between two shapes.
    
    Args:
        shape1: First shape
        shape2: Second shape
        
    Returns:
        The minimum distance (0 if shapes intersect)
    """
    
    # If shapes intersect, distance is 0
    if check_crossing(shape1, shape2):
        return 0.0
    
    # Circle - Circle
    if isinstance(shape1, Circle) and isinstance(shape2, Circle):
        center1 = shape1.center
        center2 = shape2.center
        distance_between_centers = ((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)**0.5
        return max(0, distance_between_centers - shape1.radius - shape2.radius)
    
    # Rectangle - Rectangle
    elif isinstance(shape1, Rectangle) and isinstance(shape2, Rectangle):
        if shape1.x + shape1.a < shape2.x:  
            horiz_dist = shape2.x - (shape1.x + shape1.a)
        elif shape2.x + shape2.a < shape1.x:  
            horiz_dist = shape1.x - (shape2.x + shape2.a)
        else:  
            horiz_dist = 0
        
        if shape1.y + shape1.b < shape2.y:  
            vert_dist = shape2.y - (shape1.y + shape1.b)
        elif shape2.y + shape2.b < shape1.y: 
            vert_dist = shape1.y - (shape2.y + shape2.b)
        else:  
            vert_dist = 0
        
        if horiz_dist == 0 and vert_dist == 0:
            return 0
        
        if horiz_dist == 0:
            return vert_dist
        if vert_dist == 0:
            return horiz_dist
        
        return (horiz_dist**2 + vert_dist**2)**0.5
    
    # Circle - Rectangle
    elif isinstance(shape1, Circle) and isinstance(shape2, Rectangle):
        return ShapeUtils.circle_rectangle_distance(shape1, shape2)
    elif isinstance(shape1, Rectangle) and isinstance(shape2, Circle):
        return ShapeUtils.circle_rectangle_distance(shape2, shape1)
    
    return float('inf')

def search_shapes_by_area(map: Map, area: float) -> List[Shape]:
    """
    Find shapes with area equal to the specified value.
    
    Args:
        map: The collection of shapes to search
        area: The target area value
        
    Returns:
        List of shapes with matching area
    """
    return [shape for shape in map.shapes if shape.area() == area]

def search_shapes_by_position(map: Map, x: float, y: float) -> List[Shape]:
    """
    Find shapes that contain the specified point.
    
    Args:
        map: The collection of shapes to search
        x: X-coordinate of the point
        y: Y-coordinate of the point
        
    Returns:
        List of shapes that contain the point
    """    
    result = []
    
    for shape in map.shapes:
        if isinstance(shape, Rectangle):
            # Check if point is inside rectangle
            if (shape.x <= x <= shape.x + shape.a and 
                shape.y <= y <= shape.y + shape.b):
                result.append(shape)
                
        elif isinstance(shape, Circle):
            # Check if point is inside circle
            dx = x - shape.center[0]
            dy = y - shape.center[1]
            distance_squared = dx*dx + dy*dy
            if distance_squared <= shape.radius * shape.radius:
                result.append(shape)
                
        elif isinstance(shape, Triangle):
            # Use ShapeUtils to convert to vertices and check
            vertices = ShapeUtils.shape_to_vertices(shape)
            if vertices and ShapeUtils.is_point_inside_polygon((x, y), vertices):
                result.append(shape)
                
        elif isinstance(shape, Polygon):
            # Polygon already has vertices
            if hasattr(shape, 'vertices') and ShapeUtils.is_point_inside_polygon((x, y), shape.vertices):
                result.append(shape)
    
    return result
def polygons_intersect(poly1: List[Tuple[float, float]], poly2: List[Tuple[float, float]]) -> bool:
    """
    Check if two polygons intersect.
    
    Args:
        poly1: List of vertices for first polygon [(x1, y1), (x2, y2), ...]
        poly2: List of vertices for second polygon [(x1, y1), (x2, y2), ...]
        
    Returns:
        True if polygons intersect, False otherwise
    """
    # Check if any vertex of one polygon is inside the other
    if any(ShapeUtils.is_point_inside_polygon(p, poly2) for p in poly1) or \
       any(ShapeUtils.is_point_inside_polygon(p, poly1) for p in poly2):
        return True

    # Check if any edges intersect
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            if ShapeUtils.line_intersects(poly1[i], poly1[(i + 1) % len(poly1)], 
                               poly2[j], poly2[(j + 1) % len(poly2)]):
                return True
    return False