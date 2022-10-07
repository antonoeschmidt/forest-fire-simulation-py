from processes.cell import Cell, CellState


class Forest(object):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.map = [
            Cell(0, 0, CellState.MED_VEG), Cell(1, 0, CellState.MED_VEG), Cell(2, 0, CellState.MED_VEG), Cell(3, 0, CellState.MED_VEG), Cell(4, 0, CellState.MED_VEG), Cell(5, 0, CellState.MED_VEG),
            Cell(0, 1, CellState.MED_VEG), Cell(1, 1, CellState.MED_VEG), Cell(2, 1, CellState.MED_VEG), Cell(3, 1, CellState.MED_VEG), Cell(4, 1, CellState.MED_VEG), Cell(5, 1, CellState.MED_VEG),
            Cell(0, 2, CellState.MED_VEG), Cell(1, 2, CellState.MED_VEG), Cell(2, 2, CellState.MED_VEG), Cell(3, 2, CellState.MED_VEG), Cell(4, 2, CellState.MED_VEG), Cell(5, 2, CellState.MED_VEG),
            Cell(0, 3, CellState.MED_VEG), Cell(1, 3, CellState.MED_VEG), Cell(2, 3, CellState.MED_VEG), Cell(3, 3, CellState.MED_VEG), Cell(4, 3, CellState.MED_VEG), Cell(5, 3, CellState.MED_VEG),
            Cell(0, 4, CellState.MED_VEG), Cell(1, 4, CellState.MED_VEG), Cell(2, 4, CellState.MED_VEG), Cell(3, 4, CellState.MED_VEG), Cell(4, 4, CellState.MED_VEG), Cell(5, 4, CellState.MED_VEG),
            Cell(0, 5, CellState.MED_VEG), Cell(1, 5, CellState.MED_VEG), Cell(2, 5, CellState.MED_VEG), Cell(3, 5, CellState.MED_VEG), Cell(4, 5, CellState.MED_VEG), Cell(5, 5, CellState.MED_VEG),
        ]

    def get_cell(self, x, y):
        return self.map[x * self.width + y]
