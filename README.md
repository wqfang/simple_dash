# a simple dash app

Using Render or Railway.

## a few things

- Sad news from Heroku ... :(. [Here are some alternatives](https://www.qovery.com/blog/heroku-discontinue-their-free-tier---what-are-the-top-3-best-alternatives), with a [review](https://nixsanctuary.com/best-paas-backend-hosting-heroku-vs-render-vs-flyio-vs-railwayapp/)
- Using GitHub for your app (cloning on remote instance)
- When running your Dash app

## Environment Setup

1. [Create a environment.yml](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually) file containing the packages you think you'll need (check your `import` statements). **Make sure all your packages (except `pip` and maybe `python=x.x`) are under the `pip:` section.**
   - Update this (manually) as you install more packages. It'll make it easier if you or anyone else ever wants to recreate the environment.
2. Create your environment from the file using `conda env create -f environment.yml`.
3. Everything you install in this environment should be done using pip.
4. Make a requirements file using `pip freeze > requirements.txt`

## Railway

1. Sign up using your GitHub account.
2. Create a new project, only give Railway access to select repositories.
3. Create a new environment in the Dashboard Settings.
4. Select your app (repository) card in the dashboard. Click **Settings**.
5. Change the **Build Command** to `pip install -r requirements.txt`
6. Change the **Start Command** to `python app.py`
7. Share this publicly under **Environment**, and beneath "Domains", select "Generate Domain". (You can edit it this, if your edited version is available.)


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