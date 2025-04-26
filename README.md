# llm-document-qna-chatbot-amazon-bedrock
- llm-document-qna-chatbot-amazon-bedrock

### AWS Services
- Amazon Bedrock
  - Fully managed service, offering high-performing foundation models (FMs) including Anthropic. 

### Use Case
- A Q&A chatbot based on documents allows users to get answers to their questions related to the documents.
  
### Prerequisites
- Conda
  -  Can be installed via Miniconda installer which is a lightweight version of the Anaconda Distribution installer that only provides conda, its dependencies, and a few other select packages.
  -  Added naconda3 to my PATH environment variable
- Visual Studio Code (GitHub Copilot integrated)
- AWS account (Root user)

### Set up
Visual Studio Code
1. Create a virtual environment
  - View > New Terminal > Switch to Command Prompt
    - Navigate to the folder where a virtual environment will be created
    - Run `conda create -p venv python==3.10`
      - Explanation: `-p venv`: to create the environment in the venv directory; relative to my current working directory
2. Activate this environment
  - Run `conda activate venv/`
3. Create a Requirements text file with required libraries
  - File > New Text File
    - enter `boto3` and
      - This is AWS SDK for Python. This is used to interact with AWS services programmatically.
    - enter `awscli` in the next line
      - This is AWS Command Line Interface. This is used to manage AWS servies from the command line.
  - Save as `required_libraries.txt`
4. Install required libraries
  - Run `pip install -r required_libraries.txt`
    - Explanation: `-r` is `--requirement`. It specifies that the argument following this is a requirements file containing a list of dependencies to install.

AWS
1. Create a IAM user
  - AWS Console > Search `IAM`
  - Go to `Users` in the Access management section
  - Click on `Create user`
    - Step 1: Set user name: `testadmin`
    - Step 2: Set permission options: tick `Attach policies directly`
      - Select the policy `AdministratorAccess` (Type: AWS managed - job function)
    - Step 3: Review and create user
2. Create access key
  - IAM > Users > testadmin
  - Click `Create accesss key`
    - Step 1: Select the use case as  `Command Line Interface (CLI)`: to use this access key to enable the AWS CLI to access your AWS account.
    - Step 2: Set description tag as `testkey`. Then, click on `Create access key`
    - Step 3: Retrieve access keys  - For later use, download both `access key` and `secret access key` as .csv file.
    - Copy this access key to configure in VS
      
Visual Studio Code
1. In the Command Prompt, run `aws configure`
  - It will display `File association not found for extension .py` and ask for:
  - AWS Access Key ID: enter the copied access key
  - AWS Secret Access Key: copy it from AWS and paste it here
  - Default region name: enter `us-east-1`
  - Default outputformat: enter `json`

AWS
1. Set Model Access for Amazon Bedrock
  - AWS Console > Search `Amazon Bedrock`
  - Go to `Model access` in the Bedrock configurations section. By default, access is not granted to any of the base models.
    - Note that the availability of models varies across regions.
  - Click on `Enable specific models` - TBC

