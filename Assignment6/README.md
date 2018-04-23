# Ontario Progressive Conservative Leadership Race
I created a Sankey graph and a small multiples bar chart, put them into a Dash
webapp and docorized this. This can be run by cloning the repo and creating
a docker-engine and running:
```
$ eval $(docker-machine env nameOfMachine)
$ docker-compose up --build -d
```

or going to the ip address: <http://165.227.176.9> if it is still running.
This link is something I am paying for and I will take off line in a couple of
months.

Finally, you can run it locally if you have all the dependencies by going to the
directory in terminal and running `$ python app.py`.

This final method is contingent on having the proper libraries installed locally.

## Resources Used:
I used <plot.ly> for information on sankey diagrams and dash as well as [this](https://sladkovm.github.io/webdev/2017/10/16/Deploying-Plotly-Dash-in-a-Docker-Container-on-Digitital-Ocean.html)
link to docerize and put on Digital Ocean.
