# Jamf Pro API Sampler

The Jamf Pro API has really improved, though considered a beta. This project demonstrates the key difference between the two APIs: authentication. With the Classic API, every call to the API needed to include a valid username and password. With the Pro API, an API access token is requested once, and then used to authenticate going forward.

The included script, `uapi_demo.py`, shows the new procedure and makes a call to the Jamf Pro API. Your credentials should be entered in the `local_credentials.py` file. Copy `local_credentials_template.py` to `local_credentials.py`, and enter your specific info there. I find this method a bit more secure than entering them directly into main source of your script and can easily be ignored by source code control.

In the future, as I find additional interesting techniques or methods, I'll add them here.

Thanks for stopping by!