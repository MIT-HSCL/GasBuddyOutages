# GasBuddyOutages
Script to consolidate GasBuddy data during a disruption

09.06.21
## Copy the GasBuddy Data
To sync to an AWS S3 Bucket you need to use the AWS CLI (Command Line Interface).
https://docs.aws.amazon.com/cli/index.html

After you have installed the AWS CLI, you can list the folders you want using
$ aws s3 ls "s3://bucket-name/key-name"

For GasBuddy the bucket-name is "hurricane.gasbuddy.io". There are many folders in that directory.

To list the available data currently being shared by Gas Buddy
```
$ aws s3 ls s3://hurricane.gasbuddy.io
```

To copy a version of the available file you need to use the sync command.
```
$ aws s3 sync "s3://hurricane.gasbuddy.io/Hurricane Ida 2021 Outages/" Hurricane_Ida_Outages --no-sign-request
```

This will copy all of the sub-folders and files from the Ida folder. Before you start, you need to install the requirements to run your python program.

## Install all requirements
(preferably in a virtual environment)

Make sure you have Python 3.8+ installed on your system. You can download it [here](https://www.python.org/downloads/).

### Set up a Virtual Environment
(Optional) Set up a virtual environment:
  If you are using `virtualenv`, you can create a new environment based on Python 3.8.x:
  ```sh
  virtualenv -p python3 venv
  ```
  Where `venv` is the directory name to place the new virtual environment.

  Then, you must activate it:
  ```sh
  source venv/bin/activate
  ```

  In Windows this can be sourced by typing:
  ```sh
  venv\Scripts\activate
  ```

### Install the required packages
  While in the project root and virtualenv:
  ```
  pip install -r requirements.txt
  ```

<hr/>



### To make a gif of images:
https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
Use imageio, which was developed to solve this problem and more, and is intended to stay.

Quick and dirty solution:

import imageio
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('/path/to/movie.gif', images)

### To make a gif in Tableau:
https://towardsdatascience.com/how-to-render-your-tableau-viz-as-a-gif-file-b0a11ed6acf9
