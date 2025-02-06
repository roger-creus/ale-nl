from ocatari.ram.game_objects import NoObject
from ocatari.ram.freeway import Chicken, Car
from IPython import embed

def make_caption(ram, objs):
    object_dict = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in (Chicken, Car)
    }

    for key, items in object_dict.items():
        object_dict[key] = sorted(items, key=lambda obj: (obj.center[1], obj.center[0]))

    chickens = object_dict.get('Chicken', [])
    cars = object_dict.get('Car', [])

    chicken = chickens[0]
    caption = f"The chicken is at position (x={chicken.center[0]}, y={chicken.center[1]}).\n"

    caption += describe_car_positions(cars)
    return caption


def describe_car_positions(cars):
    if not cars:
        return "There are no cars on the road."

    lanes = {}
    for car in cars:
        y = car.center[1]
        lanes.setdefault(y, []).append(car.center[0])

    lane_descriptions = []
    for y in sorted(lanes):
        x_positions = sorted(lanes[y])
        count = len(x_positions)
        pos_text = ", ".join(str(x) for x in x_positions)
        car_word = "car" if count == 1 else "cars"
        lane_descriptions.append(
            f"In lane y = {y}, there {'is' if count == 1 else 'are'} {count} {car_word} at x positions: {pos_text}."
        )

    return "\n".join(lane_descriptions)