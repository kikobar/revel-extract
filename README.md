**Objective**

These Python scripts allow to extract records from the Revel POS system by simulating interactions via the portal. The extracted data is stored as .csv files.

**Requirements**

* Python installed on the machine running this application.
* Credentials for accessing the Revel POS system - you need to request from your administrator for your credentials and URLs.

**How to run this application**

* Copy the file `config-sample.py` to `config.py`.
* Edit `config.py` with your credentials and defaults.
* To extract the orders and payments from the Revel POS, run `python3 login-and-extract-from-revel.py`  - This will download the orders as a .csv file and will request the payment to be sent to the email address in your Revel user.
* To connect to your email, extract the download link and download the payment from Revel, run `python3 extract-from-email.py` - This will download the payments as a .csv file.
