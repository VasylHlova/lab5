import unittest
import math
import sys
import os

# Add the parent directory to sys.path to import modules correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shapes.primitives import Triangle, Rectangle, Circle
from shapes.primitives import LabelledColoredRectangle, LabelledColoredCircle, LabelledColoredTriangle
from shapes.poligons import Polygon


class TestTriangle(unittest.TestCase):
    """Test cases for the Triangle class."""
    
    def test_init(self):
        """Test triangle initialization."""
        t = Triangle(3, 4, 5, 1, 2, 30)
        self.assertEqual(t.a, 3)
        self.assertEqual(t.b, 4)
        self.assertEqual(t.c, 5)
        self.assertEqual(t.x, 1)
        self.assertEqual(t.y, 2)
        self.assertEqual(t.angle, 30)
    
    def test_area(self):
        """Test triangle area calculation using Heron's formula."""
        # Right triangle 3-4-5
        t = Triangle(3, 4, 5, 0, 0, 0)
        self.assertEqual(t.area(), 6)
        
        # Equilateral triangle with side 10
        t = Triangle(10, 10, 10, 0, 0, 0)
        # Area = (s^2 * sqrt(3))/4 where s is side length
        expected_area = (10**2 * math.sqrt(3))/4
        self.assertAlmostEqual(t.area(), expected_area, places=10)
    
    def test_perimeter(self):
        """Test triangle perimeter calculation."""
        t = Triangle(3, 4, 5, 0, 0, 0)
        self.assertEqual(t.perimeter(), 12)
    
    def test_move(self):
        """Test moving a triangle."""
        t = Triangle(3, 4, 5, 1, 2, 0)
        t.move(2, 3)
        self.assertEqual(t.x, 3)
        self.assertEqual(t.y, 5)
    
    def test_rotate(self):
        """Test rotating a triangle."""
        t = Triangle(3, 4, 5, 0, 0, 30)
        t.rotate(60)
        self.assertEqual(t.angle, 90)
        
        # Test wraparound
        t.rotate(300)
        self.assertEqual(t.angle, 30)


class TestRectangle(unittest.TestCase):
    """Test cases for the Rectangle class."""
    
    def test_init(self):
        """Test rectangle initialization."""
        r = Rectangle(5, 10, 1, 2, 45)
        self.assertEqual(r.a, 5)
        self.assertEqual(r.b, 10)
        self.assertEqual(r.x, 1)
        self.assertEqual(r.y, 2)
        self.assertEqual(r.angle, 45)
    
    def test_area(self):
        """Test rectangle area calculation."""
        r = Rectangle(5, 10, 0, 0, 0)
        self.assertEqual(r.area(), 50)
    
    def test_perimeter(self):
        """Test rectangle perimeter calculation."""
        r = Rectangle(5, 10, 0, 0, 0)
        self.assertEqual(r.perimeter(), 30)
    
    def test_move(self):
        """Test moving a rectangle."""
        r = Rectangle(5, 10, 1, 2, 0)
        r.move(3, 4)
        self.assertEqual(r.x, 4)
        self.assertEqual(r.y, 6)
    
    def test_rotate(self):
        """Test rotating a rectangle."""
        r = Rectangle(5, 10, 0, 0, 0)
        r.rotate(45)
        self.assertEqual(r.angle, 45)
        
        # Test wraparound
        r.rotate(330)
        self.assertEqual(r.angle, 15)


class TestCircle(unittest.TestCase):
    """Test cases for the Circle class."""
    
    def test_init(self):
        """Test circle initialization."""
        c = Circle(5, 1, 2, 0)
        self.assertEqual(c.r, 5)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 2)
        self.assertEqual(c.angle, 0)
    
    def test_properties(self):
        """Test circle properties."""
        c = Circle(5, 1, 2, 0)
        self.assertEqual(c.center, (1, 2))
        self.assertEqual(c.radius, 5)
    
    def test_area(self):
        """Test circle area calculation."""
        c = Circle(5, 0, 0, 0)
        # Using 3.14 as the circle's implementation does
        self.assertEqual(c.area(), 3.14 * 25)
    
    def test_perimeter(self):
        """Test circle perimeter (circumference) calculation."""
        c = Circle(5, 0, 0, 0)
        # Using 3.14 as the circle's implementation does
        self.assertEqual(c.perimeter(), 2 * 3.14 * 5)
    
    def test_move(self):
        """Test moving a circle."""
        c = Circle(5, 1, 2, 0)
        c.move(3, 4)
        self.assertEqual(c.x, 4)
        self.assertEqual(c.y, 6)
        self.assertEqual(c.center, (4, 6))
    
    def test_rotate(self):
        """Test rotating a circle."""
        c = Circle(5, 0, 0, 0)
        c.rotate(45)
        self.assertEqual(c.angle, 45)


class TestPolygon(unittest.TestCase):
    """Test cases for the Polygon class."""
    
    def test_init(self):
        """Test polygon initialization."""
        vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        p = Polygon(vertices, 30)
        self.assertEqual(p.vertices, vertices)
        self.assertEqual(p.angle, 30)
    
    def test_init_invalid(self):
        """Test invalid polygon initialization."""
        # Less than 3 vertices
        with self.assertRaises(ValueError):
            Polygon([(0, 0), (1, 0)], 0)
    
    def test_perimeter(self):
        """Test polygon perimeter calculation."""
        # Square with side 1
        p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], 0)
        self.assertEqual(p.perimeter(), 4)
    
    def test_area(self):
        """Test polygon area calculation using Shoelace formula."""
        # Square with side 1
        p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], 0)
        self.assertEqual(p.area(), 1)
        
        # Triangle
        p = Polygon([(0, 0), (1, 0), (0, 1)], 0)
        self.assertEqual(p.area(), 0.5)
    
    def test_centroid(self):
        """Test polygon centroid calculation."""
        # Square with side 1 centered at (0.5, 0.5)
        p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], 0)
        self.assertEqual(p._calculate_centroid(), (0.5, 0.5))
        
        # Triangle
        p = Polygon([(0, 0), (3, 0), (0, 3)], 0)
        self.assertEqual(p._calculate_centroid(), (1, 1))
    
    def test_move(self):
        """Test moving a polygon."""
        p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], 0)
        p.move(2, 3)
        self.assertEqual(p.vertices, [(2, 3), (3, 3), (3, 4), (2, 4)])
    
    def test_rotate(self):
        """Test rotating a polygon."""
        # Square with side 1 centered at (0.5, 0.5)
        p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], 0)
        p.rotate(90)
        
        # After 90 degree rotation, vertices should be roughly:
        # [(1, 0), (1, 1), (0, 1), (0, 0)] when rotating around center (0.5, 0.5)
        # Check with rounding due to floating point precision
        expected = [(1, 0), (1, 1), (0, 1), (0, 0)]
        for actual, expected_vertex in zip(p.vertices, expected):
            self.assertAlmostEqual(actual[0], expected_vertex[0], places=10)
            self.assertAlmostEqual(actual[1], expected_vertex[1], places=10)


class TestColorMixin(unittest.TestCase):
    """Test cases for the ColorMixin."""
    
    def test_color_in_labeled_rectangle(self):
        """Test color functionality in LabelledColoredRectangle."""
        rect = LabelledColoredRectangle(5, 10, 0, 0, 0, color="red", label="test")
        self.assertEqual(rect.color, "red")
        
        # Test set_color method
        rect.set_color("blue")
        self.assertEqual(rect.color, "blue")
    
    def test_color_in_labeled_circle(self):
        """Test color functionality in LabelledColoredCircle."""
        circle = LabelledColoredCircle(5, 0, 0, 0, color="green", label="test")
        self.assertEqual(circle.color, "green")
        
        # Test set_color method
        circle.set_color("yellow")
        self.assertEqual(circle.color, "yellow")


class TestLabelMixin(unittest.TestCase):
    """Test cases for the LabelMixin."""
    
    def test_label_in_labeled_rectangle(self):
        """Test label functionality in LabelledColoredRectangle."""
        rect = LabelledColoredRectangle(5, 10, 0, 0, 0, color="red", label="Rectangle 1")
        self.assertEqual(rect.label, "Rectangle 1")
        
        # Test set_label method
        rect.set_label("New Label")
        self.assertEqual(rect.label, "New Label")
    
    def test_label_in_labeled_circle(self):
        """Test label functionality in LabelledColoredCircle."""
        circle = LabelledColoredCircle(5, 0, 0, 0, color="green", label="Circle 1")
        self.assertEqual(circle.label, "Circle 1")
        
        # Test set_label method
        circle.set_label("New Circle Label")
        self.assertEqual(circle.label, "New Circle Label")


class TestLabelledColoredShapes(unittest.TestCase):
    """Test cases for combined labeled and colored shapes."""
    
    def test_labeled_colored_rectangle(self):
        """Test LabelledColoredRectangle functionality."""
        rect = LabelledColoredRectangle(5, 10, 1, 2, 45, color="red", label="test")
        
        # Test that it inherits Rectangle functionality
        self.assertEqual(rect.area(), 50)
        self.assertEqual(rect.perimeter(), 30)
        
        # Test that it inherits ColorMixin functionality
        self.assertEqual(rect.color, "red")
        rect.set_color("blue")
        self.assertEqual(rect.color, "blue")
        
        # Test that it inherits LabelMixin functionality
        self.assertEqual(rect.label, "test")
        rect.set_label("new label")
        self.assertEqual(rect.label, "new label")
    
    def test_labeled_colored_circle(self):
        """Test LabelledColoredCircle functionality."""
        circle = LabelledColoredCircle(5, 1, 2, 45, color="green", label="circle test")
        
        # Test that it inherits Circle functionality
        self.assertEqual(circle.area(), 3.14 * 25)
        
        # Test that it inherits ColorMixin functionality
        self.assertEqual(circle.color, "green")
        
        # Test that it inherits LabelMixin functionality
        self.assertEqual(circle.label, "circle test")
    
    def test_labeled_colored_triangle(self):
        """Test LabelledColoredTriangle functionality."""
        triangle = LabelledColoredTriangle(3, 4, 5, 1, 2, 30, color="blue", label="triangle test")
        
        # Test that it inherits Triangle functionality
        self.assertEqual(triangle.area(), 6)
        
        # Test that it inherits ColorMixin functionality
        self.assertEqual(triangle.color, "blue")
        
        # Test that it inherits LabelMixin functionality
        self.assertEqual(triangle.label, "triangle test")


if __name__ == '__main__':
    unittest.main()