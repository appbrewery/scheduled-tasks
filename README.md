# Run Your Python Script Daily (Free!)

This template runs your Python script automatically using GitHub Actions.

**No server needed. No credit card. Completely free.**

---

## Setup Instructions

### Step 1: Create Your Own Copy

**<img width="1529" height="392" alt="image" src="https://github.com/user-attachments/assets/ad18c370-5d54-4cf0-aebf-4826c3928281" />
**

- Click the **"fork"** button at the top of this page

You now have your own copy to edit!

### Step 2: Enable the Github Action Workflows

The workflows I created for you will be disabled automatically on your copy. You have to enable them. 

- Click the green button **"I understand my workflows etc etc"**
 
<img width="834" height="349" alt="image" src="https://github.com/user-attachments/assets/296570ac-3800-40d6-9585-d501538cfc8c" />

Obviously one should always (!) check before running random stuff on the internet ;) 
And of course, once checked, the workflows need to be enabled:

<img width="1547" height="895" alt="image" src="https://github.com/user-attachments/assets/d7fbd3c7-0215-44f8-bba7-8c04c3447b5a" />


---

### Step 3: Add Your Code

#### 3a. Copy your Python files

Upload or copy-paste your Python code into `main.py`

If you have other files your script needs (like `.csv` files or `.txt` templates),
add those to the repository too.

#### 3b. Make these two small changes to your code:

**Change 1:** Add this import at the top of your file:

```python
import os
```

**Change 2:** Replace any hardcoded passwords/API keys with this pattern:

```python
# BEFORE (don't do this - secrets visible to everyone!)
MY_EMAIL = "myemail@gmail.com"
MY_PASSWORD = "mysecretpassword"

# AFTER (secrets stored securely in GitHub)
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
```

#### 3c. Add your dependencies

Open `requirements.txt` and list any packages your script needs:

```python
# For example:
pandas
requests
```

---

### Step 4: Add Your Secrets

**Never put passwords or API keys directly in your code!**

GitHub Secrets keeps them safe and hidden.

1. Go to your repository on GitHub
2. Click **Settings** (top menu bar)
3. Click **Secrets and variables** (left sidebar)
4. Click **Actions**
5. Click **"New repository secret"**
6. Add each secret your script needs:

| Name          | Value                               |
| ------------- | ----------------------------------- |
| `MY_EMAIL`    | your email address                  |
| `MY_PASSWORD` | your email password or app password |

> **Gmail Users:** You need an "App Password", not your regular password.
> Get one here: https://myaccount.google.com/apppasswords

---

### Step 5: Set Your Schedule

Edit the file `.github/workflows/scheduled.yml`

Find this line near the top:

```yaml
- cron: "0 9 * * *"
```

Change the numbers to set your schedule:

```
         ┌─ minute (0-59)
         │  ┌─ hour (0-23) in UTC time
         │  │
    cron: '0 9 * * *'   means "run at 9:00 AM UTC every day"
```

**Common schedules:**
| What you want | Cron to use |
|--------------|-------------|
| 9:00 AM UTC | `'0 9 * * *'` |
| 2:30 PM UTC | `'30 14 * * *'` |
| Midnight UTC | `'0 0 * * *'` |
| 6:00 PM UTC | `'0 18 * * *'` |

**Convert your local time to UTC:** https://time.is/UTC

---

### Step 6: Test Your Setup

1. Go to the **Actions** tab in your repository
2. Click **"Test Setup"** in the left sidebar
3. Click **"Run workflow"** → **"Run workflow"**

This checks that:
- Your secrets are configured
- All required files exist
- Your Python code has no syntax errors

If everything passes, you're ready to go!


### Step 7: Run Your Script

Once the test passes, try running your actual script:

1. Go to the **Actions** tab
2. Click **"Daily Script"** in the left sidebar
3. Click **"Run workflow"** → **"Run workflow"**

Watch it run! Click on the job to see the output.

- Pro tip: it is useful to fail a run so that you can see what happens. There is no Console as such, so it can be confusing when a problem occurs. One common issue I've seen in the Q&A, for example, is forgetting to put the SMTP port number in the connection. 

<img width="1509" height="1096" alt="image" src="https://github.com/user-attachments/assets/3f5e7fea-e1a5-4f90-afd6-8a695af7f529" />


---

## Checking If Your Script Ran

1. Go to the **Actions** tab
2. You'll see a list of all runs with green (success) or red (failed)
3. Click on any run to see details
4. Click on **"run"** to expand and see your script's output

---

## Troubleshooting

### "My script isn't running on schedule"

- GitHub schedules can be delayed by 5-15 minutes (this is normal)
- Your repository must have activity every 60 days, or GitHub pauses the schedule
- Fix: Make any small commit to re-enable it

### "Error: No module named 'pandas'" (or other package)

- Add the missing package to `requirements.txt`
- Make sure spelling matches exactly (case-sensitive)

### "My secrets aren't working"

- Secret names are case-sensitive: `MY_EMAIL` is different from `my_email`
- In your code, use the exact same name: `os.environ.get("MY_EMAIL")`
- In the workflow file, the secret must be passed to the script (already done in template)

### "Email not sending"

- Gmail requires an **App Password**, not your regular password
- Check that "Less secure apps" is enabled (some providers)
- Check the Actions log for error messages

---

## Time Zone Reference

To run at 9:00 AM in your local time, use this hour in UTC:

| Your Location         | UTC Offset | Hour to use         |
| --------------------- | ---------- | ------------------- |
| London (GMT/BST)      | +0 / +1    | 9 or 8              |
| Paris, Berlin (CET)   | +1         | 8                   |
| New York (EST/EDT)    | -5 / -4    | 14 or 13            |
| Chicago (CST/CDT)     | -6 / -5    | 15 or 14            |
| Denver (MST/MDT)      | -7 / -6    | 16 or 15            |
| Los Angeles (PST/PDT) | -8 / -7    | 17 or 16            |
| Sydney (AEST/AEDT)    | +10 / +11  | 23 or 22 (prev day) |
| Tokyo (JST)           | +9         | 0 (midnight)        |
| India (IST)           | +5:30      | 3 (minute: 30)      |

_Two values shown for locations with daylight saving time_

---
