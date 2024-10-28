import unittest
from checkers import State, get_possible_moves, get_directions, is_within_bounds, get_chain_jumps


class TestCheckersFunctions(unittest.TestCase):
    def setUp(self):
        # Common board states used across multiple tests
        self.empty_board = [['.' for _ in range(8)] for _ in range(8)]

        # Simple board state with a single black piece that can move
        self.single_move_board = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'b', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]

        # Board with a jump opportunity for black
        self.jump_board = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'b', '.', '.', '.'],
            ['.', '.', '.', '.', '.', 'r', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]

        # King piece board
        self.king_board = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'R', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]

    def test_is_within_bounds(self):
        state = State(self.empty_board, 0, 0, 0, 0)
        self.assertTrue(is_within_bounds(state, 0, 0))
        self.assertTrue(is_within_bounds(state, 7, 7))
        self.assertFalse(is_within_bounds(state, 8, 8))
        self.assertFalse(is_within_bounds(state, -1, 0))

    def test_get_directions(self):
        black_directions = get_directions('b')
        red_directions = get_directions('r')
        self.assertEqual(black_directions, [(1, -1), (1, 1)])
        self.assertEqual(red_directions, [(-1, -1), (-1, 1)])

    def test_get_possible_moves_simple(self):
        state = State(self.single_move_board, 0, 1, 0, 0)

        # Black piece at (2, 3) should be able to move to (3, 2) and (3, 4)
        possible_moves = get_possible_moves(state, 2, 3, 'b', 'r', get_directions('b'))
        self.assertEqual(len(possible_moves), 2)
        self.assertEqual(possible_moves[0].board[3][2], 'b')
        self.assertEqual(possible_moves[1].board[3][4], 'b')

    def test_get_possible_moves_with_jump(self):
        state = State(self.jump_board, 1, 1, 0, 0)

        # Black piece at (3, 4) should be able to jump over red at (4, 5) to (5, 6)
        possible_moves = get_possible_moves(state, 3, 4, 'b', 'r', get_directions('b'))
        self.assertEqual(len(possible_moves), 1)
        self.assertEqual(possible_moves[0].board[5][6], 'b')
        self.assertEqual(possible_moves[0].board[4][5], '.')

    def test_get_possible_moves_king(self):
        state = State(self.king_board, 0, 0, 1, 0)

        # Red king piece at (1, 3) can move in all 4 diagonal directions
        possible_moves = get_possible_moves(state, 1, 3, 'R', 'b', [(-1, -1), (-1, 1), (1, -1), (1, 1)])
        self.assertEqual(len(possible_moves), 4)
        self.assertEqual(possible_moves[0].board[0][2], 'R')
        self.assertEqual(possible_moves[1].board[0][4], 'R')
        self.assertEqual(possible_moves[2].board[2][2], 'R')
        self.assertEqual(possible_moves[3].board[2][4], 'R')

    def test_get_possible_moves_no_jump_back(self):
        # Test to ensure a piece can't jump backwards (for non-king pieces)
        state = State(self.jump_board, 1, 1, 0, 0)

        # Black piece at (3, 4) should only be able to jump forward, not backward
        possible_moves = get_possible_moves(state, 5, 6, 'b', 'r', get_directions('b'))
        self.assertEqual(len(possible_moves), 2)

    def test_get_possible_moves_with_blocked_paths(self):
        blocked_board = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', 'b', '.', '.', '.', '.', '.'],
            ['.', 'r', '.', 'r', '.', '.', '.', '.'],
            ['b', '.', '.', '.', 'r', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]
        state = State(blocked_board, 3, 2, 0, 0)

        # Black piece at (3, 2) should have no moves as it is blocked by red pieces
        possible_moves = get_possible_moves(state, 3, 2, 'b', 'r', get_directions('b'))
        self.assertEqual(len(possible_moves), 0)

    def test_generate_successors(self):
        random_board = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', 'b', '.', '.', '.', '.', '.'],
            ['.', 'r', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['b', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]
        # TODO: Implement!

    def test_get_chain_jumps(self):
        # Test for a black piece that can perform multiple jumps
        chain_jump_board = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', 'b', '.', '.', '.', '.', '.', '.'],
            ['.', '.', 'r', '.', 'r', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', 'R', '.', 'r', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]
        state = State(chain_jump_board, 3, 1, 1, 0)

        # After jumping to (3, 3), check if additional chain jumps are available
        possible_moves = get_chain_jumps(state, 3, 3, 'b', 'r', get_directions('b'))
        self.assertEqual(len(possible_moves), 2)


if __name__ == '__main__':
    unittest.main()
