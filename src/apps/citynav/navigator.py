from collections import namedtuple
import copy


InstructionStart = namedtuple('InstructionStart', ('point',))
InstructionGo = namedtuple('InstructionGo', ('direction', 'blocks', 'start_point', 'end_point'))
InstructionTurn = namedtuple('InstructionTurn', ('turn', 'point',))
InstructionReach = namedtuple('InstructionReach', ('landmark_name', 'start_point', 'end_point'))


class InstructionEnglishInterpreter:
    __slots__ = ('instruction',)

    DIRECTION_NAMES = {
        'N': 'North',
        'E': 'East',
        'S': 'South',
        'W': 'West',
    }

    TURN_NAMES = {
        'L': 'left',
        'R': 'right',
    }

    def __init__(self, instruction):
        self.instruction = instruction

    def __str__(self):
        if isinstance(self.instruction, InstructionStart):
            return self._interpret_start()
        elif isinstance(self.instruction, InstructionGo):
            return self._interpret_go()
        elif isinstance(self.instruction, InstructionTurn):
            return self._interpret_turn()
        elif isinstance(self.instruction, InstructionReach):
            return self._interpret_reach()
        return str(self.instruction)

    def _interpret_start(self):
        return f'Start at ({self.instruction.point[0]}, {self.instruction.point[1]})'

    def _interpret_go(self):
        if self.instruction.direction:
            direction_name = self.DIRECTION_NAMES[self.instruction.direction]
            return f'Go {direction_name} {self.instruction.blocks} block(s)'
        else:
            return f'Go {self.instruction.blocks} block(s)'

    def _interpret_turn(self):
        turn_name = self.TURN_NAMES[self.instruction.turn]
        return f'Turn {turn_name}'

    def _interpret_reach(self):
        return f'Go until you reach landmark "{self.instruction.landmark_name}"'


class RouteNavigator:
    def __init__(self, instructions, landmarks_json=None):
        self._raw_instructions = copy.deepcopy(instructions)
        if landmarks_json is None:
            self._landmarks_coordinates = self._get_landmarks_coordinates_from_db(instructions)
        else:
            self._landmarks_coordinates = self._get_landmarks_coordinates_from_json(landmarks_json)
        self._cached_instructions = None  # will contain a list with instruction namedtuples

    @classmethod
    def _get_landmarks_coordinates_from_db(cls, instructions):
        from apps.citynav.models import Landmark

        landmarks_to_find = set()
        # get all landmarks names from instructions
        for item in instructions:
            if item[0] == 'REACH':
                landmarks_to_find.add(item[1])

        if not landmarks_to_find:
            return {}

        qs = Landmark.objects.filter(name__in=landmarks_to_find)
        return {landmark.name: (landmark.x, landmark.y) for landmark in qs}

    @classmethod
    def _get_landmarks_coordinates_from_json(cls, landmarks_json):
        return {item['name']: item['coordinate'] for item in landmarks_json}

    @classmethod
    def _go(cls, point, direction, blocks):
        """
        GO instruction.
        Returns new point coordinates.
        """
        x, y = point
        if direction == 'N':
            y += blocks
        elif direction == 'S':
            y -= blocks
        elif direction == 'E':
            x += blocks
        elif direction == 'W':
            x -= blocks
        else:
            raise ValueError('invalid instructions: invalid direction')
        return x, y

    @classmethod
    def _turn(cls, direction, turn):
        """
        TURN instruction.
        Returns new direction.
        """
        directions = ('N', 'E', 'S', 'W')
        i = directions.index(direction)
        if turn == 'L':
            i -= 1
        elif turn == 'R':
            i += 1
        else:
            raise ValueError('invalid instructions: invalid turn')
        if i < 0:
            i += 4
        elif i > 3:
            i -= 4
        return directions[i]

    def _reach(self, point, direction, landmark_name):
        """
        REACH instruction.
        Returns new point coordinates.
        """
        if landmark_name not in self._landmarks_coordinates:
            raise ValueError('invalid instructions: unknown landmark')

        landmark_x, landmark_y = self._landmarks_coordinates[landmark_name]
        x, y = point
        if direction in {'W', 'E'}:
            if (y != landmark_y
                    or (direction == 'W' and x < landmark_x)
                    or (direction == 'E' and x > landmark_x)):
                raise ValueError('invalid instructions: invalid landmark coordinate')
            x = landmark_x
        elif direction in {'N', 'S'}:
            if (x != landmark_x
                    or (direction == 'N' and y > landmark_y)
                    or (direction == 'S' and y < landmark_y)):
                raise ValueError('invalid instructions: invalid landmark coordinate')
            y = landmark_y

        return x, y

    def get_instructions(self):
        """
        Returns a list with instruction namedtuples
        """
        if self._cached_instructions is None:
            if self._raw_instructions[0][0] != 'START':  # the first instruction must be START
                raise ValueError('invalid instructions: the first item is not START type')
            instructions = []
            point = self._raw_instructions[0][1]
            direction = None
            instructions.append(InstructionStart(point))
            for item in self._raw_instructions[1:]:
                if item[0] == 'GO':
                    item_direction, item_blocks = item[1]
                    if item_direction:
                        direction = item_direction  # get direction from instruction
                    elif not item_direction and not direction:
                        # no information about direction
                        raise ValueError('invalid instructions: no enough direction info')
                    prev_point = point
                    point = self._go(point, direction, item_blocks)
                    instructions.append(InstructionGo(item_direction, item_blocks, prev_point, point))
                elif item[0] == 'TURN':
                    if not direction:
                        # no information about direction
                        raise ValueError('invalid instructions: no enough direction info')
                    direction = self._turn(direction, item[1])
                    instructions.append(InstructionTurn(item[1], point))
                elif item[0] == 'REACH':
                    if not direction:
                        # no information about direction
                        raise ValueError('invalid instructions: no enough direction info')
                    prev_point = point
                    point = self._reach(point, direction, item[1])
                    instructions.append(InstructionReach(item[1], prev_point, point))
                else:
                    raise ValueError('invalid instruction: invalid instruction type')
            self._cached_instructions = instructions
        return self._cached_instructions

    def get_start_point(self):
        return self.get_instructions()[0].point

    def get_end_point(self):
        last_instruction = self.get_instructions()[-1]
        val = getattr(last_instruction, 'end_point', None)
        if val is None:
            val = getattr(last_instruction, 'point', None)
        return val

    def get_readable_instructions(self):
        """
        Returns a list with readable instructions.
        """
        return [str(InstructionEnglishInterpreter(item)) for item in self.get_instructions()]
