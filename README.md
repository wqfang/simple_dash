# a simple dash app

Using Railway with a SQL database, and setting up Render. In this tutorial, we'll discuss setting up an app in both Railway and Render, but since Render charges for SQL past 90-days, we will use Railway as the main example platform.

## a few things

- Sad news from Heroku ... they are no longer offering a free product version :(. [Here are some alternatives](https://www.qovery.com/blog/heroku-discontinue-their-free-tier---what-are-the-top-3-best-alternatives), with a [review](https://nixsanctuary.com/best-paas-backend-hosting-heroku-vs-render-vs-flyio-vs-railwayapp/) for each.
- When running your Dash app, make sure it's listening on `host='0.0.0.0'` before pushing it to GitHub.

## Environment Setup

1. [Create a environment.yml](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually) file containing the packages you think you'll need (check your `import` statements). **Make sure all your packages (except `pip` and maybe `python=x.x`) are under the `pip:` section.**
   - See the environment.yml file in this repo as an example.
   - Update this (manually) as you install more packages. It'll make it easier if you or anyone else ever wants to recreate the environment.
2. Create your environment from the file using `conda env create -f environment.yml`.
3. **IMPORTANT: Everything you install in this environment should be done using pip.**
4. Make a requirements file using `pip freeze > requirements.txt`
   - You'll have to **rerun this command each time you install (or re-install) a new package.**
   - This file is referenced by both Render and Railway.

If you like to use JupyterLab (instead of Notebook):

1. In this environment, install ipykernel with `pip install ipykernel`. 
2. Then, give it a kernel specification so that it shows up as a tile in JupyterLab:

   `python -m ipykernel install --user --name <env name> --display-name "<preferred kernel name>"`

*In most cases, it's okay to just let the `<env name>` be the same as the `<preferred kernel name>`.*

## On Git

To build an app in Railway or Render, you'll need your project to be tracked in GitHub. In general, it is highly encouraged that along with an environment, you should **create a git repo for every data science project**. This repository should contain your code, .yml files, requirements.txt files, and sometimes .ipynb files. However it should **not** contain things like API keys, secrets, and in most cases it shouldn't contain any data.

Build a [.gitignore file](https://www.atlassian.com/git/tutorials/saving-changes/gitignore) **before your first commit**. In this file, consider setting git to ignore the files you don't want on GitHub. In the case of this project, there is a *config_vars.json* file that is stored only locally and on a protected GCP VM instance (you can't see it here on GitHub). Similarly, a *data* folder, *model.pickle* file, and a *scratch.ipynb* file are not meant to be saved to GitHub.

Lastly, it is recommended have a separate small Python [package](https://docs.python.org/3/tutorial/modules.html#packages) for project utilities. In this project, we use the *apputil* folder. Consider creating a *scratch.ipynb* file to test code in your project, and make sure this file is ignored in your .gitignore file.

## Render

1. Sign up using GitHub
2. Create a **Web Service**
3. Connect your GitHub Account, but select **only select repositories**
4. Pick your project's app repository.
5. Click **Connect**.
6. Select Python 3 as your Environment.
7. Change the **Start Command** to be `python app.py`
8. On the side bar, select **Environment**, and "Add Environment Variable".
9. Set a key for "PYTHON_VERSION" and its value to be the python version running on your environment. You can check this on your local computer (in the environment) by running `python --version`. You'll need the full 3-decimal version value (e.g., `3.9.15`)

A few things about Render:

- A free SQL database will only last 90 days, then it is deleted.
- To keep from using up too many free credits, you can "**Suspend**" your service in the **Settings** menu of your project's main page (at the bottom).

## Railway

### App Setup

1. Sign up using your GitHub account.
2. Create a new project, only give Railway access to select repositories.
3. Select your app (repository) card in the dashboard. Click **Settings**.
4. Change the **Build Command** to `pip install -r requirements.txt`
5. Change the **Start Command** to `python app.py`
6. Share this publicly under **Environment**, and beneath "Domains", select "Generate Domain". (You can edit it this, if your preferred edited version is available.)

**A few things about Railway:**

- To conserve credits, you can take your app offline by [removing](https://docs.railway.app/deploy/deployments#remove) the most recent deployment.

### SQL Database Setup

1. From the Dashboard, click the **New** button, and select "Database". For this tutorial, we'll be building a Postgres database, so select "Postgres".
2. Select the Postgres card, and then select the "Connect" tab.
3. We'll use the "Postgres Connection URL" for this project. In SQLAlchemy, using `sqlalchemy.create_engine`, connect to the database with `engine = create_engine(<url>)`, where `<url>` is the URL copied from this "Postgres Connection URL" in Railway.
4. Put your initial dataset into a pandas DataFrame, `df`. Then, upload your data to the database with `df.to_sql('table_name', engine)`, where `table_name` is whatever makes sense for this data.
   - You can add to this table pretty easily by adjusting the `if_exists` argument in `to_sql`.
   - You can access data in this *database* using `pd.read_sql`.

### Running Scheduled Jobs

You can schedule CRON jobs using `yarn`, as described in the Railway blog article [here](https://blog.railway.app/p/cron-jobs). For example, the *apputil/data.py* file in this repository could be made into a simple Python script, and run on command.

## Using Environment Variables

**Keys and secret strings should never be pushed to GitHub.** Instead, it's a best practice to use the **environment variable** functionality hosted by the cloud platform being used (e.g., Streamlit, Railway, Heroku, AWS, GCP, etc.). For Railway, declare keys and secrets using the [Railway environment variable functionality](https://docs.railway.app/develop/variables).

On your local computer, there are a few ways to keep references to these variables consistent in your code. For example, you can add all your variables to a *config_vars.json* file, add it to your .gitignore file, and then pull secret variables from this file any time your app is being run locally. But **it is recommended that you use [conda environment variables](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#setting-environment-variables) on your local computer**:

For each new variable you need to use (and protect) in this environment (e.g., an SQL database URL), set a new environment variable with the following code **run in your environment**: `conda env config vars set <variable>=<value>`
   - When you run this again with the same variable, it will just overwrite the preexisting one.
   - You can remove any environment variable with `conda env config vars unset <variable> -n <env name>`

This should be all you need to do to access environment variables in Python files. However, Jupyter notebooks require one extra step. You need to declare environment variables using the `%env` magic `%env <variable>=<value>`, run at the top of your scratch notebook. **Make sure this notebook is in your .gitignore file**. Alternatively, you can create a **ignored** .env file, and use [dotenv](https://github.com/theskumar/python-dotenv#getting-started) to keep things clean.