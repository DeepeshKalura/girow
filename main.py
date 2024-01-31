import click
import subprocess

oldBranchName = "None"


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
