# Understanding CI/CD Pipelines

This document provides a comprehensive, step-by-step explanation of what CI/CD is, how it works, why it is crucial in the tech industry, and a deep dive into how it is implemented in this specific project.

---

## 1. The Basics: What is CI/CD?

**CI/CD** stands for **Continuous Integration** and **Continuous Deployment (or Delivery)**.

Think of building a software project like building a car on an assembly line.
- In the old days, developers would build different parts of the car in separate garages for months. When they finally brought all the parts together, they usually didn't fit.
- **CI/CD** is a modern assembly line where every time a developer creates a new part (writes code), it is immediately tested and attached to the car automatically to make sure everything still works.

### Continuous Integration (CI)
Continuous Integration is the practice of automatically integrating code changes from multiple developers into a single shared repository, multiple times a day.
- **Goal:** Catch bugs quickly.
- **How:** Every time a developer pushes code, an automated system builds the application and runs automated tests. If the tests pass, the code is considered "safe." If they fail, the developer is notified immediately.

### Continuous Deployment (CD)
Continuous Deployment takes the code that passed the CI stage and automatically releases it to the real world (production environment).
- **Goal:** Deliver features to users as fast as possible.
- **How:** If the tests pass, the pipeline automatically packages the application and deploys it to a server, app store, or package manager without human intervention.

---

## 2. How it Works on GitHub (GitHub Actions)

GitHub provides a built-in CI/CD service called **GitHub Actions**.

### Key Concepts in GitHub Actions:
1. **Workflows:** A configurable automated process made up of one or more jobs. Workflows are defined by a YAML file inside the `.github/workflows/` directory of your repository.
2. **Events:** Something that triggers a workflow (e.g., pushing code to `main`, opening a Pull Request).
3. **Jobs:** A set of steps that execute on the same runner (server). Jobs can run in parallel or sequentially.
4. **Runners:** The actual servers (usually hosted by GitHub) that execute your code. They can be Linux, macOS, or Windows machines.
5. **Steps:** Individual tasks inside a job (e.g., running a script, installing a dependency).
6. **Actions:** Pre-written reusable scripts that you can include in a step (e.g., an action to set up Python).

---

## 3. Teamwork and Industry Importance

### Why is CI/CD critical in the industry?
- **Speed:** Teams can release new features or bug fixes in minutes rather than weeks.
- **Reliability:** Automated tests ensure that new code doesn't break old features.
- **Reduced Risk:** Releasing small changes frequently is much safer than releasing a massive update once a year.

### How it affects Teamwork:
- **No more "It works on my machine":** Code is tested on a neutral, standardized server. If it fails on the server, it's broken.
- **Fewer Conflicts:** Because developers integrate their code multiple times a day, "merge conflicts" are much smaller and easier to resolve.
- **Confidence:** Developers can write code confidently knowing that the pipeline acts as a safety net to catch mistakes before they reach the users.

---

## 4. The CI/CD Pipeline in This Project

In this `RAG_chatbot` project, the CI/CD pipeline is defined in the `.github/workflows/ci.yml` file. Let's break down exactly what happens every time someone pushes code to the `main` branch.

### The Trigger (Events)
The pipeline is triggered automatically on two events:
- A direct `push` to the `main` branch.
- A `pull_request` targeting the `main` branch.

### Job 1: Lint and Test (The "CI" part)
1. **Setup:** It requests an Ubuntu server (`ubuntu-latest`) and sets up multiple Python versions (3.8 to 3.12).
2. **Install Dependencies:** It runs `pip install` to install all required libraries.
3. **Linting:** It runs `pre-commit run --all-files` to ensure the code formatting is clean and adheres to style guidelines.
4. **Testing:** It runs `pytest` to execute all unit tests. It also checks **Code Coverage** and explicitly enforces that at least 80% of the code must be covered by tests (`--cov-fail-under=80`).
5. **Report:** It uploads the test results to Codecov.

### Job 2: Security Scan
*(Only runs if "Lint and Test" passes)*
- It uses **GitGuardian** to scan the code for hardcoded secrets (like passwords or API keys) and security vulnerabilities.

### Job 3: Build and Package
*(Only runs if "Security Scan" passes)*
- It sets up Python 3.10 and uses standard Python packaging tools (`build`, `twine`) to convert the raw code into a distributable Python package.
- The compiled package is saved as an "artifact" so it can be passed to the next job.

### Job 4: Deploy (The "CD" part)
*(Only runs if "Build and Package" passes AND the branch is `main`)*
- **Where is the CD in this project?** It is located right here in the `deploy` job at the bottom of the `ci.yml` file!
- **What it does:** It downloads the packaged artifact from the previous step and automatically publishes it to **PyPI (Python Package Index)** using an API token stored securely in GitHub Secrets.

---

## 5. Why are the Workflows Failing? (Based on the Notification Screenshot)

In the screenshot provided, there are several failed workflows labeled **"CI Pipeline workflow run failed for main branch"**. 

Given the architecture of the `ci.yml` file, common reasons for failure include:
1. **Failing Tests:** A bug in the code caused `pytest` to fail, or code coverage dropped below the required 80%.
2. **Linting Errors:** The `pre-commit` hook found poorly formatted code (e.g., missing blank lines, unused imports).
3. **Missing GitHub Secrets:** The pipeline requires specific secrets to run successfully:
   - `CODECOV_TOKEN`
   - `GITGUARDIAN_API_KEY`
   - `PYPI_API_TOKEN`
   If these secrets have not been configured in the repository settings (Settings > Secrets and variables > Actions), the pipeline jobs will fail when trying to access them.

*To fix the failing pipelines, you should click on one of the failed runs in the GitHub Actions tab, look at the logs, and identify exactly which step failed.*

---

## 6. How to Set Up CI/CD in a New GitHub Repository

If you want to set up this exact CI/CD pipeline in a brand new repository from scratch, here is how you do it step-by-step:

### Step 1: Create the Workflows Directory
GitHub automatically looks for CI/CD pipelines in a specific folder. 
In the root of your project, create the following directory structure:
```bash
mkdir -p .github/workflows
```

### Step 2: Create the YAML File
Inside the `.github/workflows/` directory, create a new file called `ci.yml`. This file will hold the instructions for your pipeline.
Copy the contents of your pipeline (like the one we have in this project) and paste it into `ci.yml`.

### Step 3: Add the Required Secrets
As mentioned earlier, pipelines often need API keys to talk to third-party services (like PyPI, Codecov, or GitGuardian).
To add these to your GitHub repository:
1. Go to your repository on **GitHub.com**.
2. Click on the **Settings** tab at the top.
3. On the left sidebar, scroll down to **Secrets and variables** and click **Actions**.
4. Click the green **New repository secret** button.
5. Add the name of your secret (e.g., `PYPI_API_TOKEN`) and its value.
6. Repeat for all required secrets.

### Step 3.1: How to Obtain the 3 API Keys Used in This Project

If you are totally new to this, an "API Key" or "Token" is basically a secret password that allows GitHub to log into these 3rd-party websites on your behalf to do its job. **Yes, all three of these services are 100% FREE** for personal or open-source projects!

Here is what they are and how to get their values:

#### 1. `CODECOV_TOKEN` (Codecov)
- **What it is used for:** Codecov tracks how much of your code is covered by automated tests. The CI pipeline runs the tests, and uses this token to send the "report card" to Codecov.com so you can see a nice dashboard of your test coverage.
- **How to get it:**
  1. Go to [codecov.io](https://about.codecov.io/) and sign in with your GitHub account.
  2. Select your repository from the list.
  3. It will immediately show you a "Repository Upload Token". Copy this long string of letters and numbers—this is your `CODECOV_TOKEN`.

#### 2. `GITGUARDIAN_API_KEY` (GitGuardian)
- **What it is used for:** GitGuardian is a security tool. Its job is to scan every line of code you push to GitHub to ensure you didn't accidentally type a real password or API key in your code.
- **How to get it:**
  1. Go to [gitguardian.com](https://www.gitguardian.com/) and sign up for a free account (usually by logging in with GitHub).
  2. Go to your Dashboard, click on **API > Personal Access Tokens** (or look for "API Keys" in settings).
  3. Click **Create new token**, give it a name (like "GitHub Actions"), and copy the key it gives you. This is your `GITGUARDIAN_API_KEY`.

#### 3. `PYPI_API_TOKEN` (PyPI)
- **What it is used for:** PyPI stands for Python Package Index. It's the official global database of Python packages. When you type `pip install something`, it downloads from PyPI. This token allows your GitHub pipeline to automatically upload your finished project to PyPI so others can download it!
- **How to get it:**
  1. Go to [pypi.org](https://pypi.org/) and create a free account.
  2. Click your username in the top right, go to **Account settings**.
  3. Scroll down to the **API tokens** section and click **Add API token**.
  4. Give it a name (e.g., "GitHub Actions Deployment") and set the scope to "Entire account" (or to your specific project if you already created it on PyPI).
  5. Click **Add token** and copy the resulting string (it usually starts with `pypi-`). This is your `PYPI_API_TOKEN`.

### Step 4: Push to GitHub
Now that the `.github/workflows/ci.yml` file is created and the secrets are configured, all you need to do is push your code to the `main` branch.
```bash
git add .github/workflows/ci.yml
git commit -m "Setup CI/CD pipeline"
git push origin main
```
As soon as you push, go to the **Actions** tab on your GitHub repository, and you will see your pipeline automatically start running!
