import click
import subprocess


@click.group(help="CLI tool to manage learning branches in your python project.")
def app():
   pass

def save_old_branch_name(name):
    """Save the old branch name to a file."""
    with open('old_branch_name.txt', 'w') as f:
        f.write(name)

def load_old_branch_name():
    """Load the old branch name from a file."""
    try:
        with open('old_branch_name.txt', 'r') as f:
            name = f.read().strip()
            subprocess.run(["rm", "old_branch_name.txt"])
            return name
    except FileNotFoundError:
        return None


@click.command(help="Create a new learning branch, from main branch.")
@click.option('--name', '-n' ,prompt='Enter the branch to create', help='The name of the new branch you want to learn for this project')
def sl(name: str):
    """
    Create a new branch, install Jupyter dependencies, and create a new Jupyter notebook.

    Args:
        name (str): The name of the new branch and Jupyter notebook.

    Returns:
        None
    """
    
    oldBranchName = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    save_old_branch_name(oldBranchName)
    subprocess.run(["git", "checkout", "-b", "learn"+name])
    subprocess.run(["pip", "install", "-r", "jypter.txt"])
    subprocess.run(["touch", name+".ipynb"])



@click.command(help='Merge the changes from the learn branch to the main branch')
def ml():
    """
    Merge the changes from the learn branch to the main branch.

    This command checks if the current branch is a learn branch. If it is, it performs the following steps:
    1. Uninstalls the packages listed in 'jypter.txt' using pip.
    2. Removes the notebook file corresponding to the current branch.
    3. Checks out the old branch name.
    4. Pulls the latest changes from the origin repository for the old branch.
    5. Merges the changes from the learn branch to the old branch.
    6. Deletes the learn branch.

    If the current branch is not a learn branch, it displays a message indicating that the user is not in a learning branch.
    """
    oldBranchName = load_old_branch_name()
    if(oldBranchName == "None"):
        click.echo("You are not in learn branch")
        return
    currentBranch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    if("learn" in currentBranch):
        currentBranch = currentBranch[5:]
        subprocess.run(["pip", "uninstall", "-r", "jypter.txt", "-y"])
        subprocess.run(["rm", currentBranch+".ipynb"])
        try:
            subprocess.run(["git", "checkout", oldBranchName])
        except Exception as e:
            click.echo(str(e))
        subprocess.run(["git", "pull", "origin", oldBranchName])
        subprocess.run(["git", "merge", "learn"+currentBranch])
        subprocess.run(["git", "branch", "-d", "learn"+currentBranch])
    else:
        click.echo("You are not in a learning branch")
    

app.add_command(ml)
app.add_command(sl)


