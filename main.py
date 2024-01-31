import click
import subprocess
import platform
import os

oldBranchName = "None"

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


@click.group(help="CLI tool to manage learning branches in your python project.")
def app():
   pass

@click.command(help="Create a new learning branch, install Jupyter Notebook, and create a new Jupyter Notebook file.")
@click.option('--name', '-n' ,prompt='Enter the branch to create', help='The name of the new branch you want to learn for this project')
def learn_more_about_your_project(newBranchName: str):
    """
    Create a new branch, install Jupyter Notebook, and create a new Jupyter Notebook file.

    Args:
        newBranchName (str): The name of the new branch.

    Returns:
        None
    """
    global oldBranchName
    oldBranchName = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "checkout", "-b", "learn"+newBranchName])
    subprocess.run(["pip", "install", "jupyter", "notebook"])
    subprocess.run(["touch", newBranchName+".ipynb"])


@click.command()
@click.option(help='Merge the changes from the learn branch to the main branch')
def merge_the_learn_code():
    """
    Merge the changes from the current branch to the production branch.

    This function checks if the current branch contains the word "learn" in its name.
    If it does, it removes the "learn" prefix from the branch name, uninstalls the "jupyter" and "notebook" packages,
    deletes the corresponding notebook file, checks out the "production" branch, pulls the latest changes from the remote "production" branch,
    merges the changes from the learning branch to the "production" branch, and finally deletes the learning branch.

    If the current branch does not contain the word "learn" in its name, it displays a message indicating that it is not a learning branch.
    """
    global oldBranchName
    if(oldBranchName == "None"):
        click.echo("You are not in learn branch")
        return
    currentBranch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    if("learn" in currentBranch):
        currentBranch = currentBranch[5:]
        subprocess.run(["pip", "uninstall", "jupyter", "notebook"])
        subprocess.run(["rm", currentBranch+".ipynb"])
        try:
            subprocess.run(["git", "checkout", oldBranchName])
        
        except Exception as e:
            click.echo(str(e))
            
        subprocess.run(["git", "pull", "origin", oldBranchName])

        subprocess.run(["git", "merge", "learn"+currentBranch])
        subprocess.run(["git", "branch", "-d", "learn"+currentBranch])
        oldBranchName = "None"
    else:
        click.echo("You are not in a learning branch")
    

app.add_command(learn_more_about_your_project)
app.add_command(merge_the_learn_code)


if __name__ == '__main__':
    app()
