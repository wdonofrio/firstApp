import pytest
from unittest.mock import Mock
from kivy.uix.widget import Widget

from src.objects import ConcreteObject


def test_collides_with():
    concrete_object = ConcreteObject()
    mock_widget = Mock(spec=Widget)

    concrete_object.collide_widget = Mock(return_value=True)
    assert concrete_object.collides_with(mock_widget) is True
    concrete_object.collide_widget = Mock(return_value=False)
    assert concrete_object.collides_with(mock_widget) is False
    concrete_object.collide_widget = Mock(return_value=None)
    assert concrete_object.collides_with(mock_widget) is None


@pytest.mark.skip(reason="Not setup")
@pytest.mark.parametrize(
    "concrete_center_x, concrete_center_y, concrete_width, concrete_height, obj_center_x, obj_center_y, expected_velocity",
    [
        (100, 200, 50, 50, 150, 250, (-1, -1)),  # Normal collision scenario
        (100, 200, 50, 50, 120, 210, (-1, -1)),  # Collision with a different center point
        (100, 200, 50, 50, 140, 200, (-1, -1)),  # Collision with a different center_x value
        (100, 200, 50, 50, 150, 220, (-1, -1)),  # Collision with a different center_y value
        (100, 200, 50, 50, 160, 250, (1, 1)),  # No collision scenario
    ],
)
def test_bounce_obj(concrete_center_x, concrete_center_y, concrete_width, concrete_height, obj_center_x, obj_center_y, expected_velocity):
    concrete_object = ConcreteObject()
    concrete_object.collide_widget = Mock(return_value=True)
    concrete_object.center_x = concrete_center_x
    concrete_object.center_y = concrete_center_y
    concrete_object.width = concrete_width
    concrete_object.height = concrete_height

    obj = Mock()
    obj.center_x = obj_center_x
    obj.center_y = obj_center_y
    obj.velocity = (1, 1)

    concrete_object.bounce_obj(obj)
    assert obj.velocity == expected_velocity
