from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.Amity import Amity
from models.Office import Office
from models.LivingSpace import LivingSpace
from models.Fellow import Fellow
from dbmodels import Offices, LivingSpaces, Fellows, Staff, Allocated,\
    Unallocated


class Sessions(object):

    def __init__(self, dbname):
        db_dir = "models/"
        engine = create_engine('sqlite:///' + db_dir + dbname + '.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.amity = Amity()

    def populate_offices(self):
        for room in Amity.rooms["Office"]:
            room_object = self.session.query(Offices).filter_by(
                office_name=room.room_name).first()

            if room_object is None:
                new_office = Offices(office_id=room.room_id,
                                     office_name=room.room_name)
                self.session.add(new_office)
                self.session.commit()

            else:
                print "Database is already synced"

        print "Rooms synced successfuly"

    def populate_livingspaces(self):
        for room in Amity.rooms["LivingSpace"]:
            room_object = self.session.query(LivingSpaces).filter_by(
                livingspace_name=room.room_name).first()

            if room_object is None:
                new_lspace = LivingSpaces(livingspace_id=room.room_id,
                                          livingspace_name=room.room_name)
                self.session.add(new_lspace)
                self.session.commit()

            else:
                print "Database is already synced"

        print "Rooms synced successfuly"

    def populate_fellows(self):
        for fellow in Amity.people["FELLOWS"]:
            fellow_object = self.session.query(Fellows).filter_by(
                first_name=Fellows.first_name, last_name=Fellows.last_name).first()

            if fellow_object is None:
                new_fellow = Fellows(fellow_id=Fellows.employeeID,
                                     first_name=Fellows.first_name,
                                     last_name=Fellows.last_name,
                                     person_type="FELLOW", wants_space="Y")
                self.session.add(new_fellow)
                self.session.commit()

            else:
                print "Database is already synced"

        print "Fellows synced successfully"

    def populate_staff(self):
        for staff in Amity.people["STAFF"]:
            staff_object = self.session.query(Staff).filter_by(
                first_name=staff.first_name, last_name=staff.last_name).first()

            if staff_object is None:
                new_staff = Staff(staff_id=staff.employeeID,
                                  first_name=staff.first_name,
                                  last_name=staff.last_name,
                                  person_type="STAFF")
                self.session.add(new_staff)
                self.session.commit()

            else:
                print "Database is already synced"

        print "Staff synced successfully"

    def populate_allocated(self):
        for allocated in Amity.allocated_persons:
            allocate = self.session.query(Allocated).filter_by(
                livingspace_name=allocated[1].room_name,
                allocated_fellows_fname=allocated[0].first_name,
                allocated_fellows_lname=allocated[0].last_name).first()

            if allocate is None:
                add_allocations = Allocated(
                    livingspace_name=allocated[1].room_name,
                    allocated_fellows_fname=allocated[0].first_name,
                    allocated_fellows_lname=allocated[0].last_name)
                self.session.add(add_allocations)
                self.session.commit()

            else:
                print "Database is already synced"

        print "Staff synced successfully"

    def populate_unallocated(self):
        for unallocated in Amity.unallocated_persons:
            unallocate = self.session.query(Unallocated).filter_by(
                first_name=unallocated.first_name, last_name=unallocated.last_name).first()
            if unallocate is None:
                unallocate = Unallocated(first_name=unallocated.first_name,
                                         last_name=unallocated.last_name,
                                         person_type="FELLOW", wants_space="Y")
                self.session.add(unallocate)
                self.session.commit()

            else:
                print "Database is synced"

        print "Unallocated fellows synced successfully"

    def load_rooms(self):
        offices = self.session.query(Offices).all()
        livingspaces = self.session.query(LivingSpaces).all()

        for office in offices:
            old_office = Office(office.office_name)
            old_office.room_id = office.office_id
            Amity.rooms["Office"].append(old_office)

        for livingspace in livingspaces:
            old_lspace = LivingSpace(livingspace.livingspace_name)
            old_lspace.room_id = livingspace.livingspace_id
            Amity.rooms["LivingSpace"].append(old_lspace)

        print "Rooms loaded successfully"

    def load_people(self):
        fellows = self.session.query(Fellows).all()
        staff = self.session.query(Staff).all()

        for fellow in fellows:
            old_fellow = Fellow(fellow.first_name, fellow.last_name)
            old_fellow.employeeID = fellow.fellow_id
            Amity.people["FELLOWS"].append(old_fellow)

        for person in staff:
            old_staff = Staff()
            old_staff.first_name = person.first_name
            old_staff.last_name = person.last_name
            old_staff.employeeID = person.staff_id
            Amity.people["STAFF"].append(old_staff)

        print "People loaded successfully"

    def load_allocations(self):
        allocations = self.session.query(Allocated).all()
        unallocations = self.session.query(Unallocated).all()

        for allocated in allocations:
            person_fname = allocated.allocated_fellows_fname
            person_lname = allocated.allocated_fellows_lname
            room = allocated.livingspace_name

            room_obj = self.amity.get_roomobject(room)
            person_obj = self.amity.get_fellowobject(person_fname, person_lname)

            Amity.allocated_persons.append([person_obj, room_obj])
            room_obj.append.occupants(person_obj)

        for unallocated in unallocations:
            person_fname = unallocated.first_name
            person_lname = unallocated.last_name
            person_obj = self.amity.get_fellowobject(person_fname, person_lname)
            Amity.unallocated_persons.append(person_obj)

        print "Allocations loaded successfully"
