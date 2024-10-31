import random
import string
import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # Define a brighter color (Yellow)
ORANGE = (255, 165, 0)  # Define a brighter color (Orange)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end_of_word
    
    def get_all_words(self):
        words = []
        self._get_all_words_recursive(self.root, "", words)
        return words

    def _get_all_words_recursive(self, node, current_word, words):
        if node.is_end_of_word:
            words.append(current_word)

        for char, child_node in node.children.items():
            self._get_all_words_recursive(child_node, current_word + char, words)

class WordSearchGraph:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.graph = {}

    def add_edge(self, node1, node2):
        if node1 in self.graph:
            self.graph[node1].append(node2)
        else:
            self.graph[node1] = [node2]

    def build_graph(self):
        for i in range(self.rows):
            for j in range(self.cols):
                current_node = (i, j)

                # Connect with horizontal and vertical neighbors
                for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                    if 0 <= ni < self.rows and 0 <= nj < self.cols:
                        neighbor_node = (ni, nj)
                        self.add_edge(current_node, neighbor_node)

                # Connect with diagonal neighbors
                for ni, nj in [(i + 1, j + 1), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1)]:
                    if 0 <= ni < self.rows and 0 <= nj < self.cols:
                        neighbor_node = (ni, nj)
                        self.add_edge(current_node, neighbor_node)

    def fill_empty_spaces(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == ' ':
                    self.grid[i][j] = random.choice(string.ascii_uppercase)

    def word_search_csp(self, words, index=0):
        if index == len(words):
            return True  # All words placed successfully

        word = words[index]
        nodes = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        random.shuffle(nodes)  # Randomize node selection
        for node in nodes:
            for direction in ['horizontal', 'vertical', 'diagonal']:
                for orientation in [1, -1]:
                    if self.is_valid_assignment(word, node, direction, orientation):
                        self.assign_word(word, node, direction, orientation)
                        if self.word_search_csp(words, index + 1):
                            return True
                        self.unassign_word(word, node, direction, orientation)

        return False

    def is_valid_assignment(self, word, node, direction, orientation):
        if direction == 'horizontal':
            return all(0 <= node[1] + i * orientation < self.cols and
                       (self.grid[node[0]][node[1] + i * orientation] == ' ' or
                        self.grid[node[0]][node[1] + i * orientation] == word[i]) for i in range(len(word)))
        elif direction == 'vertical':
            return all(0 <= node[0] + i * orientation < self.rows and
                       (self.grid[node[0] + i * orientation][node[1]] == ' ' or
                        self.grid[node[0] + i * orientation][node[1]] == word[i]) for i in range(len(word)))
        elif direction == 'diagonal':
            return all(0 <= node[0] + i * orientation < self.rows and
                       0 <= node[1] + i * orientation < self.cols and
                       (self.grid[node[0] + i * orientation][node[1] + i * orientation] == ' ' or
                        self.grid[node[0] + i * orientation][node[1] + i * orientation] == word[i]) for i in range(len(word)))
        return False
    def assign_word(self, word, node, direction, orientation):
        if direction == 'horizontal':
            a = random.choice([0, 1])
            for i in range(len(word)):
                if a == 0:
                    self.grid[node[0]][node[1] + i * orientation] = word[-i - 1]
                if a == 1:
                    self.grid[node[0]][node[1] + i * orientation] = word[i]
        elif direction == 'vertical':
            a = random.choice([0, 1])
            for i in range(len(word)):
                if a == 0:
                    self.grid[node[0] + i * orientation][node[1]] = word[-i - 1]
                if a == 1:
                    self.grid[node[0] + i * orientation][node[1]] = word[i]
        elif direction == 'diagonal':
            a = random.choice([0, 1])
            for i in range(len(word)):
                if a == 0:
                    self.grid[node[0] + i * orientation][node[1] + i * orientation] = word[-i - 1]
                if a == 1:
                    self.grid[node[0] + i * orientation][node[1] + i * orientation] = word[i]

    def unassign_word(self, word, node, direction, orientation):
        if direction == 'horizontal' or direction == 'vertical':
            for i in range(len(word)):
                row = node[0]
                col = node[1] + i * orientation
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    self.grid[row][col] = ' '
        elif direction == 'diagonal':
            for i in range(len(word)):
                row = node[0] + i * orientation
                col = node[1] + i * orientation
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    self.grid[row][col] = ' '

class WordSearchCSP:
    def __init__(self, grid_size, trie):
        self.grid_size = grid_size
        self.word_search_graph = WordSearchGraph([[' ' for _ in range(grid_size)] for _ in range(grid_size)])  # Adjusted grid size here
        self.trie = trie
        self.words = trie.get_all_words()


    def solve(self):
        return self.word_search_graph.word_search_csp(self.words)

    def display_grid(self):
        for row in self.word_search_graph.grid:
            print(' '.join(row))



def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((890, 670))  # Increased width and height to accommodate score, time, and border
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    # Define multiple sets of words
    word_lists = [
        [("ELEPHANT", "A very large plant-eating mammal with a trunk"),
         ("MONKEY", "A small to medium-sized primate"),
         ("GIRAFFE", "A tall African mammal with a long neck and legs"),
         ("ZEBRA", "An African wild horse with black-and-white stripes"),
         ("RHINOCEROS", "A large, heavily built herbivorous mammal with one or two upright horns on the snout")],
        [("MOUNTAIN", "A large natural elevation of the earth's surface"),
         ("VALLEY", "A low area of land between hills or mountains"),
         ("FOREST", "A large area covered chiefly with trees and undergrowth"),
         ("RIVER", "A large natural stream of water flowing in a channel"),
         ("LAKE", "A large body of water surrounded by land")],
        [("COMPUTER", "An electronic device for storing and processing data"),
         ("INTERNET", "A global computer network providing a variety of information and communication facilities"),
         ("SOFTWARE", "The programs and other operating information used by a computer"),
         ("HARDWARE", "The physical components of a computer system"),
         ("PROGRAMMING", "The process of writing computer programs")],
        [("OCEAN", "A very large expanse of sea"),
         ("SEA", "The expanse of salt water that covers most of the earth's surface"),
         ("BEACH", "A pebbly or sandy shore, especially by the ocean"),
         ("WAVE", "A long body of water curling into an arched form and breaking on the shore"),
         ("TIDE", "The alternate rising and falling of the sea")],
        [("ADVENTURE", "An unusual and exciting experience or activity"),
         ("EXPLORATION", "The action of traveling in or through an unfamiliar area in order to learn about it"),
         ("DISCOVERY", "The act of finding or learning something for the first time"),
         ("JOURNEY", "An act of traveling from one place to another"),
         ("EXPEDITION", "A journey undertaken by a group of people with a particular purpose")],
        [("LITERATURE", "Written works, especially those considered of superior or lasting artistic merit"),
         ("POETRY", "Literary work in which special intensity is given to the expression of feelings and ideas by the use of distinctive style and rhythm"),
         ("FICTION", "Literature in the form of prose, especially novels, that describes imaginary events and people"),
         ("NONFICTION", "Prose writing that is based on facts, real events, and real people, such as biography or history"),
         ("DRAMA", "A play for theater, radio, or television")]]

    # Randomly choose one word list
    chosen_word_list = random.choice(word_lists)
    print("Chosen Word List:")
    for word, definition in chosen_word_list:
        print(f"Word: {word}")

    trie_example = Trie()
    for word, _ in chosen_word_list:
        trie_example.insert(word)

    grid_size = 14  # Set grid size to 14x14
    word_search_csp_example = WordSearchCSP(grid_size, trie_example)

    if word_search_csp_example.solve():
        word_search_csp_example.word_search_graph.fill_empty_spaces()

    found_words = set()
    score = 0
    start_time = pygame.time.get_ticks()  # Get the current time in milliseconds

    
    last_clicked_cell = None
    clicked_word = ""

    while True:
        draw_game_ui(word_search_csp_example.word_search_graph.grid, score, start_time, found_words,chosen_word_list)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_row = mouse_pos[1] // (600 // grid_size)
                clicked_col = mouse_pos[0] // (600 // grid_size)
                if last_clicked_cell is None or is_adjacent((clicked_row, clicked_col), last_clicked_cell):
                    selected_letter = word_search_csp_example.word_search_graph.grid[clicked_row][clicked_col]
                    clicked_word += selected_letter
                    last_clicked_cell = (clicked_row, clicked_col)
                else:
                    last_clicked_cell = None
                    clicked_word = ""

                if clicked_word in [word for word, _ in chosen_word_list]:
                    if clicked_word not in found_words:
                        print("Word found:", clicked_word)
                        found_words.add(clicked_word)
                        highlight_word(clicked_word, word_search_csp_example.word_search_graph.grid)
                        score += 10  # Increase score by 10
                        clicked_word = ""
                        last_clicked_cell = None

                blink_cell(clicked_row, clicked_col, grid_size)

        if len(found_words) == len(chosen_word_list):
            display_gameover_win(score, start_time)

    


def is_adjacent(cell1, cell2):
    row1, col1 = cell1
    row2, col2 = cell2
    return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1 and (row1 != row2 or col1 != col2)

def draw_game_ui(grid, score, start_time, found_words, chosen_word_list):
    SCREEN.fill(BLACK)

    # Draw the game grid
    draw_grid(grid)

    # Draw the border around the game grid
    pygame.draw.rect(SCREEN, WHITE, (0, 0, 600, 600), 2)

    # Display found words
    display_found_words(grid, found_words)

    # Display chosen words in the score and time area
    display_chosen_words_in_score_area(chosen_word_list,found_words)

    # Display score and time below the grid
    display_score(score)
    display_time(start_time)
    
    
def display_gameover_win(score, start_time):
    SCREEN.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text = font.render("Congratulations! You found all words!", True, GREEN)
    text_rect = text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
    SCREEN.blit(text, text_rect)

    # Display final score and time
    display_score(score)
    display_time(start_time)

    pygame.display.update()
    pygame.time.delay(10000)  # Wait for 3 seconds before closing the window
    pygame.quit()
    sys.exit()


# def display_chosen_words_in_score_area(chosen_word_list):
#     font = pygame.font.Font(None, 24)
#     text_x = 620  # Start x position for displaying words
#     text_y = 50   # Start y position for displaying words
#     max_width = 200  # Maximum width for text in the score area

#     for word, definition in chosen_word_list:
#         # Render the text
#         text = f"{word}: {definition}"

#         # Wrap the text to fit within the maximum width
#         wrapped_text = wrap_text(text, max_width)

#         # Display the wrapped text
#         for line in wrapped_text:
#             text_rect = line.get_rect(topleft=(text_x, text_y))
#             SCREEN.blit(line, text_rect)
#             text_y += 20  # Increase y position for the next line


def display_chosen_words_in_score_area(chosen_word_list, found_words):
    font = pygame.font.Font(None, 24)
    text_x = 620  # Start x position for displaying words
    text_y = 50   # Start y position for displaying words
    max_width = 200  # Maximum width for text in the score area

    # Filter out the words that have already been found
    remaining_words = [(word, definition) for word, definition in chosen_word_list if word not in found_words]

    for word, definition in remaining_words:
        # Render the text
        text = f"{word}: {definition}"

        # Wrap the text to fit within the maximum width
        wrapped_text = wrap_text(text, max_width)

        # Display the wrapped text
        for line in wrapped_text:
            text_rect = line.get_rect(topleft=(text_x, text_y))
            SCREEN.blit(line, text_rect)
            text_y += 20  # Increase y position for the next line



def wrap_text(text_surface, max_width):
    words = text_surface.split(' ')
    wrapped_lines = []
    current_line = ''
    font = pygame.font.Font(None, 24)

    for word in words:
        test_line = current_line + word + ' '
        test_width, _ = font.size(test_line)
        if test_width <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(font.render(current_line, True, WHITE))
            current_line = word + ' '

    wrapped_lines.append(font.render(current_line, True, WHITE))
    return wrapped_lines


def display_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    text_rect = text.get_rect(bottomleft=(620, 600))
    SCREEN.blit(text, text_rect)

def display_time(start_time):
    elapsed_time = pygame.time.get_ticks() - start_time
    seconds = elapsed_time // 1000
    font = pygame.font.Font(None, 36)
    text = font.render(f"Time: {seconds} sec", True, WHITE)
    text_rect = text.get_rect(bottomleft=(620, 640))
    SCREEN.blit(text, text_rect)


def highlight_word(word, grid):
    rows = len(grid)
    cols = len(grid[0])
    directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]

    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                found_word = ""
                for length in range(len(word)):
                    end_x = i + length * dx
                    end_y = j + length * dy
                    if 0 <= end_x < rows and 0 <= end_y < cols:
                        found_word += grid[end_x][end_y]
                        if found_word == word:
                            for k in range(len(word)):
                                grid[end_x - k * dx][end_y - k * dy] = grid[end_x - k * dx][end_y - k * dy].lower()
                            return
                    else:
                        break
    return





def find_selected_word(trie, grid, start, chosen_word_list):
    rows = len(grid)
    cols = len(grid[0])
    directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]
    
    for dx, dy in directions:
        for i in range(-rows, rows):
            for j in range(-cols, cols):
                word = ""
                x, y = start
                while 0 <= x < rows and 0 <= y < cols:
                    word += grid[x][y]
                    if trie.search(word):
                        for w, definition in chosen_word_list:
                            if w == word:
                                return word, definition
                    x += dx
                    y += dy
    return None, None

def display_found_words(grid, found_words):
    rows = len(grid)
    cols = len(grid[0])
    blockSize = 600 // cols

    for i in range(rows):
        for j in range(cols):
            cell_center = (j * blockSize + blockSize // 2, i * blockSize + blockSize // 2)
            cell_word = grid[i][j]
            if cell_word.lower() in found_words:
                text = pygame.font.Font(None, 36).render(cell_word, True, GREEN)
                text_rect = text.get_rect(center=cell_center)
                SCREEN.blit(text, text_rect)

def blink_cell(row, col, grid_size):
    blockSize = 600 // grid_size
    x = col * blockSize
    y = row * blockSize
    rect = pygame.Rect(x, y, blockSize, blockSize)
    pygame.draw.rect(SCREEN, RED, rect, 1)
    pygame.display.update()
    pygame.time.delay(100)
    pygame.draw.rect(SCREEN, BLACK, rect, 1)
    pygame.display.update()

# def blink_cell(row, col, grid_size):
#     blockSize = 600 // grid_size
#     x = col * blockSize
#     y = row * blockSize
#     rect = pygame.Rect(x, y, blockSize, blockSize)
#     pygame.draw.rect(SCREEN, YELLOW, rect, 1)  # Change RED to YELLOW
#     pygame.display.update()
#     pygame.time.delay(100)
#     pygame.draw.rect(SCREEN, BLACK, rect, 1)
#     pygame.display.update()

# def blink_cell(row, col, grid_size):
#     blockSize = 600 // grid_size
#     x = col * blockSize
#     y = row * blockSize
#     rect = pygame.Rect(x, y, blockSize, blockSize)
#     pygame.draw.rect(SCREEN, ORANGE, rect, 1)  # Change YELLOW to ORANGE
#     pygame.display.update()
#     pygame.time.delay(100)
#     pygame.draw.rect(SCREEN, BLACK, rect, 1)
#     pygame.display.update()

def draw_grid(grid):
    if not grid:
        return

    rows = len(grid)
    cols = len(grid[0])

    blockSize = 600 // cols
    for i in range(rows):
        for j in range(cols):
            x = j * blockSize
            y = i * blockSize
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, RED, rect, 1)
            text = pygame.font.Font(None, 36).render(grid[i][j], True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            SCREEN.blit(text, text_rect)

            if grid[i][j].islower():
                pygame.draw.rect(SCREEN, RED, rect)
            else:
                pygame.draw.rect(SCREEN, WHITE, rect, 1)




if __name__ == "__main__":
    main()