from dataclasses import dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Info message about training session."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Training type: {self.training_type}; '
                f'Duration: {self.duration:.3f} h; '
                f'Dastance: {self.distance:.3f} km; '
                f'Avg speed: {self.speed:.3f} kmph; '
                f'Cal spended: {self.calories:.3f}.')


class Training:
    """Base training type."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = None

    def get_distance(self) -> float:
        """Get distance (km)."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average speed (kmph)."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get spended calories."""
        raise NotImplementedError('Функция get_spent_calories '
                                  'не переопределена в классе '
                                  f'{type(self).__name__}')

    def show_training_info(self) -> InfoMessage:
        """Get info message about training session."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training type: running."""

    FACTOR: int = 18
    SUBSTRAHEND: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.training_type = type(self).__name__

    def get_spent_calories(self) -> float:
        """Get spended calories."""

        return ((self.FACTOR
                * self.get_mean_speed()
                - self.SUBSTRAHEND)
                * self.weight
                / self.M_IN_KM
                * self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Training type: sports walking."""

    WEIGHT_FACTOR: float = 0.035
    SPEED_FACTOR: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.training_type = type(self).__name__

    def get_spent_calories(self) -> float:
        """Get spended calories."""
        return ((self.WEIGHT_FACTOR
                * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.SPEED_FACTOR
                * self.weight) * self.duration * self.H_IN_MIN)


class Swimming(Training):
    """Training type: swimming."""

    LEN_STEP: float = 1.38
    ADD: float = 1.1
    FACTOR: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.training_type = type(self).__name__

    def get_mean_speed(self) -> float:
        """Get average speed."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Get spended calories."""
        return ((self.get_mean_speed()
                + self.ADD)
                * self.FACTOR
                * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Read sensors data."""

    workout_codes: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}

    if workout_type in workout_codes:
        return workout_codes[workout_type](*data)
    raise ValueError('Unknown training type.')


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
