from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.Amity import Amity
from dbmodels import Offices, LivingSpaces, Fellows, Staff, Allocated,\
    Unallocated


class Sessions(object):

    def __init__(self, dbname):
        db_dir = "/"
        engine = create_engine('sqlite:///' + db_dir + dbname + '.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()

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
        for room in Amity.rooms["LivingSpaces"]:
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
                fellow_name=fellow.name).first()

            if fellow_object is None:
                new_fellow = Fellows(fellow_id=fellow.id,
                                     fellow_name=fellow.name,
                                     person_type="FELLOW", wants_space="Y")
                self.session.add(new_fellow)
                self.session.commit()

            else:
                print "Database is already synced"

        print "Fellows synced successfully"

    def populate_staff(self):
        for staff in Amity.people["STAFF"]:
            staff_object = self.session.query(Staff).filter_by(
                staff_name=staff.name).first()

            if staff_object is None:
                new_staff = Staff(staff_id=staff.id,
                                  staff_name=staff.name, person_type="STAFF")
                self.session.add(new_staff)
                self.session.commit()

            else:
                print "Database is already synced"

        print "Staff synced successfully"

    def populate_allocated(self):
        for allocated in Amity.allocated_persons:
            allocate = self.session.query(Allocated).filter_by(
                livingspace_name=allocated[1].room_name,
                allocated_fellows=allocated[0].name).first()

            if allocate is None:
                add_allocations = Allocated(
                    livingspace_name=allocated[1].room_name,
                    allocated_fellows=allocated[0].name)
                self.session.add(add_allocations)
                self.session.commit()

            else:
                print "Database is already synced"

        print "Staff synced successfully"

    def populate_unallocated(self):
        for unallocated in Amity.unallocated_persons:
            unallocate = self.session.query(Unallocated).filter_by(
                fellow_name=unallocated.name).first()
            if unallocate is None:
                unallocate = Unallocated(fellow_name=unallocated.name,
                                         person_type="FELLOW", wants_space="Y")
                self.session.add(unallocate)
                self.session.commit()

            else:
                print "Database is synced"

        print "Unallocated fellows synced successfully"
