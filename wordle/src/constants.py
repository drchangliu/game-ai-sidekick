from openai.types.chat_model import ChatModel

# Originally used in AnimationObject. Imported to gameloop
DEFAULT_FRAMERATE = 60

# from LetterCell
LETTER_GRID_WIDTH = 620
LETTER_GRID_HEIGHT = 520
WORD_LENGTH = 5
BORDER_OFFSET_Y = 10
SPACE_BETWEEN_CELLS = 8

# from letter button
# constants to hold letter button sizes
LETTER_BUTTON_SPACING = 5
LETTER_BUTTON_OFFSET_X = 10
LETTER_BUTTON_OFFSET_Y_TOP = 90
LETTER_BUTTON_OFFSET_Y_BOTTOM = 10
LETTER_BUTTON_WIDTH = (LETTER_GRID_WIDTH - 9 *
                       LETTER_BUTTON_SPACING - 2 * LETTER_BUTTON_OFFSET_X) / 10
LETTER_BUTTON_AREA_HEIGHT = LETTER_BUTTON_WIDTH * 3 + \
    LETTER_BUTTON_SPACING * 2 + LETTER_BUTTON_OFFSET_Y_TOP + \
    LETTER_BUTTON_OFFSET_Y_BOTTOM

# from setup
# DON'T TOUCH THESE VALUES -> they are conditional to the length of the word and number of guesses
SCREEN_WIDTH = LETTER_GRID_WIDTH
SCREEN_HEIGHT = LETTER_GRID_HEIGHT + LETTER_BUTTON_AREA_HEIGHT

# from end_screen
BACKGROUND_WIDTH = SCREEN_WIDTH - 2 * 40
BACKGROUND_HEIGHT = 240

# from Words
# constants for animations
ANIMATION_JUMP_HEIGHT = 10
ANIMATION_SHAKE_HEIGHT = 5
ANIMATION_DURATION = 250
FEEDBACK_DIFF_DURATION = ANIMATION_DURATION - 50
NUM_SHAKES = 3

# from GameState
LETTERS = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
    ["z", "x", "c", "v", "b", "n", "m", "back", "enter"]
]

# hint constants
MIN_NUM_GUESSES = 5
MIN_LETTERS_TO_ADD = 3

LLM_MODEL: ChatModel = "gpt-4.1"
MAX_LLM_CONTINUOUS_CALLS = 5

LLM_PLATFORM = "openai"
LOG_LLM_MESSAGES = False
ERROR_MESSAGE_VISIBLE_TIME = 5
