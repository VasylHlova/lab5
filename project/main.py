from shapes.primitives import Triangle, Rectangle, Circle, LabelledColoredRectangle
from shapes.poligons import Polygon
from operations.algorithms import (
    Map, ShapeActions, check_crossing, distance_between_shapes, 
    search_shapes_by_area, search_shapes_by_position
)


def perform_shape_action(action_type: ShapeActions, *args, **kwargs):
    """
    Perform different shape operations based on the action type.
    
    Args:
        action_type: The type of action to perform
        *args, **kwargs: Arguments specific to the action
    
    Returns:
        Result of the requested operation
    """
    if action_type == ShapeActions.CROSSING:
        shape1, shape2 = args
        return check_crossing(shape1, shape2)
    
    elif action_type == ShapeActions.DISTANCE:
        shape1, shape2 = args
        return distance_between_shapes(shape1, shape2)
    
    elif action_type == ShapeActions.SEARCH_BY_AREA:
        map_obj, area = args
        return search_shapes_by_area(map_obj, area)
    
    elif action_type == ShapeActions.SEARCH_BY_POSITION:
        map_obj, x, y = args
        return search_shapes_by_position(map_obj, x, y)
    
    else:
        raise ValueError(f"Unsupported action: {action_type}")

def main():
    """Main function demonstrating the usage of shapes and operations."""
    
    print("Creating shapes...")
    rectangle1 = Rectangle(10, 5, 0, 0, 0)
    rectangle2 = Rectangle(8, 4, 15, 3, 0)
    circle1 = Circle(5, 5, 5, 0)
    circle2 = Circle(3, 20, 10, 0)
    triangle = Triangle(5, 5, 7, 10, 10, 0)
    
    polygon = Polygon([
        (30, 10), (40, 10), (45, 20), (40, 30), (30, 30), (25, 20)
    ])
    
    colored_rect = LabelledColoredRectangle(8, 6, 2, 2, 0, color="blue", label="Blue Rectangle")

    print(f"\nBasic shape properties:")
    print(f"Rectangle 1: Area = {rectangle1.area()}, Perimeter = {rectangle1.perimeter()}")
    print(f"Circle 1: Area = {circle1.area()}, Perimeter = {circle1.perimeter()}")
    print(f"Triangle: Area = {triangle.area()}, Perimeter = {triangle.perimeter()}")
    print(f"Polygon: Area = {polygon.area()}, Perimeter = {polygon.perimeter()}")
    print(f"Colored Rectangle: Color = {colored_rect.color}, Label = {colored_rect.label}")
    
    print("\nCreating map and adding shapes:")
    shape_map = Map()
    shape_map.add_shape(rectangle1)
    shape_map.add_shape(rectangle2)
    shape_map.add_shape(circle1)
    shape_map.add_shape(circle2)
    shape_map.add_shape(triangle)
    shape_map.add_shape(polygon)
    
    print(f"Total shapes in map: {len(shape_map.shapes)}")
    print(f"Total area of all shapes: {shape_map.total_area():.2f}")

    print("\nUsing ShapeActions enum to perform operations:")
    

    print("\nChecking for intersections:")
    is_intersecting = perform_shape_action(ShapeActions.CROSSING, circle1, rectangle1)
    print(f"Circle 1 and Rectangle 1 intersect: {is_intersecting}")
    
   
    print("\nCalculating distances between shapes:")
    distance = perform_shape_action(ShapeActions.DISTANCE, circle1, rectangle2)
    print(f"Distance between Circle 1 and Rectangle 2: {distance:.2f}")
    

    target_area = circle1.area()
    print(f"\nSearching for shapes with area equal to {target_area:.2f}:")
    matching_shapes = perform_shape_action(ShapeActions.SEARCH_BY_AREA, shape_map, target_area)
    print(f"Found {len(matching_shapes)} shape(s) with matching area")
        

    print("\nSearching for shapes at position (5, 5):")
    position_shapes = perform_shape_action(ShapeActions.SEARCH_BY_POSITION, shape_map, 5, 5)
    print(f"Found {len(position_shapes)} shape(s) containing point (5, 5)")

if __name__ == "__main__":
    main()