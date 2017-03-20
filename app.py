#!/usr/bin/env python
"""
Usage:
    amity (-i | --interactive)
    amity (-h | --help | --version)
    amity create_room <room_type> <room_names_list>...
    amity add_person <first_name> <last_name> <person_type> <wants_space>
    amity reallocatePerson <first_name> <last_name> <room_name>
    amity print_allocations [--o=filename]
    amity print_unallocated [--o=filename]
    amity load_people [--o=flename]


Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""

import sys
import cmd
import os
from docopt import docopt, DocoptExit
from dbmodels import create_db
from models.Amity import Amity
from sessions import Sessions


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
            print(e)
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
    intro = 'Welcome to my Amity allocation!' \
        + ' (type help for a list of commands.)'
    prompt = '<amity>'
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_names_list>..."""
        new_room_name = arg['<room_names_list>']
        new_room_type = arg['<room_type>']
        AmityInteractive.amity.create_room(new_room_name, new_room_type)

    @docopt_cmd
    def do_add_people(self, arg):
        """Usage: add_people <person_fname> <person_lname> <person_type> <wants_space>"""
        new_person_fname = arg['<person_fname>']
        new_person_lname = arg['<person_lname>']
        person_type = arg['<person_type>']
        wants_space = arg['<wants_space>']

        AmityInteractive.amity.add_people(new_person_fname, new_person_lname, person_type.upper(),
                                          wants_space.upper())

    @docopt_cmd
    def do_allocate_person(self, arg):
        """Usage: allocate_person <person_fname> <person_lname> <person_type> <room_name>"""
        person_fname = arg['<person_fname>']
        person_lname = arg['<person_lname>']
        person_type = arg['<person_type>']
        room_name = arg['<room_name>']

        AmityInteractive.amity.allocate_person(person_fname, person_lname, person_type.upper(),
                                               room_name)

    @docopt_cmd
    def do_reallocatePerson(self, arg):
        """Usage: reallocatePerson <person_fname> <person_lname> <person_type> <room_name>"""
        person_fname = arg['<person_fname>']
        person_lname = arg['<person_lname>']
        person_type = arg['<person_type>']
        room_name = arg['<room_name>']

        AmityInteractive.amity.reallocatePerson(person_fname, person_lname, person_type.upper(),
                                                room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""
        filename = arg['--o']

        AmityInteractive.amity.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        filename = arg['--o']

        AmityInteractive.amity.print_unallocated()

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people [--o=filename]"""
        filename = arg['--o']

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

        print('Good Bye!')
        exit()


if __name__ == "__main__":
    AmityInteractive().cmdloop()
