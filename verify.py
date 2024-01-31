import os
import platform
import subprocess

#! I will add all the factors in which are code can be created
def get_operating_system():
    """Get the name of the operating system"""
    os_name = platform.system()
    return os_name



def does_system_has_git():
    """Check if the system has git installed"""
    
    r = subprocess.call(['git', '--version'])

    if(r == 0):
        return "git"
    else:
        os_name = get_operating_system()
        return "No git"



def does_system_has_python():
    r = does_system_has_git()

    if(r == 0):
        t = subprocess.call(['python', '--version'])
        if(t==0):
            return "python"
        else:
            t = subprocess.call(['python3', '--version'])
            if(t==0):
                return "python3"
            else:
                return "No python"
#TODO: I am going to improve this function believe me
def project_created_for_python():
    """Check if the project is created for python"""
    r = does_system_has_python()
    if r == "python":
        # Check all subdirectories in the current directory
        for root, dirs, files in os.walk('.'):
            # If 'python' or 'python3' and 'pip' exist in the 'bin' or 'Scripts' directory, it might be a venv
            if (os.path.exists(os.path.join(root, 'bin', 'python')) or os.path.exists(os.path.join(root, 'bin', 'python3')) or os.path.exists(os.path.join(root, 'Scripts', 'python.exe'))) and os.path.exists(os.path.join(root, 'bin', 'pip')) or os.path.exists(os.path.join(root, 'Scripts', 'pip.exe')):
                return True
    return False

def create_project():
    """a virtual environment is equivalent to a project"""
    r = does_system_has_python()
    if(r == "python"):
        subprocess.call(['python', '-m', 'venv', '.venv'])
    else:
        # Need to improve too much here
        subprocess.call(['python3', '-m', 'venv', '.venv'])

def activate_project():
    """Activate the virtual environment"""
    r = does_system_has_python()
    if(r == "python"):
        subprocess.call(['.venv/bin/activate'])
    else:
        # Need to improve too much here
        subprocess.call(['.venv/Scripts/activate'])

