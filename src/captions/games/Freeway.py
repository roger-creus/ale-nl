from ocatari.ram.game_objects import NoObject
from ocatari.ram.freeway import Chicken, Car

def make_caption(ram, objs):
    object_dict = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in (Chicken, Car)
    }

    for key, items in object_dict.items():
        object_dict[key] = sorted(items, key=lambda obj: (obj.center[1], obj.center[0]))

    chickens = object_dict.get("Chicken", [])
    cars = object_dict.get("Car", [])

    lines = []

    if chickens:
        chicken = chickens[0]
        lines.append(f"Chicken Position: x={chicken.center[0]}, y={chicken.center[1]}")

    lines.extend(describe_car_positions(cars))
    
    return "\n".join(lines)


def describe_car_positions(cars):
    if not cars:
        return ["No Cars: True"]

    lanes = {}
    for car in cars:
        y = car.center[1]
        lanes.setdefault(y, []).append(car.center[0])

    lane_descriptions = []
    for y in sorted(lanes):
        x_positions = sorted(lanes[y])
        for i, x in enumerate(x_positions):
            lane_descriptions.append(f"Lane {y} Car {i+1} Position: x={x}")

    return lane_descriptions
