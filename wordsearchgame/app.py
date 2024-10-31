'''from flask import Flask, render_template, jsonify
import random
import string
import pygame
import sys

app = Flask(__name__)

# Your Word Search game classes and functions go here (trie, word search graph, etc.)


@app.route('/')
def index():
    return render_template('wordsearchfront.html')


@app.route('/start_game')
def start_game():
    # Code to start the Word Search game
    global game_instance  # Assuming you have a global instance of your game class
    game_instance = main()  # Call your main function to start the game
    return jsonify({'message': 'Game started successfully'})

@app.route('/game')
def game():
    return render_template('game.html')



@app.route('/check_word/<word>')
def check_word(word):
    global game_instance
    if game_instance:
        # Check if the word is found in the game
        if word.upper() in game_instance.found_words:
            return jsonify({'status': 'success', 'message': 'Word found!'})
        else:
            return jsonify({'status': 'error', 'message': 'Word not found!'})
    else:
        return jsonify({'status': 'error', 'message': 'Game not started!'})


if __name__ == '__main__':
    app.run(debug=True)'''

'''from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return render_template('wordsearchfront.html')

@app.route('/start_game', methods=['POST'])  # Change the method to POST
def start_game():
    # Code to start the Word Search game
    # Replace this with your actual game initialization code
    return jsonify({'message': 'Game started successfully'})

if __name__ == '__main__':
    app.run(debug=True)'''
    

'''from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return render_template('wordsearchfront.html')

@app.route('/start_game', methods=['POST'])  # Change the method to POST
def start_game():
    # Code to start the Word Search game
    # Replace this with your actual game initialization code
    return jsonify({'message': 'Game started successfully'})

@app.route('/game')  # Define route for the game page
def game():
    return render_template('game.html')  # Assuming you have a template for the game page



if __name__ == '__main__':
    app.run(debug=True)
    
# Flask app with Word Search game integrated'''
# Import the required libraries
'''import random
import string
import pygame
import sys
from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# Define colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define the TrieNode and Trie classes

# Define the WordSearchGraph and WordSearchCSP classes

# Define the main function to run the game
def pygame_page():
    # Initialize Pygame
    pygame.init()

    # Set up the screen dimensions
    screen_width = 800
    screen_height = 800
    SCREEN = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Word Search Game")

    # Run your main game loop here
    # You can copy and paste your main() function here
    
    # Quit Pygame
    pygame.quit()

# Define the Flask route for the start page
@app.route('/')
def start_page():
    return render_template('start_page.html')



@app.route('/start_game', methods=['POST'])
def start_game():
    # Generate the grid data for the Word Search game
    grid_data = generate_word_search_grid()  # You need to implement this function

    # Render the start_game.html template with the grid data
    return render_template('start_game.html', grid_data=grid_data)


# Define the Flask route for the game page
@app.route('/pygame_page')
def run_word_search_game():
    # Run the Pygame Word Search game function
    pygame_page()
    
    # Return a placeholder message (this will not be visible to the user)
    return 'Pygame page'

if __name__ == '__main__':
    app.run(debug=True)'''
# Import the required libraries
import random
import string
import pygame
import sys
from flask import Flask, render_template
from finalchange_adsa import main



# Initialize the Flask application
app = Flask(__name__)

# Define colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define the TrieNode and Trie classes
# Define the WordSearchGraph and WordSearchCSP classes

# Define the main function to run the game
def pygame_page():
    # Initialize Pygame
    pygame.init()

    # Set up the screen dimensions
    screen_width = 800
    screen_height = 800
    SCREEN = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Word Search Game")

    # Run your main game loop here
    # You can copy and paste your main() function here
    
    # Quit Pygame
    pygame.quit()

# Define the Flask route for the Pygame page
@app.route('/')
def home():
    return render_template('start_page.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    # Run the Pygame Word Search game function
    pygame_page()
    
    # Return a placeholder message (this will not be visible to the user)
    return main()

if __name__ == '__main__':
    app.run(debug=True)



