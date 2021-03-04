# 28/9/20

Met with rudolph. discussed project and ourselves. He showed us his work pc with 1TB RAM
The project is not to develop a neural network as much but port the application to the MOC, power9 processor and to make the application point and click so that doctors can use it.


# 29/9/20

Met with the team over Discord. Discussed a possible timeline for our project.

Step 1: Take the python inference script out of the terminal and into a GUI so that a human who doesn't know how to use the command line can use it in a "point and click" way. Aim to have this working by the November prototyping window.

Step 2: Port the application so that it works on the MOC. I'm not entirely sure what this means so there will need to be individual research conducted here. I think we need to make it work on Docker so we can put the Docker environment on the MOC

Step 3: Get it working on power9, which means converting it from CISC x86_64 to RISC, whilst still on the MOC. Yeah, IDK either.

Kind of daunting. I guess start on the research and then go from there.

Research topics to go over: 
MOC
Docker
Power9
Making an application for a python script


# 1/10/20

Also need to implement an algorithm that presents the most likely cases at the top of a list

First IDR today..

# 24/2/21

This is my documentation of how to create a new cookiecutter plugin for use with ChRIS, using the information provided here:

https://github.com/FNNDSC/cookiecutter-chrisapp

The machine I am using is Ubuntu 20.10

Start by creating and going into a directory for your plugin

`mkdir sevStack`

sevStack being the stack of ranked severity reports produced by pl-covidnet.

`cookiecutter https://github.com/FNNDSC/cookiecutter-chrisapp.git`

This will give a few options to fill out, and you can fill them out as you see fit. Just make sure the 

`app_repo_name`

option is all lowercase, because when the app goes to Dockerhub, Dockerhub will only accept containers that are lowercase.
When asked

`Select app_type`

I selected

`1 - ds`

because that will create a branch of a tree of nodes.

When asked 

`Select platforms`

`1 - linux/amd64`

`2 - linux/amd64, linux/ppc64le`

`3 - linux/amd64, linux/ppc64le, linux/arm64`

I selected option 3 because we will be porting the app to the MOC which has powerPC architecture, so this will build this for us for free, and #3 has support for Docker if it ever goes to Android.
That should be it! You now have a new plugin.

`ls`

Will show

`pl-sevstack`

Move into the new directory the cookiecutter made for you.

`cd sevstack`

`ls -la`

Will show what cookiecutter populated the directory with, with the name you chose for the app as a new directory within there. This contains

`sevstack.py`

Which is where the code for the plugin lives.

`nano sevstack.py`

To see what is in there. You'll see it includes an example of a bare bones execution.

From the README, there is a command to build the Docker container

`docker build -t local/pl-sevstack .`

If you haven't added your user to the Docker group, you will have to use 

`sudo docker build -t local/pl-sevstack .`

But we can easily add our user to the docker group

`sudo groupadd docker`

`sudo usermod -aG docker $USER`

Restart your machine and then test that you have been added to the docker group and can run without sudo.

`docker run hello-world`

Now build the docker container with the plugin. (Make sure to change back to the directory you were working in)

`docker build -t local/pl-sevstack .`

Now we have a built container, we can go to the README again and find the dummy command to execute. We'll need to create an in and out directory so that the app can actually do something, as well as touch up the dummy command so it works properly.

`mkdir in out`

You'll need to use some sanity checking, like making sure input and output arguments are appropriate, as well as directory paths and whatever you've named your plugin.

`docker run --rm -u $(id -u)                      \ `

`-v $(pwd)/in:/incoming -v $(pwd)/out/:outgoing   \ `

`local/pl-sevstack sevstack                       \ `

`/in /out                                           `

Edit your README under the "Run" heading and save it there so you always have it, then you can copy/paste it in your command line
Since we haven't done anything with 

`sevstack.py`,

Running the container will just print its name and version number to the terminal. We can go ahead and edit it to print

`Hello World` 

by editing this file, so go to your favourite text editor and do just that. Add it under 

`def run(self, options)`

Rebuild using 

`docker build -t local/pl-sevstack .`

And run again using the command you edited in the README and somewhere around the print out of the apps name, you will see your "hello world" message!

Now, building a Docker container is time consuming so an easy way to run the .py file is to run it in a virtual environment.
Create it and activate a virtual environment with

`python3 -m venv ss-env && source ss-env/bin/activate`

Change into the directory with the setup.py file

`cd pl-sevstack`

And to install to your python virtual environment

`pip install -e .`

`sevstack --man`

Shows it has been installed to the environment.

To build the plugin with a debugger, add to the top of sevstack.py under 

`from chrisapp.base import ChrisApp`

`import pudb`

Once you have done that, try to re-install and run

`pip install .`

`sevstack --man`

If you haven't added pudb to requirements.txt, or installed pudb in your virtual environment:

`pip install pudb`

And in requirements.txt, add

`pudb~=2021.1`

So that when you rebuild the container, it will include pudb.

`docker build -t local/pl-sevstack .`

Map your source code live into the container with a new command. I put it in the README with the other command we edited so I can get at it easily. For me it worked best if I copied it out of 

`nano README.rst`

But YMMV

`docker run --rm -u $(id -u)                                                                                            \ `

`-v $(pwd)/sevstack:/usr/local/lib/python3.9/site-packages/sevstack:ro -v $(pwd)/in:/incoming -v $(pwd)/out/:outgoing   \ `

`local/pl-sevstack sevstack                                                                                             \ `

`/in /out                                                                                                                 `      

This command means that you can just run this without rebuilding the container everytime you change the source code :)
Remember pudb? Here's how to run it. Add 

`pudb.set_trace()`

In your source code, where you want a break to happen. Then run the container with the `-ti` flag for interactive mode.

`docker run --rm -u $(id -u) -ti                                                                                        \ `

`-v $(pwd)/sevstack:/usr/local/lib/python3.9/site-packages/sevstack:ro -v $(pwd)/in:/incoming -v $(pwd)/out/:outgoing   \ `

`local/pl-sevstack sevstack                                                                                             \ `

`/in /out                                                                                                                 `

# 25/2/21

Run pudb without error messages by removing the 

`-u $(id -u)`

From the first line of this latest command.

### Automatic builds

First, a repo needs to be initialised for this project. Dockerhub is very particular how to do this. Go to Dockerhub and create an account (if you don't have one), and a repo with the _exact_ name of your cookiecutter project. So in this example

`pl-sevstack`

Link it to a GitHub account that has the same repo name and do the following to upload your code to GitHub and build container images

`cd pl-sevstack`

`git init`

`git add .`

`git commit -m 'First commit'`

`git remote add origin https://github.com/JonoCameron/pl-sevstack.git`

`git push origin master`

`git tag 0.2`

`git push --tags`

This will push your new app to GitHub. Next, push it to Dockerhub:

`docker build -t jonocameron/pl-sevstack:0.2`

`docker push jonocameron/pl-sevstack:0.2`

Then I made it a plugin on the ChRIS store:
https://chrisstore.co/

To automate builds and updates to container images  each time a push is made to GitHub, I followed this guide here:
https://github.com/FNNDSC/cookiecutter-chrisapp/wiki/Automatic-Builds

To add secrets to my GitHub actions.


# 1/3/21

Today I added enabled automatic pushes and builds to dockerhub from github on my plugin.

To do this I added the following secrets to the github repo github.com/JonoCameron/pl-sevstack

`DOCKERHUB_USERNAME`

`DOCKERHUB_PASSWORD`

It also required a re-run of the cookie cutter to select 

`1 - publish to github automatically`

# 2/3/21

Today I will make a plugin that takes an input file 

`in/randomnumbers.txt`

 (in the input directory of the plugin) of randomly generated numbers, tab/comma/new line separated I haven't decided, sorts these numbers and outputs them to the output directory. 

 `out/sortednumbers.txt`

 I will start by populating 

 `in/randomnumbers.txt` 

 with 

 `generaterandom.py`

In the end, I managed to use python IO operations to read the file, and then used numpy to sort the numbers, after a bit of formatting(remove newlines, int(string), etc..) I could not work out how to output to the output directory, and this is something I'm going to follow up with the client on.

# 4/3/21

Today I will get a local instance of ChRIS backend running, so that I can test covidnet.sh.

To run the ChRIS backend with no fuss: https://github.com/FNNDSC/ChRIS_ultron_backEnd/blob/master/README.md

`git clone https://github.com/FNNDSC/ChRIS_ultron_backend`

`./unmake.sh ; sudo rm -fr FS ; rm -fr FS ; ./make.sh`

## Aside into why I was struggling to do python IO operations the other day....

I wasn't mapping inputs and outputs correctly in this command:

`docker run --rm -u $(id -u)                                                                                            \ `

`-v $(pwd)/sevstack:/usr/local/lib/python3.9/site-packages/sevstack:ro -v $(pwd)/in:/incoming -v $(pwd)/out/:outgoing   \ `

`local/pl-sevstack sevstack                                                                                             \ `

`/in /out                                                                                                                 `      

So volume mapping has to be specified as `<hostDir>:<containerDir>` otherwise it won't find the directory it wants outside of the container. The two directories in the last line have to match the directories in the second line.