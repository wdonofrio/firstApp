import pytest
from unittest.mock import Mock
from kivy.uix.widget import Widget

from src.objects import ConcreteObject


def test_collides_with_returns_true_when_collision_occurs():
    concrete_object = ConcreteObject()
    mock_widget = Mock(spec=Widget)
    concrete_object.collide_widget = Mock(return_value=True)

    result = concrete_object.collides_with(mock_widget)

    assert result is True
    concrete_object.collide_widget.assert_called_once_with(mock_widget)


def test_collides_with_returns_false_when_no_collision_occurs():
    concrete_object = ConcreteObject()
    mock_widget = Mock(spec=Widget)
    concrete_object.collide_widget = Mock(return_value=False)

    result = concrete_object.collides_with(mock_widget)

    assert result is False
    concrete_object.collide_widget.assert_called_once_with(mock_widget)


def test_bounce_obj_updates_velocity_when_collision_occurs():
    concrete_object = ConcreteObject()
    concrete_object.collide_widget = Mock(return_value=True)
    concrete_object.center_x = 100
    concrete_object.center_y = 200
    concrete_object.width = 50
    concrete_object.height = 50

    obj = Mock()
    obj.center_x = 150
    obj.center_y = 250
    obj.velocity = (1, 1)

    concrete_object.bounce_obj(obj, velocity=0.5)

    assert obj.velocity[0] == pytest.approx(-1.5)
    assert obj.velocity[1] == pytest.approx(-1.5)
    assert obj.velocity == (-1.5, -1.5)
