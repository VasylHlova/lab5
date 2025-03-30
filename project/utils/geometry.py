from typing import List, Tuple, Optional, Union
from shapes.primitives import Circle, Rectangle, Triangle
import math  

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
    def is_point_inside_polygon_way1(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
        total_angle = 0
        n = len(polygon)
        epsilon = 1e-6
        print(f"Testing point {point} with polygon of {n} vertices")
        print(f"Polygon vertices: {polygon}")
        
        for i in range(n):  # Change from n-1 to n to process all vertices
            current_vertex = polygon[i]
            next_vertex = polygon[(i+1)%n]
            
            vector1 = (point[0]-current_vertex[0], point[1]-current_vertex[1])
            vector2 = (point[0]-next_vertex[0], point[1]-next_vertex[1])
            
            len1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
            len2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
            
            if len1 == 0 or len2 == 0:
                print(f"Point is on vertex {current_vertex or next_vertex}")
                return True
            
            dot = vector1[0]*vector2[0] + vector1[1]*vector2[1]
            
            cosin_angle = dot/(len1*len2)
            if abs(cosin_angle) > 1:
                cosin_angle = 1 if cosin_angle > 1 else -1     
            angle = math.acos(cosin_angle)
            
            cross = vector1[0] * vector2[1] - vector1[1] * vector2[0]
            if cross < 0:
                angle = -angle
                
            total_angle += angle
            print(f"Edge {i}: {current_vertex}->{next_vertex}, Angle: {angle:.4f}, Total: {total_angle:.4f}")
        
        result = abs(abs(total_angle) - 2*math.pi) < epsilon
        print(f"Final total: {total_angle:.4f}, Diff from 2π: {abs(abs(total_angle) - 2*math.pi):.8f}, Inside: {result}")
        return result
                       
            
            
    @staticmethod
    def is_point_inside_polygon_way2(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
        n = len(polygon)
        sign = None
        
        for  i in range(n-1):
            current_vertex = polygon[i]
            next_vertex = polygon[(i+1)%n]
            
            edge_vector = (current_vertex[0] - next_vertex[0], current_vertex[1]-next_vertex[1])
            point_vector = (point[0]-current_vertex[0], point[1] - current_vertex[1])
            
            cross_product = edge_vector[0]*point_vector[1] - edge_vector[1]*point_vector[0]
            
            if cross_product == 0:
                continue
            if sign is None:
                sign = (cross_product>0)
            else:
                if (cross_product > 0 ) != sign:
                    return False    
        return True    
    
    @staticmethod
    def line_intersects(line1_p1: Tuple[float, float], line1_p2: Tuple[float, float], 
                       line2_p1: Tuple[float, float], line2_p2: Tuple[float, float]) -> bool:
        """
        Checks if two line segments (p1, p2) and (p1, p2) intersect.
        
        Args:
            line1_p1: First point of the first line segment
            line1_p2: Second point of the first line segment
            line2_p1: First point of the second line segment
            line2_p2: Second point of the second line segment
            
        Returns:
            True if the line segments intersect, False otherwise
        """
        def cross_product(a: Tuple[float, float], b: Tuple[float, float]) -> float:
            return a[0] * b[1] - a[1] * b[0]

        def direction(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
            return cross_product((c[0] - a[0], c[1] - a[1]), (b[0] - a[0], b[1] - a[1]))

        d1 = direction(line1_p1, line1_p2, line2_p1)
        d2 = direction(line1_p1, line1_p2, line2_p2)
        d3 = direction(line2_p1, line2_p2, line1_p1)
        d4 = direction(line2_p1, line2_p2, line1_p2)

        return (d1 * d2 < 0 and d3 * d4 < 0)
    


