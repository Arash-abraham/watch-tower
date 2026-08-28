# MySql or Mongo ? I using Mongo
# Database -> watch-tower 
# Collections : programs , subdomains , bugcrowd_programs , etc ...
# Programs -> 
    # - program_name 
    # - scopes 
    # - out-scope 
    # - created_at
    # - updated_at 


from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os
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

# MongoDB connection URI
MONGO_URI = f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/"
client = MongoClient(MONGO_URI)
db = client[db_name]

def check_and_create_database():
    try:
        # Check if database exists by listing databases
        existing_dbs = client.list_database_names()
        
        if db_name in existing_dbs:
            return 'Exist'
        else:
            create = input(f"Do you want the database '{db_name}' to be created (y/n) : ")
            
            if create.lower() == 'y':
                # In MongoDB, database is created automatically when you insert data
                # Just create a temporary collection to force creation
                db.create_collection("_temp")
                db.drop_collection("_temp")
                return 'Exist'
            else:
                return 'NoExist'
                    
    except Exception as e:
        return e
    except KeyboardInterrupt:
        sys.exit(1)

def upsert_program(program_name, scopes, outScopes, config_data):
    if scopes is None:
        scopes = []
    if outScopes is None:
        outScopes = []
    if config_data is None:
        config_data = {}
    
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
    
    # ============================================================
        # Changes made:
        # The line below, which was responsible for creating the tables, has been commented out
        # because the table structure is to be managed by Laravel
        # Python is only responsible for inserting and updating data
    # ============================================================

    # No need for metadata.create_all in MongoDB
    
    try:
        programs_collection = db['programs']
        
        # Find existing program
        program = programs_collection.find_one({'program_name': program_name})
        
        if program:
            old_scopes = set(program.get('scopes', []))
            old_outScopes = set(program.get('outScopes', []))
            
            new_scopes = set(scopes)
            new_outScopes = set(outScopes)
            
            # Update the document
            programs_collection.update_one(
                {'program_name': program_name},
                {'$set': {
                    'scopes': scopes,
                    'outScopes': outScopes,
                    'config': config_data,
                    'last_update': datetime.now()
                }}
            )
            
            added_scopes = new_scopes - old_scopes
            removed_scopes = old_scopes - new_scopes
            added_outScopes = new_outScopes - old_outScopes
            removed_outScopes = old_outScopes - new_outScopes
            
            print(f"[{current_time()}] Updated program: {program_name}")
            
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
            new_program = {
                'program_name': program_name,
                'created_date': datetime.now(),
                'last_update': datetime.now(),
                'config': config_data,
                'scopes': scopes,
                'outScopes': outScopes
            }
            programs_collection.insert_one(new_program)
            print(f"[{current_time()}] Inserted new program: {program_name}")
            print(f"  Scopes: {scopes}")
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def insert_all_bugcrowd_programs(all_data):
    db_status = check_and_create_database()
    if db_status != 'Exist':
        if db_status == 'NoExist':
            print('To use the program with a specified name in env, create a database for the database.')
            sys.exit(1)
        else:
            print(Fore.WHITE + 'We have a problem! ' + Fore.RED + f'\n{db_status}')
            sys.exit(1)
    
    # ============================================================
        # Changes made:
        # The line below, which was responsible for creating the tables, has been commented out
        # because the table structure is to be managed by Laravel
        # Python is only responsible for inserting and updating data
    # ============================================================
    
    # No need for metadata.create_all in MongoDB
    
    bugcrowd_collection = db['bugcrowd_programs']
    
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
            
            existing = bugcrowd_collection.find_one({'program_name': program_name})
            
            if existing:
                bugcrowd_collection.update_one(
                    {'program_name': program_name},
                    {'$set': {
                        'program_url': program_data.get('url'),
                        'allows_disclosure': str(program_data.get('allows_disclosure', False)),
                        'managed_by_bugcrowd': str(program_data.get('managed_by_bugcrowd', False)),
                        'safe_harbor': program_data.get('safe_harbor'),
                        'max_payout': program_data.get('max_payout'),
                        'in_scope': in_scope_list,
                        'out_of_scope': out_of_scope_list,
                        'last_update': datetime.now()
                    }}
                )
                updated_count += 1
            else:
                new_program = {
                    'program_name': program_name,
                    'program_url': program_data.get('url'),
                    'allows_disclosure': str(program_data.get('allows_disclosure', False)),
                    'managed_by_bugcrowd': str(program_data.get('managed_by_bugcrowd', False)),
                    'safe_harbor': program_data.get('safe_harbor'),
                    'max_payout': program_data.get('max_payout'),
                    'in_scope': in_scope_list,
                    'out_of_scope': out_of_scope_list,
                    'created_date': datetime.now(),
                    'last_update': datetime.now()
                }
                bugcrowd_collection.insert_one(new_program)
                inserted_count += 1
        
        print(f"\n[{current_time()}] Bugcrowd programs saved successfully!")
        print(f"  + Inserted: {inserted_count} new programs")
        print(f"  ~ Updated: {updated_count} existing programs")
        print(f"  ★ Total: {inserted_count + updated_count} programs")
        
        return True
        
    except Exception as e:
        print(Fore.RED + f"Error inserting bugcrowd programs: {e}" + Fore.RESET)
        return None

def current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")