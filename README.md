# Create an environment and install the requirements for the first time
. conda create --name mydashenv python=3.6
. conda activate mydashenv
. pip install -r requirements.txt

# Load the environment created
. conda activate mydashenv
. conda deactivate