import requests , json
import subprocess,os

# try:
#     result = subprocess.run(["./sendRequest.sh"], capture_output=True, text=True)
# except PermissionError:
#     os.system('chmod +x sendRequest.sh')



def RunCode():
    try:
        script_path = "sendRequest.sh"
            
        result = subprocess.run(["bash", script_path], capture_output=True, text=True)
        
        if result.returncode == 0:

            data = json.loads(result.stdout)
            
            print(data)

        else:
            print("error", result.stderr)
            return None
    except PermissionError:
        os.system("chmod +x sendRequest.sh")
        RunCode()

if __name__ == '__main__':
    RunCode()
