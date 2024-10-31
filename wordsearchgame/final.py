# import pygame
import sys
import random
import string
import time
import requests
import pygame.time


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHT_GRAY = (240, 240, 240)

# Define SCREEN globally
SCREEN = None

class TrieNode:
    def __init__(self):
        self.children = {}
        self.definition = None
        self.is_end_of_word = False
        
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, definition=None):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.definition = definition

    def search(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return False, None  # Modified to return a tuple
            current = current.children[char]
        return current.is_end_of_word, current.definition

    
    def get_all_words(self):
        words = []
        self._get_all_words_recursive(self.root, "", words)
        return words

    def _get_all_words_recursive(self, node, current_word, words):
        if node.is_end_of_word:
            words.append((current_word, node.definition))

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
                if self.grid[i][j] ==' ':
                    self.grid[i][j] = random.choice(string.ascii_uppercase)

    def word_search_csp(self, words, index=0):
        if index == len(words):
            return True  # All words placed successfully

        word, _ = words[index]  # Extract word from tuple
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
        self.word_search_graph = WordSearchGraph([[' ' for _ in range(grid_size)] for _ in range(grid_size)])
        self.trie = trie
        self.words = trie.get_all_words()

    def solve(self):
        return self.word_search_graph.word_search_csp(self.words)

    def display_grid(self):
        for row in self.word_search_graph.grid:
            print(' '.join(row))

def draw_grid(grid, selected_cells, found_word_cells, score, time_left):
    # Function to draw the grid on the screen
    if not grid:
        return  # Return if grid is empty

    global SCREEN  # Access SCREEN globally

    rows = len(grid)
    cols = len(grid[0])

    blockSize = 400 // cols  # Calculate size of each block
    for x in range(0, 400, blockSize):
        for y in range(0, 400, blockSize):
            if y // blockSize < rows and x // blockSize < cols:  
                rect = pygame.Rect(x, y, blockSize, blockSize)
                if (y // blockSize, x // blockSize) in selected_cells:
                    pygame.draw.rect(SCREEN, BLUE, rect)  # Highlight selected cells in blue
                elif (y // blockSize, x // blockSize) in found_word_cells:
                    pygame.draw.rect(SCREEN, GREEN, rect)  # Highlight found word cells in green
                else:
                    pygame.draw.rect(SCREEN, WHITE, rect, 1)  # Draw grid lines
                text = pygame.font.Font(None, 36).render(grid[y // blockSize][x // blockSize], True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                SCREEN.blit(text, text_rect)

    # Display score and time left
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_text, (450, 50))
    time_text = pygame.font.Font(None, 36).render(f"Time left: {time_left}s", True, BLACK)
    SCREEN.blit(time_text, (450, 100))

def send_word_to_flask(word, definition):
    try:
        response = requests.post('http://127.0.0.1:5000/word_found', json={'word': word, 'definition': definition})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending word to Flask server: {e}")


def find_selected_word(grid, start_pos, end_pos):
    if not start_pos or not end_pos:
        return ""
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if start_row == end_row:
        # Horizontal selection
        if start_col < end_col:
            return ''.join(grid[start_row][start_col:end_col + 1])
        else:
            return ''.join(grid[start_row][end_col:start_col + 1][::-1])
    elif start_col == end_col:
        # Vertical selection
        if start_row < end_row:
            return ''.join(grid[row][start_col] for row in range(start_row, end_row + 1))
        else:
            return ''.join(grid[row][start_col] for row in range(end_row, start_row + 1)[::-1])
    elif abs(start_row - end_row) == abs(start_col - end_col):
        # Diagonal selection
        if start_row < end_row:
            if start_col < end_col:
                return ''.join(grid[start_row + i][start_col + i] for i in range(end_row - start_row + 1))
            else:
                return ''.join(grid[start_row + i][start_col - i] for i in range(end_row - start_row + 1))
        else:
            if start_col < end_col:
                return ''.join(grid[start_row - i][start_col + i] for i in range(start_row - end_row + 1))
            else:
                return ''.join(grid[start_row - i][start_col - i] for i in range(start_row - end_row + 1))

    return ""

def handle_user_input():
    input_box = pygame.Rect(450, 150, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        SCREEN.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        SCREEN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(SCREEN, color, input_box, 2)

        pygame.display.flip()

    try:
        grid_size = int(text)
        if grid_size < 5:
            raise ValueError
    except ValueError:
        grid_size = 5

    return grid_size

def display_selected_words(selected_words):
    text_y = 200  # Starting y-coordinate for displaying selected words
    for word, definition in selected_words:
        word_text = pygame.font.Font(None, 24).render(f"*{definition}", True, BLACK)
        SCREEN.blit(word_text, (450, text_y))
        text_y += 30  # Increment y-coordinate for the next word
import pygame.time

# def display_gameover_win(score, start_time):
#     global SCREEN
    
#     # Clear the screen
#     SCREEN.fill(LIGHT_GRAY)
    
#     # Calculate the total time taken to complete the game
#     total_time_taken = int(time.time() - start_time)
    
#     # Display the game-over/win message
#     if score == 0:
#         message = "Game Over! You didn't find any words."
#     else:
#         message = f"Congratulations! You found all words with a score of {score}."
#     message += f"\nTotal Time Taken: {total_time_taken} seconds."
    
#     font = pygame.font.Font(None, 36)
#     text = font.render(message, True, BLACK)
#     text_rect = text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
#     SCREEN.blit(text, text_rect)
    
#     # Update the display
#     pygame.display.flip()
    
#     # Introduce a delay before exiting
#     pygame.time.wait(20000)  # Wait for 5000 milliseconds (5 seconds)

def display_gameover_win(score, start_time, total_characters):
    global SCREEN
    
    # Clear the screen
    SCREEN.fill(LIGHT_GRAY)
    
    # Calculate the total time taken to complete the game
    total_time_taken = int(time.time() - start_time)
    
    # Display the game-over/win message
    if score == 0:
        message = "Game Over! You didn't find any words."
    elif score == total_characters:
        message = f"Congratulations! You found all words with a score of {score}."
    else:
        message = "Game Over! Still words are present."
    
    message += f"\nTotal Time Taken: {total_time_taken} seconds."
    
    font = pygame.font.Font(None, 36)
    text_lines = message.split('\n')
    y_offset = SCREEN.get_height() // 2 - 50
    
    for line in text_lines:
        text = font.render(line, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN.get_width() // 2, y_offset))
        SCREEN.blit(text, text_rect)
        y_offset += 40
    
    # Update the display
    pygame.display.flip()
    
    # Introduce a delay before exiting
    pygame.time.wait(20000)  # Wait for 20000 milliseconds (20 seconds)


def main():
    pygame.init()
    global SCREEN
    SCREEN = pygame.display.set_mode((1200,500))
    pygame.display.set_caption('Word Search')

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
    selected_word_list = random.choice(word_lists)
    
    trie = Trie()
    for word, definition in selected_word_list:
        trie.insert(word, definition)
        print(f"Trie Tree for '{word}':")
        print_trie(trie.root, "")
    
        print(f"Path from root to leaf for '{word}':")
        print_trie_path(trie.root, word)
    for word, definition in selected_word_list:  
        print(f"Search path for '{word}':")
        search_path = search_word_in_trie(trie.root, word)
        if search_path:
            for char, definition in search_path:
                print(f"{char} (Definition: {definition})")
        else:
            print(f"Word '{word}' not found in trie.")

    grid_size = handle_user_input()
    word_search_csp = WordSearchCSP(grid_size, trie)
    print(word_search_csp.display_grid())
    word_search_csp.solve()
    word_search_csp.word_search_graph.fill_empty_spaces()
    
    
    start_pos = None
    end_pos = None
    selected_cells = set()
    found_word_cells = set()
    score = 0
    time_limit = 30  # 2 minutes
    start_time = time.time()

    # Calculate the total number of characters of the words to be found
    total_characters = sum(len(word) for word, _ in selected_word_list)

    while True:
        SCREEN.fill(LIGHT_GRAY)
        time_left = int(time_limit - (time.time() - start_time))
        if time_left <= 0:
            print("Time's up!")
            display_gameover_win(score, start_time, total_characters)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    start_pos = (event.pos[1] // (400 // grid_size), event.pos[0] // (400 // grid_size))
                    selected_cells = {start_pos}
            elif event.type == pygame.MOUSEMOTION:
                if start_pos:
                    end_pos = (event.pos[1] // (400 // grid_size), event.pos[0] // (400 // grid_size))
                    selected_cells = get_cells_between(start_pos, end_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    end_pos = (event.pos[1] // (400 // grid_size), event.pos[0] // (400 // grid_size))
                    selected_word = find_selected_word(word_search_csp.word_search_graph.grid, start_pos, end_pos)
                    found, _ = trie.search(selected_word)
                    if found:
                        found_word_cells.update(selected_cells)
                        score += len(selected_word)
                        send_word_to_flask(selected_word, _)  # Send the found word and definition to Flask

                    start_pos = None
                    end_pos = None
                    selected_cells = set()

        draw_grid(word_search_csp.word_search_graph.grid, selected_cells, found_word_cells, score, time_left)
        display_selected_words(selected_word_list)  # Display selected words
        pygame.display.flip()

        if len(found_word_cells) == total_characters:
            display_gameover_win(score, start_time, total_characters)  # Display the game-over/win screen
            break  # Exit the game loop if all words have been found


    # start_pos = None
    # end_pos = None
    # selected_cells = set()
    # found_word_cells = set()
    # score = 0
    # time_limit = 120  # 2 minutes
    # start_time = time.time()

    # while True:
    #     SCREEN.fill(LIGHT_GRAY)
    #     time_left = int(time_limit - (time.time() - start_time))
    #     if time_left <= 0:
    #         print("Time's up!")
    #         pygame.quit()
    #         sys.exit()

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             if event.button == 1:  # Left mouse button
    #                 start_pos = (event.pos[1] // (400 // grid_size), event.pos[0] // (400 // grid_size))
    #                 selected_cells = {start_pos}
    #         elif event.type == pygame.MOUSEMOTION:
    #             if start_pos:
    #                 end_pos = (event.pos[1] // (400 // grid_size), event.pos[0] // (400 // grid_size))
    #                 selected_cells = get_cells_between(start_pos, end_pos)
    #         elif event.type == pygame.MOUSEBUTTONUP:
    #             if event.button == 1 and start_pos:
    #                 end_pos = (event.pos[1] // (400 // grid_size), event.pos[0] // (400 // grid_size))
    #                 selected_word = find_selected_word(word_search_csp.word_search_graph.grid, start_pos, end_pos)
    #                 found, _ = trie.search(selected_word)
    #                 if found:
    #                     found_word_cells.update(selected_cells)
    #                     score += len(selected_word)
    #                     #send_word_to_flask(selected_word, _)  # Send the found word and definition to Flask

    #                 start_pos = None
    #                 end_pos = None
    #                 selected_cells = set()

    #     draw_grid(word_search_csp.word_search_graph.grid, selected_cells, found_word_cells, score, time_left)
    #     display_selected_words(selected_word_list)  # Display selected words
    #     pygame.display.flip()
        
    #     if len(found_word_cells) == sum(len(word) for word, _ in selected_word_list):
    #         display_gameover_win(score, start_time)  # Display the game-over/win screen
    #         break  # Exit the game loop if all words have been found

    #     pygame.display.flip()
        
def print_trie(node, prefix):
        if node.is_end_of_word:
            print(f"{prefix} (Definition: {node.definition})")
        for char, child_node in node.children.items():
            print_trie(child_node, prefix + char)
            
def print_trie_path(node, word):
    prefix = ""
    for char in word:
        prefix += char
        print(f"{prefix} (Definition: {node.definition})")
        node = node.children[char]

    print(f"{prefix} (Definition: {node.definition})")  # Print the leaf node with definition

        
def search_word_in_trie(root, word):
    node = root
    path = []  # Store the path of search

    for char in word:
        if char in node.children:
            path.append((char, node.definition))  # Append the character and its definition to the path
            node = node.children[char]
        else:
            return None  # Return None if the character is not found in the trie

    # Append the final node's definition to the path
    if node.is_end_of_word:
        path.append((word, node.definition))
    else:
        return None  # Return None if the word is not found in the trie

    return path


def get_cells_between(start_pos, end_pos):
    cells = set()
    if start_pos and end_pos:
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row == end_row:
            # Horizontal selection
            if start_col < end_col:
                for col in range(start_col, end_col + 1):
                    cells.add((start_row, col))
            else:
                for col in range(end_col, start_col + 1):
                    cells.add((start_row, col))
        elif start_col == end_col:
            # Vertical selection
            if start_row < end_row:
                for row in range(start_row, end_row + 1):
                    cells.add((row, start_col))
            else:
                for row in range(end_row, start_row + 1):
                    cells.add((row, start_col))
        elif abs(start_row - end_row) == abs(start_col - end_col):
            # Diagonal selection
            if start_row < end_row:
                if start_col < end_col:
                    for i in range(end_row - start_row + 1):
                        cells.add((start_row + i, start_col + i))
                else:
                    for i in range(end_row - start_row + 1):
                        cells.add((start_row + i, start_col - i))
            else:
                if start_col < end_col:
                    for i in range(start_row - end_row + 1):
                        cells.add((start_row - i, start_col + i))
                else:
                    for i in range(start_row - end_row + 1):
                        cells.add((start_row - i, start_col - i))
    return cells

if __name__ == "__main__":
    main()
