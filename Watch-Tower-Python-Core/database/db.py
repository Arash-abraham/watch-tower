# MySql or Mongo ? I using MySql
# Database -> watc-tower 
# Tables : programs , subdoamin , live , etc ...
# Programs -> 
    # - program_name 
    # - spcopes 
    # - out-scope 
    # - crated_at
    # - updated_at 

from sqlalchemy import create_engine, Column, String, DateTime, Text , text , JSON , Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from colorama import *
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config

load_dotenv()

db_host = config.DB_HOST
db_user = config.DB_USER
db_pass = config.DB_PASS
db_name = config.DB_NAME
db_port = config.DB_PORT

DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URI)
Base = declarative_base()


def check_and_create_database():

    try:
        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/"
        )
        
        with engine.connect() as conn:
            result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'"))
            if result.fetchone():
                # print(f" Database '{db_name}' has exist !")
                return 'Exist'
            else:
                # print(f" Database '{db_name}' dose not exist !")
                create = input(f"Do you want the database '{db_name}' to be created (y/n) : ")
                
                if create.lower() == 'y':
                    conn.execute(text(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                    conn.commit()
                    return 'Exist'
                else:
                    return 'NoExist'
                    
    except Exception as e:
        return e
    except KeyboardInterrupt:
        sys.exit(1)

class Programs(Base):
    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    program_name = Column(String(255), unique=True, nullable=False)  
    
    config = Column(JSON, nullable=True) 
    
    scopes = Column(JSON, default=[])
    outScopes = Column(JSON, default=[])
    
    created_date = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Subdomains(Base):
    __tablename__ = 'subdomains'

    program_name = Column(String(255), primary_key=True)
    subdomain = Column(String(255), primary_key=True)
    
    scope = Column(String(255), nullable=False)
    
    providers = Column(Text, default="")
    
    created_date = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class ProgramsInBugCrowd(Base):
    __tablename__ = 'bugcrowd_programs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    program_name = Column(String(255), unique=True, nullable=False)
    program_url = Column(String(500), nullable=True)
    allows_disclosure = Column(String(50), nullable=True)
    managed_by_bugcrowd = Column(String(50), nullable=True)
    safe_harbor = Column(String(50), nullable=True)
    max_payout = Column(Integer, nullable=True)
    in_scope = Column(JSON, default=[])
    out_of_scope = Column(JSON, default=[])
    created_date = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)


def upsert_program(program_name, scopes, outScopes, config):
    if scopes is None:
        scopes = []
    if outScopes is None:
        outScopes = []
    if config is None:
        config = {}
    
    conflicts = set(scopes) & set(outScopes)

    if conflicts:
        print(Fore.RED + "\n" + "="*50)
        print(f"  CONFLICT: {program_name}")
        print("="*50)
        print(Fore.YELLOW + f"  Domain(s): {', '.join(conflicts)}")
        print(Fore.WHITE + f"  Problem: Appears in both 'scope' and 'out-scope'")
        print(Fore.CYAN + f"  Solution: Remove from one of them" + Fore.RESET)
        print()
        return None
    db_status = check_and_create_database()
    if db_status != 'Exist':
        if db_status == 'NoExist':
            print('To use the program with a specified name in env, create a database for the database.')
            sys.exit(1)
        else:
            print(Fore.WHITE+'We have a problem! '+ Fore.RED +f'\n{db_status}')
            sys.exit(1)
    
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        program = session.query(Programs).filter_by(program_name=program_name).first()
        
        if program:

            old_scopes = set(program.scopes)
            old_outScopes = set(program.outScopes)

            new_scopes = set(scopes)
            new_outScopes = set(outScopes)
            
            program.scopes = scopes
            program.outScopes = outScopes
            program.config = config
            
            session.commit()
            
            added_scopes = new_scopes - old_scopes
            removed_scopes = old_scopes - new_scopes
            added_outScopes = new_outScopes - old_outScopes
            removed_outScopes = old_outScopes - new_outScopes
            
            print(f"[{current_time()}] Updated program: {program.program_name}")
            
            if added_scopes:
                print(f"  + Added scopes ({len(added_scopes)}): {list(added_scopes)}")
            if removed_scopes:
                print(f"  - Removed scopes ({len(removed_scopes)}): {list(removed_scopes)}")
            if added_outScopes:
                print(f"  + Added out-scopes ({len(added_outScopes)}): {list(added_outScopes)}")
            if removed_outScopes:
                print(f"  - Removed out-scopes ({len(removed_outScopes)}): {list(removed_outScopes)}")
            
            if not added_scopes and not removed_scopes and not added_outScopes and not removed_outScopes:
                print("  No changes detected.")
        else:
            new_program = Programs(
                program_name=program_name,
                created_date=datetime.now(),
                config=config,
                scopes=scopes, 
                outScopes=outScopes
            )
            session.add(new_program) 
            session.commit()
            print(f"[{current_time()}] Inserted new program: {new_program.program_name}")
            print(f"  Scopes: {new_program.scopes}") 
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        session.close()
        
def current_time():
    now = datetime.now()

    return now.strftime("%Y-%m-%d %H:%M:%S")



def insert_all_bugcrowd_programs(all_data):
    db_status = check_and_create_database()
    if db_status != 'Exist':
        if db_status == 'NoExist':
            print('To use the program with a specified name in env, create a database for the database.')
            sys.exit(1)
        else:
            print(Fore.WHITE + 'We have a problem! ' + Fore.RED + f'\n{db_status}')
            sys.exit(1)
    
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    inserted_count = 0
    updated_count = 0
    
    try:
        for program_data in all_data:
            program_name = program_data.get('name')
            if not program_name:
                print(Fore.RED + f"Warning: Program without name, skipping..." + Fore.RESET)
                continue

            in_scope_list = program_data.get('targets', {}).get('in_scope', [])
            out_of_scope_list = program_data.get('targets', {}).get('out_of_scope', [])
            
            existing = session.query(ProgramsInBugCrowd).filter_by(program_name=program_name).first()
            
            if existing:
                existing.program_url = program_data.get('url')
                existing.allows_disclosure = str(program_data.get('allows_disclosure', False))
                existing.managed_by_bugcrowd = str(program_data.get('managed_by_bugcrowd', False))
                existing.safe_harbor = program_data.get('safe_harbor')
                existing.max_payout = program_data.get('max_payout')
                existing.in_scope = in_scope_list
                existing.out_of_scope = out_of_scope_list
                existing.last_update = datetime.now()
                updated_count += 1
            else:
                new_program = ProgramsInBugCrowd(
                    program_name=program_name,
                    program_url=program_data.get('url'),
                    allows_disclosure=str(program_data.get('allows_disclosure', False)),
                    managed_by_bugcrowd=str(program_data.get('managed_by_bugcrowd', False)),
                    safe_harbor=program_data.get('safe_harbor'),
                    max_payout=program_data.get('max_payout'),
                    in_scope=in_scope_list,
                    out_of_scope=out_of_scope_list,
                    created_date=datetime.now()
                )
                session.add(new_program)
                inserted_count += 1
        
        session.commit()
        print(f"\n[{current_time()}] Bugcrowd programs saved successfully!")
        print(f"  + Inserted: {inserted_count} new programs")
        print(f"  ~ Updated: {updated_count} existing programs")
        print(f"  ★ Total: {inserted_count + updated_count} programs")
        
        return True
        
    except Exception as e:
        session.rollback()
        print(Fore.RED + f"Error inserting bugcrowd programs: {e}" + Fore.RESET)
        return None
    finally:
        session.close()
