# Dictionary, Flash Cards & Quiz Generator by Maria Regina Sirilan
# A handy little study tool that allows you to store definitions and generate flash cards/quizzes

import os
import random
import sys


def get_data(filename):
    """(str[, delim]) -> dict of {str: str}
    Return a dictionary containing terms and definitions from file.

    SAMPLE FILE FORMAT (.txt):
    term1||definition1
    term2||definition2
    """
    file = open(filename, 'r')
    data = {}
    for line in file.readlines():
        line = line.strip().split('||')
        data[line[0]] = line[1]
    file.close()
    return data


def get_fake_data():
    """() -> dict of {str: str}
    Return a dictionary containing auto-generated terms and definitions.
    Obtained from: https://www.vocabulary.com/lists/17051
    """
    return {
        'aftermath': 'the consequences of a (catastrophic) event',
        'caprice': 'a sudden desire',
        'dapper': 'marked by up-to-dateness in dress and manners',
        'fiddle-faddle': 'trivial nonsense',
        'heyday': 'the period of greatest prosperity or productivity',
        'prate': 'speak about unimportant matters rapidly and incessantly',
        'revered': 'profoundly honored',
        'timbre': 'the distinctive property of a complex sound',
        'upsurge': 'a sudden or abrupt strong increase',
        'whimsy': 'an odd or fanciful or capricious idea'
    }


def save_data(dictionary, filename):
    """(dict of {str: str}, str) -> None
    Write the contents of dictionary into filename.

    SAMPLE FILE FORMAT (.txt):
    term1||definition1
    term2||definition2
    """
    file = open(filename, 'w')
    for term, defn in dictionary.items():
        file.write(term + '||' + defn + '\n')
    file.close()


def add_entry(dictionary, term, definition):
    """(dict, str, str) -> dict
    Return a new dictionary with the new term & definition added.
    """
    new_dict = dictionary.copy()
    new_dict[term] = definition
    return new_dict


def delete_entry(dictionary, term):
    """(dict, str, str) -> dict of {str: str}
    Return a new dictionary with the term removed.
    """
    new_dict = dictionary.copy()
    if term in new_dict:
        new_dict.pop(term)
    return new_dict


def generate_quiz1(dictionary):
    """(dict) -> dict of {str: list of str}
    Return a new dictionary with terms as keys, and values as lists containing
    the corresponding definition and three random incorrect definitions.
    """
    quiz = {}
    defs = list(dictionary.values())
    for term, defn in dictionary.items():
        random.shuffle(defs)
        quiz[term] = [defn]
        i = 0
        while len(quiz[term]) < 4 and i < len(defs):
            new_def = defs[i]
            if new_def not in quiz[term]:
                quiz[term].append(new_def)
            i += 1
    return quiz


def generate_quiz2(dictionary):
    """(dict) -> dict of {str: list of str}
    Return a new dictionary with definitions as keys, and values as lists
    containing the corresponding term and three random incorrect terms.
    """
    quiz = {}
    terms = list(dictionary.keys())
    for term, defn in dictionary.items():
        random.shuffle(terms)
        quiz[defn] = [term]
        i = 0
        while len(quiz[defn]) < 4 and i < len(terms):
            new_term = terms[i]
            if new_term not in quiz[defn]:
                quiz[defn].append(new_term)
            i += 1
    return quiz


def div():
    """(None or str) -> None
    Print a line break.
    """
    print('-' * 69)


def format_entry(term, defn):
    """(str, str[, str]) -> str
    Return a formatted str using the given term and definition.
    """
    return '> {0}\n      {1}'.format(term, defn)


def alert_test(test_enabled):
    """(bool) -> None
    Print an alert if test_enabled is True.
    """
    if test_enabled:
        print('> [TEST MODE] Changes will not be saved to file.')


def take_quiz(bank, ver):
    """(dict, str) -> None
    Given a dictionary and quiz version, display the key and prompt the
    user to select the correct element from the list (value), where the
    element at index 0 is correct and the rest are incorrect. Then,
    display the user's score.
    """
    questions = bank.items()
    # Check for sufficient entries
    if not len(questions):
        print('> There aren\'t enough entries to generate a quiz.')
        input('> Press ENTER to go back. ')
    else:
        # Display version-dependent instructions
        if ver == '1':
            print('> Match the term to the correct definition.')
        else:
            print('> Match the definition to the correct term.')
        input('> Press ENTER to start. ')
        div()
        # Initialize score and question counters
        count = 1
        score = 0
        limit = len(questions)
        answer = None
        # Display a question then prompt and check the user's answer
        for q in questions:
            key, value = q[0], q[1]
            print('> Question {0} of {1}:'.format(count, limit))
            print('\n  ' + key + '\n')
            count += 1
            choices = value.copy()
            random.shuffle(choices)
            letters = ['1 - ', '2 - ', '3 - ', '4 - ']
            for index in range(len(choices)):
                print('  ' + letters[index] + choices[index])
            print()
            answer = input('> Enter your answer (1-4) or ' +
                           '\'quit\' to go back: ')
            if answer == '1':
                answer = choices[0]
            elif answer == '2':
                answer = choices[1]
            elif answer == '3':
                answer = choices[2]
            elif answer == '4':
                answer = choices[3]
            elif answer == 'quit':
                break
            else:
                answer = None
            div()
            if answer == value[0]:
                print('> CORRECT!')
                score += 1
            else:
                print('> INCORRECT!')
                if ver == '1':
                    print(format_entry(key, value[0]))
                else:
                    print(format_entry(value[0], key))
            div()
            input('> Press ENTER to continue. ')
            div()
        if answer != 'quit':
            print('> Your score: {0}/{1}'.format(score, limit))
            input('> Press ENTER to go back. ')


def display_dict(dictionary, term=None):
    """(dict[, str or None]) -> None
    Print the given key and its corresponding value. If no key is
    specified, print all terms their definitions.
    """
    # If a term is specified, check that it exists
    if term is not None:
        if term not in dictionary:
            print('> No entry found for \'{0}\'.'.format(term))
        else:
            print(format_entry(term, dictionary[term]))
    # Otherwise, display all terms and definitions
    else:
        if not dictionary:
            print('> There aren\'t any entries to display')
        else:
            entries = list(dictionary.items())
            entries.sort()
            for term, defn in entries:
                print(format_entry(term, defn))
            div()
            print('> Total entries:', len(entries))
        input('> Press ENTER to go back. ')


def display_menu(test_enabled):
    """(bool) -> str
    Print the user control menu then return the user's selection.
    """
    div()
    choice = ''
    tag = ''
    while choice not in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
        print('> MENU:')
        print('  1 - View all definitions')
        print('  2 - Search for a definition')
        print('  3 - Add/edit an entry')
        print('  4 - Delete an entry')
        print('  5 - Test your knowledge')
        print('  6 - Load saved data')
        print('  7 - Clear all entries')
        if test_enabled:
            print('  8 - Test Mode: [ON] OFF')
            tag = '[TEST MODE]'
        else:
            print('  8 - Test Mode: ON [OFF]')
        print('  9 - Quit the program')
        div()
        choice = input('> ' + tag + ' Enter an option (1-8): ')
        div()
    return choice


if __name__ == '__main__':

    # Initialize data files and variables
    filename = 'dfq_data.txt'
    if not os.path.isfile(filename):
        save_data({}, filename)
    data = get_data(filename)
    test_mode = False
    loop = True

    # Loop the menu prompt until the user exits
    while loop:
        choice = display_menu(test_mode)
        # 1 - View all definitions
        if choice == '1':
            display_dict(data)
        # 2 - Search for a definition
        elif choice == '2':
            search = input('> Search for a term or \'quit\' to go back: ')
            while search != 'quit':
                div()
                display_dict(data, search)
                div()
                search = input('> Search for a term or \'quit\' to go back: ')
        # 3 - Add/edit an entry
        elif choice == '3':
            alert_test(test_mode)
            term = input('> Enter a term: ')
            defn = input('> Enter a definition: ')
            div()
            print(format_entry(term, defn))
            div()
            # Verify user selection
            check = input('> Is this correct? (Y/N): ').lower()
            while check not in ('y', 'n'):
                check = input('> Is this correct? (Y/N): ').lower()
            if check == 'y':
                confirm = True
                # Check if term already exists and verify again
                if term in data:
                    confirm = False
                    div()
                    print('> An entry for {0} already exists:'.format(term))
                    print(format_entry(term, data[term]))
                    div()
                    replace = input('> Replace? (Y/N): ').lower()
                    while replace not in ('y', 'n'):
                        replace = input('> Replace? (Y/N): ').lower()
                    if replace == 'y':
                        confirm = True
                if confirm:
                    data = add_entry(data, term, defn)
                    if not test_mode:
                        save_data(data, filename)
                    div()
                    print('> Successfully added entry for ' +
                          '\'{0}\'.'.format(term))
                    input('> Press ENTER to go back. ')
        # Delete an entry
        elif choice == '4':
            alert_test(test_mode)
            term = input('> Enter a term to delete or \'quit\' ' +
                         'to go back: ').lower()
            if term != 'quit':
                if term not in data:
                    print('> No entry found for \'{0}\'.'.format(term))
                elif term in data:
                    display_dict(data, term)
                    div()
                    # Verify user selection
                    check = input('> Delete? (Y/N): ').lower()
                    while check not in ('y', 'n'):
                        check = input('> Delete (Y/N): ').lower()
                    if check == 'y':
                        data.pop(term)
                        if not test_mode:
                            save_data(data, filename)
                        div()
                        print('> Successfully removed entry for ' +
                              '\'{0}\'.'.format(term))
                        input('> Press ENTER to go back. ')
        # 5 - Test your knowledge
        elif choice == '5':
            version = None
            while version not in ('1', '2', '3', 'quit'):
                print('> TEST YOUR KNOWLEDGE:')
                print('  1 - Multiple-choice quiz: Choose the definition')
                print('  2 - Multiple-choice quiz: Choose the term')
                print('  3 - Flash cards')
                div()
                version = input('> Enter an option (1-3) or ' +
                                '\'quit\' to go back: ').lower()
                if version != 'quit':
                    div()
            # Generate test banks and execute a quiz
            if version == '1':
                take_quiz(generate_quiz1(data), version)
            elif version == '2':
                take_quiz(generate_quiz2(data), version)
            # Display entries as randomized flash cards
            elif version == '3':
                if data:
                    end = None
                    print('> Random cards will be displayed one at a time.')
                    print('> Press ENTER to continue or enter \'quit\' at any')
                    print('  time to go back.')
                    div()
                    input('> Press ENTER to start. ')
                    cards = list((data.items()))
                    random.shuffle(cards)
                    for term, defn in cards:
                        div()
                        end = input('> ' + term + ' ')
                        if end == 'quit':
                            break
                        else:
                            end = input('      ' + defn + ' ')

                            if end == 'quit':
                                break
                    if end != 'quit':
                        div()
                        print('> You\'ve reached the end!')
                        input('> Press ENTER to go back. ')
                else:
                    print('> There aren\'t enough entries.')
                    input('> Press ENTER to go back. ')
        # 6 - Load saved data
        elif choice == '6':
            fetch = False
            # Create a save file if needed
            if not os.path.isfile(filename):
                print('> Save file ({0}) could not be found.'.format(filename))
                div()
                create = input('Create new save file? (Y/N): ')
                while create not in ('y', 'n'):
                    create = input('Create new save file? (Y/N): ')
                if create == 'y':
                    save_data({}, filename)
                    fetch = True
                    div()
                    print('> Local save file created ({0}).'.format(filename))
            else:
                load = get_data(filename)
                confirm = input('> Load saved data? (Y/N): ').lower()
                while confirm not in ('y', 'n'):
                    confirm = input('> Load saved data? (Y/N): ').lower()
                if confirm == 'y':
                    fetch = True
                    div()
                    print('> Successfully loaded \'{0}\'.'.format(filename))
            if fetch:
                data = get_data(filename)
                if test_mode:
                    print('> TEST MODE has been disabled.')
                    test_mode = False
                print('> Total entries:', len(data))
                input('> Press ENTER to go back. ')
        # 7 - Delete saved data
        elif choice == '7':
            alert_test(test_mode)
            print('> Total entries:', len(data))
            confirm = input('> Clear all entries? (Y/N): ').lower()
            while confirm not in ('y', 'n'):
                confirm = input('> Clear all entries? (Y/N): ').lower()
            if confirm == 'y':
                data = {}
                if not test_mode:
                    save_data(data, filename)
        # 8 - Toggle TEST MODE
        elif choice == '8':
            if not test_mode:
                print('> Sample entries will be generated for testing purposes.')
                print(
                    '> This disables all saved data file modification functionalities.')
                print('> You may disable TEST MODE by loading your saved data from')
                print('  the menu (option 6) at any time.')
                confirm = ''
                while confirm not in ('y', 'n'):
                    div()
                    confirm = input('> Continue? (Y/N): ').lower()
                if confirm == 'y':
                    div()
                    data = get_fake_data()
                    test_mode = True
                    print('> TEST MODE has been enabled.')
                    input('> Press ENTER to go back. ')
            else:
                print('> TEST MODE is already enabled.')
                print('> You may disable TEST MODE by loading your saved data from')
                print('  the menu (option 6) at any time.')
                input('> Press ENTER to go back. ')
        # 9 - Quit the program
        elif choice == '9':
            loop = False
