from django.test import TestCase
from apps.citynav.navigator import (InstructionStart, InstructionGo, InstructionTurn, InstructionReach,
                                    InstructionEnglishInterpreter, RouteNavigator)


class TestInstructionEnglishInterpreter(TestCase):
    def test_interpret_start(self):
        self.assertEqual('Start at (1, 2)',
                         str(InstructionEnglishInterpreter(InstructionStart((1, 2)))))

    def test_interpret_go(self):
        self.assertEqual('Go East 5 block(s)',
                         str(InstructionEnglishInterpreter(InstructionGo('E', 5, (1, 2), (6, 2)))))
        self.assertEqual('Go 5 block(s)',
                         str(InstructionEnglishInterpreter(InstructionGo(None, 5, (1, 2), (6, 2)))))

    def test_interpret_turn(self):
        self.assertEqual('Turn left',
                         str(InstructionEnglishInterpreter(InstructionTurn('L', (1, 2)))))

    def test_interpret_reach(self):
        self.assertEqual('Go until you reach landmark "Town Hall"',
                         str(InstructionEnglishInterpreter(InstructionReach('Town Hall', (1, 2), (8, 2)))))

    def test_interpre_unknows(self):
        self.assertEqual('test', str(InstructionEnglishInterpreter('test')))


class TestRouteNavigator(TestCase):
    route_json = {
        'instructions': [
            ['START', [15, 15]],
            ['GO', ['E', 7]],
            ['TURN', 'L'],
            ['REACH', 'Town Hall'],
            ['TURN', 'R'],
            ['GO', [None, 15]],
            ['GO', ['N', 4]]
        ],
        'landmarks': [
            {'coordinate': [22, 23], 'name': 'Town Hall'}
        ]
    }
    route_readable_instructions = [
        'Start at (15, 15)',
        'Go East 7 block(s)',
        'Turn left',
        'Go until you reach landmark "Town Hall"',
        'Turn right',
        'Go 15 block(s)',
        'Go North 4 block(s)',
    ]

    def test_get_end_point(self):
        nav = RouteNavigator(self.route_json['instructions'], landmarks_json=self.route_json['landmarks'])
        self.assertEqual((37, 27), nav.get_end_point())

    def test_get_readable_instructions(self):
        nav = RouteNavigator(self.route_json['instructions'], landmarks_json=self.route_json['landmarks'])
        self.assertEqual(self.route_readable_instructions, nav.get_readable_instructions())

    def test__turn(self):
        self.assertEqual('E', RouteNavigator._turn('N', 'R'))
        self.assertEqual('W', RouteNavigator._turn('N', 'L'))

        self.assertEqual('S', RouteNavigator._turn('E', 'R'))
        self.assertEqual('N', RouteNavigator._turn('E', 'L'))

        self.assertEqual('W', RouteNavigator._turn('S', 'R'))
        self.assertEqual('E', RouteNavigator._turn('S', 'L'))

        self.assertEqual('N', RouteNavigator._turn('W', 'R'))
        self.assertEqual('S', RouteNavigator._turn('W', 'L'))

    def test__go(self):
        self.assertEqual((10, 25), RouteNavigator._go((10, 20), 'N', 5))
        self.assertEqual((15, 20), RouteNavigator._go((10, 20), 'E', 5))
        self.assertEqual((10, 15), RouteNavigator._go((10, 20), 'S', 5))
        self.assertEqual((5, 20), RouteNavigator._go((10, 20), 'W', 5))
