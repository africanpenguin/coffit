# CoffIT

CoffIT is a _Coffee as a Service (CaaS)_ platform, that focuses on delivering efficient batches of coffee to the IT-CDA-DR (and hopefully not only) department of CERN.


## Overview

This is the backend application that fuels our Coffee service, and eventually our mugs with hot coffee. It is a SocketIO-only service that provides the API to handle all the necessary actions to manage Users, Coffee Batches and whatever you can imagine (even Spanish workers). The service stores all of its data in a RDBMS and keeps no track of user sessions, except for what the `python-socketio` library already does.


## Installation/Deployment

To run the service you have to:

 - Clone the repository and `cd` inside
 - Create a `virtualenv` (or don't, since it's going to be the one and only service that you will ever need and will ship by default along with CentOS 8 in the future!)
 - Run `pip install .[all]`
 - Run `coffit db init`
 - Run `./scripts/gunicorn.sh`

In the future maybe we'll even create a `coffit` python package to make it possible to just `pip install coffit` and live happily ever after.

## See Also...

You can also checkout [CoffIT UI](https://github.com/africanpenguin/coffit-ui), a ReactJS application that serves as our frontend.
