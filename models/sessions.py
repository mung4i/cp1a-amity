from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from views.Amity import Amity
from views.Room import Office, LivingSpace
from views.Person import Fellow, Staff
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
                print "{0} has been added to the database".format(
                    room.room_name)

            else:
                self.session.commit()

        print "Success! Offices have been synced"

    def populate_livingspaces(self):
        for room in Amity.rooms["LivingSpace"]:
            room_object = self.session.query(LivingSpaces).filter_by(
                livingspace_name=room.room_name).first()

            if room_object is None:
                new_lspace = LivingSpaces(livingspace_id=room.room_id,
                                          livingspace_name=room.room_name)
                self.session.add(new_lspace)
                self.session.commit()
                print "{0} has been added to the database".format(
                    room.room_name)

            else:
                self.session.commit()

        print "Success! Living spaces have been synced"

    def populate_fellows(self):
        for fellow in Amity.people["FELLOWS"]:
            fellow_object = self.session.query(Fellows).filter_by(
                first_name=fellow.first_name,
                last_name=fellow.last_name).first()

            if fellow_object is None:
                new_fellow = Fellows(fellow_id=fellow.employeeID,
                                     first_name=fellow.first_name,
                                     last_name=fellow.last_name,
                                     person_type="FELLOW", wants_space="Y")
                self.session.add(new_fellow)
                self.session.commit()
                print "{0} {1} has been added to the database".format(
                    fellow.first_name, fellow.last_name)

            else:
                self.session.commit()
        print "Success! Fellows have been synced"

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
                print "{0} {1} has been added to the database".format(
                    staff.first_name, staff.last_name)
            else:
                self.session.commit()
        print "Success! Staff have been synced"

    def populate_allocated(self):
        # try:
        for rooms in Amity.rooms["Office"]:
            staff = rooms.occupants
            for staff_object in staff:
                allocated_persons = self.session.query(Allocated).filter_by(
                    first_name=staff_object.first_name,
                    last_name=staff_object.last_name).first()
                if allocated_persons is None:
                    if staff_object.role == 'staff':
                        allocated = Allocated(id=staff_object.employeeID,
                                              first_name=staff_object.first_name,
                                              last_name=staff_object.last_name,
                                              person_type="STAFF",
                                              office=rooms.room_name,
                                              livingspace="None")
                    if staff_object.role == 'fellow':
                        allocated = Allocated(id=staff_object.employeeID,
                                              first_name=staff_object.first_name,
                                              last_name=staff_object.last_name,
                                              person_type="FELLOWS",
                                              office=rooms.room_name)
                    self.session.add(allocated)
                    self.session.commit()
                print "{0} {1} has been added to the database".format(
                    staff_object.first_name, staff_object.last_name)

        for rooms in Amity.rooms["LivingSpace"]:
            fellows = rooms.occupants
            for i in fellows:
                fellows_object = i
                allocated_persons = self.session.query(Allocated).filter_by(
                    first_name=fellows_object.first_name,
                    last_name=fellows_object.last_name,
                    livingspace=rooms.room_name).first()
                if allocated_persons is None:

                    allocated = Allocated(id=fellows_object.employeeID,
                                          first_name=fellows_object.first_name,
                                          last_name=fellows_object.last_name,
                                          person_type="FELLOWS",
                                          livingspace=rooms.room_name)
                    self.session.add(allocated)
                    self.session.commit()
                print "{0} {1} has been added to the database".format(
                    fellows_object.first_name, fellows_object.last_name)

    def populate_unallocated(self):
        for unallocated in Amity.unallocated_persons:
            unallocate = self.session.query(Unallocated).filter_by(
                first_name=Unallocated.first_name,
                last_name=Unallocated.last_name).first()
            if unallocate is None:
                unallocate = Unallocated(id=unallocated.employeeID,
                                         first_name=unallocated.first_name,
                                         last_name=unallocated.last_name,
                                         person_type="FELLOW", wants_space="Y")
                self.session.add(unallocate)
                self.session.commit()
                print "{0} {1} has been added to unallocated".format(
                    unallocated.first_name, unallocated.last_name)

            else:
                self.session.commit()
                print "Database is synced"

    def load_rooms(self):
        offices = self.session.query(Offices).all()
        livingspaces = self.session.query(LivingSpaces).all()

        for office in offices:
            old_office = Office(office.office_name)
            old_office.room_name = office.office_name
            old_office.room_id = office.office_id
            Amity.rooms["Office"].append(old_office)
            print Amity.rooms["Office"]

        for livingspace in livingspaces:
            old_lspace = LivingSpace(livingspace.livingspace_name)
            old_lspace.room_id = livingspace.livingspace_id
            Amity.rooms["LivingSpace"].append(old_lspace)
            print Amity.rooms["LivingSpace"]

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
            livingspace = allocated.livingspace
            office = allocated.office
            for lspace in Amity.rooms["LivingSpace"]:
                if lspace.room_name == livingspace:
                    person_obj = self.amity.get_fellowobject(
                        allocated.first_name, allocated.last_name)
                    lspace.occupants.append(person_obj)
            for ospace in Amity.rooms["Office"]:
                if ospace.room_name == office:
                    if allocated.person_type == "FELLOWS":
                        person_obj = self.amity.get_fellowobject(
                            allocated.first_name, allocated.last_name)
                        ospace.occupants.append(person_obj)
                    if allocated.person_type == "STAFF":
                        staff_obj = self.amity.get_staffobject(
                            allocated.first_name, allocated.last_name)
                        ospace.occupants.append(staff_obj)

        for unallocated in unallocations:
            person_obj = Fellow(unallocated.first_name, unallocated.last_name)
            person_obj.employeeID = unallocated.id
            Amity.unallocated_persons.append(person_obj)
            Amity.people["FELLOWS"].append(person_obj)

        print "Allocations loaded successfully"
