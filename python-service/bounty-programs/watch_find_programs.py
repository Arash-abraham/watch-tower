import requests, json
import subprocess, os , sys

# try:
#     result = subprocess.run(["./sendRequest.sh"], capture_output=True, text=True)
# except PermissionError:
#     os.system('chmod +x sendRequest.sh')


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from db import insert_all_bugcrowd_programs

def RunCode():
    try:
        script_path = "sendRequest.sh"
            
        result = subprocess.run(["bash", script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            
            insert_all_bugcrowd_programs(data)
            
            return data
        else:
            print("error", result.stderr)
            return None
    except PermissionError:
        os.system("chmod +x sendRequest.sh")
        RunCode()

if __name__ == '__main__':
    RunCode()
