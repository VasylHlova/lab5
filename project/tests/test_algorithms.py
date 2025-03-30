import unittest
import sys
import os
import math

# Add the parent directory to sys.path to import modules correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operations.algorithms import (
    Map, ShapeActions, check_crossing, distance_between_shapes,
    search_shapes_by_area, search_shapes_by_position, polygons_intersect
)
from shapes.primitives import Triangle, Rectangle, Circle
from utils.geometry import ShapeUtils

class TestShapeUtils(unittest.TestCase):
    """Test cases for the ShapeUtils utility class."""
    
    def setUp(self):
        self.rectangle = Rectangle(5, 3, 1, 2, 0)
        self.triangle = Triangle(5, 4, 3, 5, 45, 0) 
        self.circle = Circle(3, 4, 4, 0)
    
    def test_shape_to_vertices_rectangle(self):
        """Test converting a rectangle to vertices."""
        vertices = ShapeUtils.shape_to_vertices(self.rectangle)
        expected = [(1, 2), (6, 2), (6, 5), (1, 5)]
        self.assertEqual(vertices, expected)
        
    def test_shape_to_vertices_unsupported(self):
        """Test converting an unsupported shape returns None."""
        vertices = ShapeUtils.shape_to_vertices(self.circle)
        self.assertIsNone(vertices)
    
    def test_circle_rectangle_intersection_overlapping(self):
        """Test detecting intersection between circle and rectangle."""
        rect = Rectangle(4, 4, 3, 3, 0)
        self.assertTrue(ShapeUtils.circle_rectangle_intersection(self.circle, rect))
    
    def test_circle_rectangle_intersection_non_overlapping(self):
        """Test detecting non-intersection between circle and rectangle."""
        rect = Rectangle(4, 4, 10, 10, 0)
        self.assertFalse(ShapeUtils.circle_rectangle_intersection(self.circle, rect))
    
    def test_circle_rectangle_intersection_touching(self):
        """Test detecting when circle touches rectangle edge."""
        # Circle at (4,4) with radius 3, rectangle at (7,4) with width 4
        rect = Rectangle(4, 4, 7, 4, 0)
        self.assertTrue(ShapeUtils.circle_rectangle_intersection(self.circle, rect))
    
    def test_circle_rectangle_distance_overlapping(self):
        """Test distance between overlapping shapes is 0."""
        rect = Rectangle(4, 4, 3, 3, 0)
        self.assertEqual(ShapeUtils.circle_rectangle_distance(self.circle, rect), 0)
    
    def test_circle_rectangle_distance_non_overlapping(self):
        """Test distance between non-overlapping shapes."""
        # Circle at (4,4) with radius 3, rectangle at (10,10) with width/height 2
        rect = Rectangle(2, 2, 10, 10, 0)
        # Closest distance from rectangle (10,10) to circle center (4,4) is sqrt(72) = 8.485...
        # Minus radius 3 = 5.485...
        expected_distance = math.sqrt(72) - 3
        self.assertAlmostEqual(ShapeUtils.circle_rectangle_distance(self.circle, rect), expected_distance)
    
    def test_is_point_inside_polygon_way1(self):
        """Test if point is inside polygon using angle method."""
        polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]  # Square
        self.assertTrue(ShapeUtils.is_point_inside_polygon_way1((5, 5), polygon))
        self.assertFalse(ShapeUtils.is_point_inside_polygon_way1((15, 15), polygon))
        
        # Test point on vertex
        self.assertTrue(ShapeUtils.is_point_inside_polygon_way1((0, 0), polygon))
        
        # Test concave polygon
        concave = [(0, 0), (10, 0), (10, 10), (5, 5), (0, 10)]
        self.assertTrue(ShapeUtils.is_point_inside_polygon_way1((2, 2), concave))
        self.assertFalse(ShapeUtils.is_point_inside_polygon_way1((11, 11), concave))
    
    def test_is_point_inside_polygon_way2(self):
        """Test if point is inside polygon using cross product method."""
        polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]  # Square
        self.assertTrue(ShapeUtils.is_point_inside_polygon_way2((5, 5), polygon))
        self.assertFalse(ShapeUtils.is_point_inside_polygon_way2((15, 15), polygon))
        
        # Test point on edge
        self.assertTrue(ShapeUtils.is_point_inside_polygon_way2((5, 0), polygon))
        
        # Test concave polygon
        concave = [(0, 0), (10, 0), (10, 10), (5, 5), (0, 10)]
        self.assertTrue(ShapeUtils.is_point_inside_polygon_way2((2, 2), concave))
        self.assertFalse(ShapeUtils.is_point_inside_polygon_way2((6, 6), concave))
    
    def test_line_intersects(self):
        """Test line intersection detection."""
        # Intersecting lines
        self.assertTrue(ShapeUtils.line_intersects((0, 0), (10, 10), (0, 10), (10, 0)))
        
        # Non-intersecting lines
        self.assertFalse(ShapeUtils.line_intersects((0, 0), (5, 5), (6, 6), (10, 10)))
        
        # Parallel lines
        self.assertFalse(ShapeUtils.line_intersects((0, 0), (5, 0), (0, 5), (5, 5)))
        
        # Lines sharing an endpoint
        self.assertFalse(ShapeUtils.line_intersects((0, 0), (5, 5), (5, 5), (10, 10)))
        
        # Lines that touch but don't cross - the implementation doesn't count this as intersection
        self.assertFalse(ShapeUtils.line_intersects((0, 0), (5, 5), (5, 5), (10, 0)))


class TestMap(unittest.TestCase):
    """Test cases for the Map class."""
    
    def setUp(self):
        self.map = Map()
        self.rectangle = Rectangle(5, 3, 0, 0, 0)
        self.circle = Circle(3, 4, 4, 0)
        self.triangle = Triangle(5, 4, 3, 5, 5, 0)
        
    def test_add_shape(self):
        """Test adding shapes to the map."""
        initial_count = len(self.map.shapes)
        self.map.add_shape(self.rectangle)
        self.assertEqual(len(self.map.shapes), initial_count + 1)
        self.assertIn(self.rectangle, self.map.shapes)
    
    def test_add_invalid_shape(self):
        """Test adding an invalid shape raises TypeError."""
        with self.assertRaises(TypeError):
            self.map.add_shape("Not a shape")
    
    def test_remove_shape(self):
        """Test removing shapes from the map."""
        self.map.add_shape(self.rectangle)
        self.map.add_shape(self.circle)
        initial_count = len(self.map.shapes)
        self.map.remove_shape(self.rectangle)
        self.assertEqual(len(self.map.shapes), initial_count - 1)
        self.assertNotIn(self.rectangle, self.map.shapes)
        self.assertIn(self.circle, self.map.shapes)
    
    def test_remove_nonexistent_shape(self):
        """Test removing a shape that isn't in the map."""
        initial_count = len(self.map.shapes)
        self.map.remove_shape(self.rectangle)  # Rectangle not in map
        self.assertEqual(len(self.map.shapes), initial_count)
    
    def test_total_area(self):
        """Test calculating total area of all shapes in the map."""
        self.map.add_shape(self.rectangle)
        self.map.add_shape(self.circle)
        expected_area = self.rectangle.area() + self.circle.area()
        self.assertAlmostEqual(self.map.total_area(), expected_area)
    
    def test_total_perimeter(self):
        """Test calculating total perimeter of all shapes in the map."""
        self.map.add_shape(self.rectangle)
        self.map.add_shape(self.circle)
        expected_perimeter = self.rectangle.perimeter() + self.circle.perimeter()
        self.assertAlmostEqual(self.map.total_perimeter(), expected_perimeter)
    
    def test_empty_map(self):
        """Test operations on an empty map."""
        self.assertEqual(len(self.map.shapes), 0)
        self.assertEqual(self.map.total_area(), 0)
        self.assertEqual(self.map.total_perimeter(), 0)


class TestCheckCrossing(unittest.TestCase):
    """Test cases for the check_crossing function."""
    
    def test_intersecting_circles(self):
        """Test intersecting circles return True."""
        circle1 = Circle(3, 0, 0, 0)
        circle2 = Circle(3, 5, 0, 0)
        self.assertTrue(check_crossing(circle1, circle2))
    
    def test_non_intersecting_circles(self):
        """Test non-intersecting circles return False."""
        circle1 = Circle(3, 0, 0, 0)
        circle2 = Circle(3, 7, 0, 0)
        self.assertFalse(check_crossing(circle1, circle2))
    
    def test_touching_circles(self):
        """Test touching circles return True."""
        circle1 = Circle(3, 0, 0, 0)
        circle2 = Circle(3, 6, 0, 0)  # Exactly touching
        self.assertTrue(check_crossing(circle1, circle2))
    
    def test_intersecting_rectangles(self):
        """Test intersecting rectangles return True."""
        rect1 = Rectangle(5, 5, 0, 0, 0)
        rect2 = Rectangle(5, 5, 3, 3, 0)
        self.assertTrue(check_crossing(rect1, rect2))
    
    def test_non_intersecting_rectangles(self):
        """Test non-intersecting rectangles return False."""
        rect1 = Rectangle(5, 5, 0, 0, 0)
        rect2 = Rectangle(5, 5, 10, 10, 0)
        self.assertFalse(check_crossing(rect1, rect2))
    
    def test_touching_rectangles(self):
        """Test touching rectangles return True."""
        rect1 = Rectangle(5, 5, 0, 0, 0)
        rect2 = Rectangle(5, 5, 5, 0, 0)  # Touching at edge
        self.assertTrue(check_crossing(rect1, rect2))
    
    def test_circle_rectangle_intersection(self):
        """Test circle-rectangle intersection."""
        circle = Circle(3, 5, 5, 0)
        rect = Rectangle(5, 5, 0, 0, 0)
        self.assertTrue(check_crossing(circle, rect))
        
        # Test reverse order too
        self.assertTrue(check_crossing(rect, circle))
    
    def test_circle_rectangle_no_intersection(self):
        """Test non-intersecting circle and rectangle."""
        circle = Circle(3, 10, 10, 0)
        rect = Rectangle(5, 5, 0, 0, 0)
        self.assertFalse(check_crossing(circle, rect))


class TestDistanceBetweenShapes(unittest.TestCase):
    """Test cases for the distance_between_shapes function."""
    
    def test_intersecting_shapes_distance_zero(self):
        """Test intersecting shapes return distance of 0."""
        circle1 = Circle(3, 0, 0, 0)
        circle2 = Circle(3, 5, 0, 0)
        self.assertEqual(distance_between_shapes(circle1, circle2), 0)
    
    def test_circle_circle_distance(self):
        """Test distance between non-intersecting circles."""
        circle1 = Circle(3, 0, 0, 0)
        circle2 = Circle(3, 10, 0, 0)
        # Centers are 10 units apart, each radius is 3, so distance is 10 - 3 - 3 = 4
        self.assertEqual(distance_between_shapes(circle1, circle2), 4)
    
    def test_rectangle_rectangle_distance(self):
        """Test distance between non-intersecting rectangles."""
        rect1 = Rectangle(5, 5, 0, 0, 0)
        rect2 = Rectangle(5, 5, 10, 0, 0)
        # Horizontal distance = 10 - 5 = 5
        self.assertEqual(distance_between_shapes(rect1, rect2), 5)
        
        # Test diagonal distance
        rect3 = Rectangle(5, 5, 10, 10, 0)
        # Diagonal distance should be sqrt(5^2 + 5^2) = sqrt(50) = 7.071...
        self.assertAlmostEqual(distance_between_shapes(rect1, rect3), math.sqrt(50))
    
    def test_circle_rectangle_distance(self):
        """Test distance between non-intersecting circle and rectangle."""
        circle = Circle(3, 15, 5, 0)
        rect = Rectangle(5, 5, 0, 0, 0)
        # Rectangle ends at (5,5), circle center at (15,5)
        # Horizontal distance from edge to center = 15 - 5 = 10
        # Subtract radius = 10 - 3 = 7
        self.assertEqual(distance_between_shapes(circle, rect), 7)
        
        # Test reverse order
        self.assertEqual(distance_between_shapes(rect, circle), 7)


class TestSearchShapesByArea(unittest.TestCase):
    """Test cases for the search_shapes_by_area function."""
    
    def setUp(self):
        self.map = Map()
        self.rectangle = Rectangle(5, 5, 0, 0, 0)  # Area = 25
        self.circle = Circle(3, 4, 4, 0)  # Area = 9π ≈ 28.27
        self.triangle = Triangle(5, 4, 3, 5, 5, 0)  # Area depends on implementation
        
        self.map.add_shape(self.rectangle)
        self.map.add_shape(self.circle)
        self.map.add_shape(self.triangle)
    
    def test_find_exact_area_match(self):
        """Test finding shapes with exact area match."""
        rectangle_area = self.rectangle.area()
        results = search_shapes_by_area(self.map, rectangle_area)
        self.assertEqual(len(results), 1)
        self.assertIn(self.rectangle, results)
    
    def test_find_no_matches(self):
        """Test finding shapes with no matching area."""
        results = search_shapes_by_area(self.map, 100)
        self.assertEqual(len(results), 0)
    
    def test_find_multiple_matches(self):
        """Test finding multiple shapes with same area."""
        # Add another rectangle with the same area
        same_area_rect = Rectangle(25, 1, 10, 10, 0)  # Area = 25
        self.map.add_shape(same_area_rect)
        
        rectangle_area = self.rectangle.area()
        results = search_shapes_by_area(self.map, rectangle_area)
        self.assertEqual(len(results), 2)
        self.assertIn(self.rectangle, results)
        self.assertIn(same_area_rect, results)


class TestSearchShapesByPosition(unittest.TestCase):
    """Test cases for the search_shapes_by_position function."""
    
    def setUp(self):
        self.map = Map()
        self.rectangle = Rectangle(5, 5, 0, 0, 0)
        self.circle = Circle(3, 4, 4, 0)
        self.triangle = Triangle(5, 4, 3, 5, 5, 0)
        
        self.map.add_shape(self.rectangle)
        self.map.add_shape(self.circle)
        self.map.add_shape(self.triangle)
    
    def test_point_inside_rectangle(self):
        """Test finding a rectangle containing a point."""
        results = search_shapes_by_position(self.map, 2, 2)
        self.assertIn(self.rectangle, results)
    
    def test_point_inside_circle(self):
        """Test finding a circle containing a point."""
        results = search_shapes_by_position(self.map, 4, 4)
        self.assertIn(self.circle, results)
    
    def test_point_outside_all_shapes(self):
        """Test point outside all shapes returns empty list."""
        results = search_shapes_by_position(self.map, 20, 20)
        self.assertEqual(len(results), 0)
    
    def test_point_inside_multiple_shapes(self):
        """Test point inside multiple shapes returns all containing shapes."""
        # Add a rectangle that overlaps with the circle
        test_map = Map()
        
        # Add two overlapping rectangles
        rect1 = Rectangle(5, 5, 0, 0, 0)
        rect2 = Rectangle(10, 10, 0, 0, 0)
        
        test_map.add_shape(rect1)
        test_map.add_shape(rect2)
        
        # Point (2,2) should be inside both rectangles
        results = search_shapes_by_position(test_map, 2, 2)
        self.assertEqual(len(results), 2)
        self.assertIn(rect1, results)
        self.assertIn(rect2, results)


class TestPolygonsIntersect(unittest.TestCase):
    """Test cases for the polygons_intersect function."""
    
    def test_intersecting_polygons(self):
        """Test intersecting polygons return True."""
        poly1 = [(0, 0), (10, 0), (10, 10), (0, 10)]
        poly2 = [(5, 5), (15, 5), (15, 15), (5, 15)]
        self.assertTrue(polygons_intersect(poly1, poly2))
    
    def test_non_intersecting_polygons(self):
        """Test non-intersecting polygons return False."""
        poly1 = [(0, 0), (10, 0), (10, 10), (0, 10)]
        poly2 = [(20, 20), (30, 20), (30, 30), (20, 30)]
        self.assertFalse(polygons_intersect(poly1, poly2))
    
    def test_touching_polygons(self):
        """Test touching polygons return True."""
        poly1 = [(0, 0), (10, 0), (10, 10), (0, 10)]
        poly2 = [(10, 0), (20, 0), (20, 10), (10, 10)]
        self.assertTrue(polygons_intersect(poly1, poly2))
    
    def test_polygon_inside_another(self):
        """Test polygon inside another polygon returns True."""
        poly1 = [(0, 0), (10, 0), (10, 10), (0, 10)]
        poly2 = [(2, 2), (8, 2), (8, 8), (2, 8)]
        self.assertTrue(polygons_intersect(poly1, poly2))
    
    def test_edge_edge_intersection(self):
        """Test polygons with edge-edge intersection."""
        poly1 = [(0, 0), (10, 0), (10, 10), (0, 10)]
        poly2 = [(5, -5), (15, 5), (5, 15), (-5, 5)]
        self.assertTrue(polygons_intersect(poly1, poly2))


if __name__ == '__main__':
    unittest.main()