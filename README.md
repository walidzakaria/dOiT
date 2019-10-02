# dOiT app
Have you ever tried to find someone near by you who can fix your TV set, or paint your house? Have you tried to look for a specific service in your local town but you failed to find that?! I'm sure you're tried to search on Facebook groups, and tried to ask your friends :wink: .
Do you have another job as a freelancer? Are you encountering a problem to adviertise yourself?
```dOiT application``` is the real solution for both situations :smile:
```dOiT``` is a very simple search engine to shows you all the nearby people who are presenting special services, all what you need is to define your location, and search.
```dOiT``` will do the job for your, it will give you a list of all the people who are nearby you and providing the searched service. It will also sort them as below:
1. Closest to furthest.
2. Highly rated to less rated.
3. People who made this service more regular rather than the others.

## Installation
1. First of all you need to have [Python 3](https://www.python.org/download/releases/3.0/) installed in your machine.
2. Please install the the requirements found in [requirements.txt](https://github.com/walidzakaria/dOiT/blob/master/requirements.txt) You can either manually install them using pip, or if you're using [PyCharm](https://www.jetbrains.com/pycharm/), it will install them automatically.

## Application Running:
Once you run ```python manage.py runserver```, you will have your application running on your local machine.
if you want to see a demo version, please open this [dOiT demo link](https://doit9.herokuapp.com/):

1. When you show the home page it will look like that:

![main page](https://github.com/walidzakaria/dOiT/blob/master/screenshots/01.home.jpg "main")

Usually the application will get your location from the browser if you're running it from PC. If you're running it from a cell phone or tablet, it will take it from your GPS. In case if you don't have GPS or if your browswer doesn't support this function, the application will get your location based on your IP address (*this is not giving an accurate location*).

You still have the option to select your location. ```dOiT``` has the ability to suggest you locations allover the world :smile: :

![search location](https://github.com/walidzakaria/dOiT/blob/master/screenshots/02.change_location.jpg "search location")


2. Since the application knows your location, you can start searching for the service you're looking for (*examples: developer, mechanic, market, tutor, ...etc*).

The results will show according your location, and based on people who scored high rating and did many work for others.

![search list](https://github.com/walidzakaria/dOiT/blob/master/screenshots/03.search_result.jpg "search list")

> the search functionality is still under construction, so the list you see is currently hardcoded for demonstration.


3. You can scroll the results, and if you want to check more details click on the person, this will open more details in the same page:

![search details](https://github.com/walidzakaria/dOiT/blob/master/screenshots/04.search_details.jpg "search details")


4. You can move through the different tabs to see his ```gallery```, or start up the ```deal``` with him, or even click on it to collapse it back and scroll to the next people:

![gallery](https://github.com/walidzakaria/dOiT/blob/master/screenshots/05.person_gallery.jpg "gallery")

![deal](https://github.com/walidzakaria/dOiT/blob/master/screenshots/06.request_deal.jpg "deal").
> this part is still under construction.

When you request a deal, the user should be notified with it, and then he can accept or decline.
If he accepts the deal, he can do the job for your, and once he's done, you can go to your deals, and rate this person. This rating will affect his appearnce order when somebody else looks for the same service.

![rate](https://github.com/walidzakaria/dOiT/blob/master/screenshots/07.rating.jpg "rating").


5. Signup proccess is totally easy, and you need to signup if you need to start a deal with somebody, or if you want to register yourself to provide service:

![login & signup menu](https://github.com/walidzakaria/dOiT/blob/master/screenshots/13.login_form.jpg "login & signup")

![signup form](https://github.com/walidzakaria/dOiT/blob/master/screenshots/08.signup.jpg "signup form").
Once you sign up, you will be logged-in and taken to your profile to fill in more details about yourself, and your activity if you want.

![profile](https://github.com/walidzakaria/dOiT/blob/master/screenshots/09.profile1.jpg "profile")
![profile2](https://github.com/walidzakaria/dOiT/blob/master/screenshots/10.profile2.jpg "profile2")
![profile3](https://github.com/walidzakaria/dOiT/blob/master/screenshots/11.profile3.jpg "profile3")

You can also move to the different pages if you're logged-in:

![logged-in menu](https://github.com/walidzakaria/dOiT/blob/master/screenshots/12.user_menu.jpg "logged-in menu")


## Requirements
All the required installations are in [requirements.txt](https://github.com/walidzakaria/dOiT/blob/master/requirements.txt).
