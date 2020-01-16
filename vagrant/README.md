These instructions were inspired from the Udacity Full Stack Web Developer Nanodegree Course

INSTALL VIRTUALBOX
VirtualBox is the software that actually runs the virtual machine. 
You can download it from virtualbox.org. 
Install the platform package for your operating system.
You do not need to launch VirtualBox after installing it; Vagrant will do that.

INSTALL VAGRANT
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. 
Download it from vagrantup.com. 
Install the version for your operating system.
If Vagrant is successfully installed, you will be able to run `vagrant --version`   in your terminal to see the version number.

DOWNLOAD THE VM CONFIGURATION
You can either download the VM configuration through Github by forking and cloning the repository: https://github.com/udacity/OAuth2.0
Alternatively, you can extract the zipped folder project submission with the source code for the flask application, a vagrantfile, and a bootstrap.sh file for installing all of the necessary tools.

START THE VIRTUAL MACHINE
From your terminal, navigate to the vagrant subdirectory with the "cd" command and run the command "vagrant up". 
This will cause Vagrant to download the Linux operating system and install it.
When vagrant up is finished running, you will get your shell prompt back. 
At this point, you can run "vagrant ssh" to log in to your newly installed Linux VM!
If you are now looking at a shell prompt that starts with the word vagrant, congratulations — you've gotten logged into your Linux VM.

USING THE FILES
Inside the VM, change directory to /vagrant and look around with ls.
The files you see here are the same as the ones in the vagrant subdirectory on your computer (where you started Vagrant from). 
Any file you create in one will be automatically shared to the other. 
This means that you can edit code in your favorite text editor, and run it inside the VM.
Files in the VM's /vagrant directory are shared with the vagrant folder on your computer, but other data inside the VM is not.

SETTING UP THE DATABASE
Navigate to the catalog folder.
Type "ls" to ensure that you are inside the directory that contains project.py, database_setup.py, two directories named 'templates' and 'static', and other files too.
Run **python database_setup.py** to initialize the database our application will depend on later.
This should create an electronics.db file which has no items within it at the moment.
Next, run **lotsoftech.py** to fill the database with a collection of preset queries I have already made.
If both those commands ran with no errors, that means the database is up and running. 

SEEING THE OUTPUT
Now, run **python project.py** to run the Flask web server.
You can press the Ctrl + C buttons on your keyboard to quit the server at any time.
In your browser, visit **http://localhost:5000** to view the Electronics Catalog app.

ABOUT THE APP
This application is a simple catalog of tech products currently available (similar to what you might see on the Amazon or BestBuy website).
You can navigate to different categories of electronics, such as laptops, phones, etc. on the left column.
The url path reflects which of those categories you are currently viewing.
The homepage (http://localhost:5000 or http://localhost:5000/electronics) lists all the devices currently in the database.
On the right column, you'll see the devices that fall within a selected category.
If you select a device, you will go to a page that displays more information about the device (brand, price, etc.).
Similarly, the name of the device you are viewing along with its database id are reflected in the url path.

If you would like to login to make changes to the devices that are currently known, you can click the login button on the top right at anytime.
This will lead you to a page with two buttons.
The top button is a **Google signin button** that uses Oauth2.0 to log a user in with their Google account.
The bottom button allows the user to **sign out** of their account.
Once signed in, the user is redirected to the homepage and is granted extra permissions, not normally available to the public.
A new button will appear that will allow a user to **add a new device** to the database.
Clicking it will send them to a page where they can set the necessary information to do just that with a form.
Clicking **submit** will add the item to the database and the user is redirected the homepage.
If they scroll down, they will see that their item has been added to the master list of items.
If they navigate to the corrsponding category of electronic, it will also appear there and they can even access an individual device page for it.
Now that they are signed in, the user also has the option of going to a device page to **edit** or **delete** it.
The edit button directs them to a form that they can use to make changes to the data.
The delete button directs them to a page where the user can confirm that they are sure about the change they are about to make. 
Lastly, there is a JSON endpoint at path **/electronics/[electronics_category]/JSON** which will display a jsonified list of the devices within **[electronics_category]**.
