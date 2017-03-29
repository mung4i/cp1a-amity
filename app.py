#!/usr/bin/env python
"""
Usage:
    amity (-i | --interactive)
    amity (-h | --help | --version)
    amity create_room <room_type> <room_names_list>...
    amity add_person <first_name> <last_name> <person_type> [<wants_space>]
    amity allocate_person <person_fname> <person_lname> <person_type> \
    <room_type>
    amity reallocate_person <first_name> <last_name> <room_name>
    amity print_allocations [--o=filename]
    amity print_unallocated [--o=filename]
    amity print_room <room_name>
    amity load_people [--o=flename]
    amity save_state <dbname>
    amity load_state <dbname>


Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""

import cmd
import os

from termcolor import cprint
from pyfiglet import figlet_format
from docopt import docopt, DocoptExit

from models.dbmodels import create_db
from views.Amity import Amity
from models.sessions import Sessions


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            cprint(e, "yellow")
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class AmityInteractive(cmd.Cmd):
    intro = 'Welcome to Amity! An office allocation app.' \
        + ' (type help for a list of commands.)'
    prompt = '\n(Amity)'
    """
    Displays an app header after app is launched
    """

    os.system("clear")
    print("\n")
    cprint(figlet_format('AMITY', font='roman'), 'blue')
    cprint('--------------------------------------------------------------',
           'magenta')
    cprint("\tAmity is a Command Line office allocation App.", 'green')
    cprint('--------------------------------------------------------------',
           'magenta')
    cprint("\n\tNew to the app? Type 'help' to see a full list of commands\
    \n", 'white')
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_names_list>..."""
        new_room_name = arg['<room_names_list>']

        if arg['<room_type>'] in ['Office', 'OFFICE', "O", 'o']:
            new_room_type = 'Office'
            AmityInteractive.amity.create_room(new_room_type, new_room_name)
        elif arg['<room_type>'] in ['LivingSpace', 'LIVINGSPACE',
                                    'L', 'l', 'lspace', 'livingspace']:
            new_room_type = "LivingSpace"
            AmityInteractive.amity.create_room(new_room_type, new_room_name)
        else:
            cprint("\n Room type should be LivingSpace "
                   "or L or lspace if livingspace."
                   "If office it should be Office or O.", "red")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <person_fname> <person_lname> <person_type> \
        [<wants_space>]"""
        new_person_fname = arg['<person_fname>']
        new_person_lname = arg['<person_lname>']

        wants_space = arg['<wants_space>']

        if arg['<person_type>'].upper() in ['FELLOW', 'F']:
            person_type = 'FELLOW'
            if arg['<wants_space>']:
                AmityInteractive.amity.add_person_fellow(new_person_fname,
                                                         new_person_lname,
                                                         person_type,
                                                         wants_space.upper())
            else:
                AmityInteractive.amity.add_person_fellow(new_person_fname,
                                                         new_person_lname,
                                                         person_type)
        elif arg['<person_type>'].upper() in ['STAFF', 'S']:
            person_type = 'STAFF'
            if arg['<wants_space>']:
                AmityInteractive.amity.add_person_staff(new_person_fname,
                                                        new_person_lname,
                                                        person_type,
                                                        wants_space.upper())
            else:
                AmityInteractive.amity.add_person_staff(new_person_fname,
                                                        new_person_lname,
                                                        person_type)
        else:
            cprint("\n Person type should be STAFF or FELLOW", "red")

    @docopt_cmd
    def do_allocate_person(self, arg):
        """Usage: allocate_person <person_fname> <person_lname> <person_type> \
        <room_type>"""
        person_fname = arg['<person_fname>']
        person_lname = arg['<person_lname>']
        person_type = arg['<person_type>']
        room_type = arg['<room_type>']

        AmityInteractive.amity.allocate_person(
            person_fname, person_lname, person_type.upper(), room_type)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_fname> <person_lname> <person_type> \
        <room_name>"""
        person_fname = arg['<person_fname>']
        person_lname = arg['<person_lname>']
        person_type = arg['<person_type>']
        room_name = arg['<room_name>']

        AmityInteractive.amity.reallocate_person(person_fname,
                                                 person_lname,
                                                 person_type.upper(),
                                                 room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations"""

        AmityInteractive.amity.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated"""

        AmityInteractive.amity.print_unallocated()

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        room_name = arg['<room_name>']

        AmityInteractive.amity.print_room(room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""

        AmityInteractive.amity.load_people()

    @docopt_cmd
    def do_save_state(self, arg):
        """ Usage: save_state <dbname> """
        database_name = arg['<dbname>']

        create_db(database_name)
        database_object = Sessions(database_name)
        database_object.populate_offices()
        database_object.populate_livingspaces()
        database_object.populate_fellows()
        database_object.populate_staff()
        database_object.populate_allocated()
        database_object.populate_unallocated()

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <dbname> """
        database_name = arg['<dbname>']

        if os.path.exists("models/" + database_name + ".db"):
            database_object = Sessions(database_name)
            database_object.load_rooms()
            database_object.load_people()
            database_object.load_allocations()
        else:
            print "Database {0} does not exist".format(database_name)

    def do_quit(self, arg):
        """Quits out of Amity Interactive Mode."""

        print('Good Bye! Thank you for using Amity')
        exit()


if __name__ == "__main__":
    print(__doc__)
    AmityInteractive().cmdloop()
