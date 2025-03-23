from typing import List, Tuple, Optional, Union
from shapes.primitives import Circle, Rectangle, Triangle  # Fixed typo from Triangel

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ShapeUtils:
    """Utility class for shape operations."""
    
    @staticmethod
    def shape_to_vertices(shape: Union[Rectangle, 'Triangle']) -> Optional[List[Tuple[float, float]]]:
        """
        Converts a shape to a list of vertices.
        
        Args:
            shape: A geometric shape (Rectangle or Triangle)
            
        Returns:
            List of (x, y) vertex coordinates or None if shape is not supported
        """
        if isinstance(shape, Rectangle):
            x, y = shape.x, shape.y
            return [(x, y), (x + shape.a, y), 
                    (x + shape.a, y + shape.b), 
                    (x, y + shape.b)]
        elif isinstance(shape, Triangle):
            x, y = shape.x, shape.y
            return [(x, y), (x + shape.a, y), (x + shape.a/2, y + shape.b)]
        return None
    
    @staticmethod
    def circle_rectangle_intersection(circle: Circle, rect: Rectangle) -> bool:
        """
        Checks if a circle and rectangle intersect.
        
        Args:
            circle: The circle object
            rect: The rectangle object
            
        Returns:
            True if shapes intersect, False otherwise
        """
        # Find closest point of rectangle to circle center
        closest_x = max(rect.x, min(circle.center[0], rect.x + rect.a))
        closest_y = max(rect.y, min(circle.center[1], rect.y + rect.b))
        
        # Calculate squared distance between closest point and circle center
        distance_squared = (closest_x - circle.center[0])**2 + (closest_y - circle.center[1])**2
        
        # If distance is less than or equal to circle radius, shapes intersect
        return distance_squared <= circle.radius**2
    
    @staticmethod
    def circle_rectangle_distance(circle: Circle, rect: Rectangle) -> float:
        """
        Calculates the minimum distance between a circle and rectangle.
        
        Args:
            circle: The circle object
            rect: The rectangle object
            
        Returns:
            The minimum distance between the shapes (0 if they intersect)
        """
        # Find closest point of rectangle to circle center
        closest_x = max(rect.x, min(circle.center[0], rect.x + rect.a))
        closest_y = max(rect.y, min(circle.center[1], rect.y + rect.b))
        
        # Calculate distance between closest point and circle center
        distance = ((closest_x - circle.center[0])**2 + (closest_y - circle.center[1])**2)**0.5
        
        # Subtract radius (but not less than 0)
        return max(0, distance - circle.radius)
    
    @staticmethod
    def is_point_inside_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
        """
        Checks if a point is inside a polygon.
        
        Args:
            point: The (x, y) coordinates of the point
            polygon: List of polygon vertices [(x1, y1), (x2, y2), ...]
            
        Returns:
            True if the point is inside the polygon, False otherwise
        """
        x, y = point
        n = len(polygon)
        inside = False

        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n] 

            if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = True

        return inside
    
    @staticmethod
    def line_intersects(p1: Tuple[float, float], p2: Tuple[float, float], 
                       q1: Tuple[float, float], q2: Tuple[float, float]) -> bool:
        """
        Checks if two line segments (p1, p2) and (q1, q2) intersect.
        
        Args:
            p1: First point of the first line segment
            p2: Second point of the first line segment
            q1: First point of the second line segment
            q2: Second point of the second line segment
            
        Returns:
            True if the line segments intersect, False otherwise
        """
        def cross_product(a: Tuple[float, float], b: Tuple[float, float]) -> float:
            return a[0] * b[1] - a[1] * b[0]

        def direction(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
            return cross_product((c[0] - a[0], c[1] - a[1]), (b[0] - a[0], b[1] - a[1]))

        d1 = direction(p1, p2, q1)
        d2 = direction(p1, p2, q2)
        d3 = direction(q1, q2, p1)
        d4 = direction(q1, q2, p2)

        return (d1 * d2 < 0 and d3 * d4 < 0)
    


