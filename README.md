# Jamf Pro API Sampler

The Jamf Pro API has really improved, though is considered still in beta. This project demonstrates the key difference between the two APIs: authentication. With the Classic API, every call to the API needed to include a valid username and password. With the Pro API, an API access token is requested once for the life of the script, and then used to authenticate going forward.

In the future, as I find additional interesting techniques or methods, I'll add them here.

Thanks for stopping by!



## Included Scripts

##### local_credentials_template.py

Add your specific JAMF server info and rename to local_credentials.py. 

There are many ways of removing sensitive info from a script. I'm not saying this is the best way, but it works for me. Be sure to include it in your .gitignore!



##### uapi_demo.py

This is a bare bones demonstration of how to use the new Pro API token login.



##### jamf_duplicate_detection.py

This is a Pro API rewrite of my Classic API script found here: https://apple.lib.utah.edu/using-the-jamf-pro-api-and-python-to-detect-duplicated-attributes/



##### copy_config_profile.py

This is an experimental script that didn't pan out as well as I had hoped, YMMV. Classic API. Copies config profiles.



##### find_the_jamf_id_of_this_machine.py

Using the classic API, find the JAMF ID of the computer the script is running on. It returns the full computer record, but I just show the ID.



## Author

Todd McDaniel, lazymutt@mac.com



## License

[MIT License](LICENSE)
