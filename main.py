import click
import subprocess
import platform
import os


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
    

def learn_more_about_your_project():
    newBranchName = input("Enter the branch name: ")
    subprocess.run(["git", "checkout", "-b", "learn"+newBranchName])
    subprocess.run(["pip", "install", "jupyter", "notebook"])
    subprocess.run(["touch", newBranchName+".ipynb"])


def merge_to_your_branch():
    currentBranch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()

    if(currentBranch == "production"):
        print("You are in production branch. Please switch to learn branch")
        exit()

    if("learn" in currentBranch):
        currentBranch = currentBranch[5:]

    print("Current Branch: ", currentBranch)


    subprocess.run(["pip", "uninstall", "jupyter", "notebook"])

    # delete the currentBranch.ipynb file
    subprocess.run(["rm", currentBranch+".ipynb"])
    subprocess.run(["git", "checkout", "production"])
    subprocess.run(["git", "pull", "origin", "production"])

    result = subprocess.run(["git", "merge", "learn"+currentBranch])


    print("End of the automation script:    ")


if __name__ == '__main__':
    get_operating_system()
def project_created_for_python():
    """Check if the project is created for python"""
    r = does_system_has_python()
    if(r == "python"):
        return True
    else:
        return False
