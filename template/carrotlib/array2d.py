from typing import Callable, Any, Generic, TypeVar

T = TypeVar('T')

class array2d_row(Generic[T]):
    def __init__(self, a: 'array2d', row: int):
        self.a = a
        self.row = row

    def __getitem__(self, col: int) -> T:
        return self.a[col, self.row]
    
    def __setitem__(self, col: int, value: T):
        self.a[col, self.row] = value

    def __len__(self):
        return self.a.n_cols
    
    def copy(self) -> list[T]:
        return [self.a[col, self.row] for col in range(self.a.n_cols)]
    
    def __repr__(self):
        return f'array2d_row({self.row}, {self.copy()})'


class array2d_col(Generic[T]):
    def __init__(self, a: 'array2d', col: int):
        self.a = a
        self.col = col

    def __getitem__(self, row: int) -> T:
        return self.a[self.col, row]
    
    def __setitem__(self, row: int, value: T):
        self.a[self.col, row] = value

    def __len__(self):
        return self.a.n_rows
    
    def copy(self) -> list[T]:
        return [self.a[self.col, row] for row in range(self.a.n_rows)]
    
    def __repr__(self):
        return f'array2d_col({self.col}, {self.copy()})'


class array2d(Generic[T]):
    data: list[T]

    def __init__(self, n_cols: int, n_rows: int, default=None):
        self.n_cols = n_cols
        self.n_rows = n_rows
        if callable(default):
            self.data = [default() for _ in range(n_cols * n_rows)]
        else:
            self.data = [default] * n_cols * n_rows
    
    @property
    def width(self) -> int:
        return self.n_cols
    
    @property
    def height(self) -> int:
        return self.n_rows

    def row(self, index: int) -> array2d_row[T]:
        if not 0 <= index < self.n_rows:
            raise IndexError(f'row index {index} not in [0, {self.n_rows})')
        return array2d_row(self, index)
    
    def col(self, index: int) -> array2d_col[T]:
        if not 0 <= index < self.n_cols:
            raise IndexError(f'col index {index} not in [0, {self.n_cols})')
        return array2d_col(self, index)

    def is_valid(self, col: int, row: int) -> bool:
        return 0 <= col < self.n_cols and 0 <= row < self.n_rows

    def get(self, col: int, row: int, default=None):
        if not self.is_valid(col, row):
            return default
        return self.data[row * self.n_cols + col]

    def __getitem__(self, index: tuple[int, int]):
        col, row = index
        if not self.is_valid(col, row):
            raise IndexError(f'({col}, {row}) is not a valid index for array2d(n_cols={self.n_cols}, n_rows={self.n_rows})')
        return self.data[row * self.n_cols + col]

    def __setitem__(self, index: tuple[int, int], value: T):
        col, row = index
        if not self.is_valid(col, row):
            raise IndexError(f'({col}, {row}) is not a valid index for array2d(n_cols={self.n_cols}, n_rows={self.n_rows})')
        self.data[row * self.n_cols + col] = value

    def __iter__(self):
        for i in range(self.n_rows):
            yield self.row(i)
    
    def __len__(self):
        return self.n_rows

    def __repr__(self):
        buffer = ['array2d(']
        for i in range(self.n_rows):
            buffer.append('    ' + repr(self.row(i)))
        buffer.append(')')
        return '\n'.join(buffer)

    def map(self, f: Callable[[T], Any]) -> 'array2d':
        new_a: array2d = array2d(self.n_cols, self.n_rows)
        for i in range(self.n_cols * self.n_rows):
            new_a.data[i] = f(self.data[i])
        return new_a
    
    def copy(self) -> 'array2d[T]':
        new_a: array2d[T] = array2d(self.n_cols, self.n_rows)
        new_a.data = self.data.copy()
        return new_a
    
    def transpose(self) -> 'array2d[T]':
        new_a: array2d[T] = array2d(self.n_rows, self.n_cols)
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                new_a[row, col] = self[col, row]
        return new_a

    def fill_(self, value: T) -> None:
        for i in range(self.n_cols * self.n_rows):
            self.data[i] = value

    def apply_(self, f: Callable[[T], T]) -> None:
        for i in range(self.n_cols * self.n_rows):
            self.data[i] = f(self.data[i])

    def copy_(self, other: 'array2d[T]') -> None:
        self.n_cols = other.n_cols
        self.n_rows = other.n_rows
        self.data = other.data.copy()

    def draw(self, width=1):
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                c = str(self[col, row])
                if len(c) < width:
                    c = ' ' * (width - len(c)) + c
                print(c, end='')
            print()
