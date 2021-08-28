"""
Defines the dict data structure which contains the actual content for the home page which act as a CV
"""
import os
import math
import datetime

from django.conf import settings


def static_url(relative_path: str) -> str:
    return os.path.join(settings.STATIC_URL, relative_path)


BIRTHDAY = datetime.datetime(1998, 4, 26, 0, 0, 0, 0)


def get_age():
    today = datetime.datetime.now()
    timedelta = today - BIRTHDAY
    delta_days = timedelta.days
    delta_years = math.floor(delta_days / (365 * 12))
    return delta_years


CV = {
    'profile': {
        'about_me': (
            'Currently, I am a student of electrical engineering with a primary focus on control systems engineering '
            'at the Karlsruhe Institute of Technology. Besides university, I also do part time programming. My main '
            'area of expertise is the python programming language, where I have dipped my toes into all sorts of '
            'domains such as command line applications, GUIs, machine learning, optimization algorithms, game and web '
            'development. Nowadays I mainly find myself tinkering with the web, but my heart is with all things '
            'electronic.'
        ),
        'image_url': static_url('images/profile_picture.jpg'),
        'name': 'Jonas Teufel',
        'age': f'{get_age()} years',
        'location': 'Karlsruhe, Germany'
    },
    'education': [
        {
            'title': 'Higher School Certificate (German Abitur)',
            'subtitle': 'final grade: <em>1,2</em>',
            'description': (
                'It was in highschool that I fell in love with science and technology. It started when I chose to '
                'program a game as a one year project for 8th grade. Later on, I elected to graduate in physics and '
                'computer science during the final term.<br>'
                'My personal highlight during school was the opportunity to contribute to the '
                '<em>Schiller in Space</em> project. In this extracurricular project, students had the chance to '
                'collaborate on building the a sensor box, which was flown to the stratosphere to collect climate data.'
            ),
            'image_url': static_url('images/schiller_info.jpg'),
            'image_title': 'Schiller Highschool',
            'from': 'September 2009',
            'to': 'June 2016',
            'links': [
                {'title': 'Schiller Homepage', 'url': 'https://www.schiller-offenburg.de/'},
                {'title': 'Schiller in Space', 'url': ''}
            ]
        },
        {
            'title': 'B.Sc. Electrical Engineering and Information Science',
            'grade': 'final grade: <em>1,9</em> - thesis grade: <em>1,0</em>',
            'description': (
                'The bachelor course taught me a lot about the fundamentals of electrical engineering. I particularly '
                'enjoyed learning about the mathematical theory of signal processing and control systems engineering. '
                'Whenever possible I elected additional computer science courses to learn more about algorithm '
                'engineering and machine learning. <br>'
                'In my bachelors thesis I conducted computation experiments for the '
                'application of a genetic algorithm to the optimization of a heterogeneous and synchronized vehicle '
                'routing and scheduling problem.'
            ),
            'image_url': static_url('images/kit_info.jpeg'),
            'image_title': 'Karlsruhe Institute of Technology',
            'from': 'October 2016',
            'to': 'March 2021',
            'links': [
                {'title': 'KIT Homepage', 'url': 'https://www.kit.edu/english/index.php'},
                {'title': 'Bachelors Thesis', 'url': ''}
            ]
        },
        {
            'title': 'M.Sc. Electrical Engineering and Information Science',
            'description': (
                'I am currently studying for my masters degree in electrical engineering with a specialization in '
                'control systems engineering.'
            ),
            'image_url': static_url('images/kit_info.jpeg'),
            'image_title': 'Karlsruhe Institute of Technology',
            'from': 'April 2021',
            'to': 'Ongoing',
            'links': [
                {'title': 'KIT Homepage', 'url': 'https://www.kit.edu/english/index.php'}
            ]
        }
    ],
    'experience': [
        {
            'title': 'Part time - Research assistant',
            'description': (
                'At the IPE I had the great opportunity to work on many diverse and interesting projects. Initially, '
                'I mainly worked on web development with PHP and Wordpress. Over the years however I was also involved '
                'in projects which involved machine learning, C development of a custom linux interface for scientific '
                'high-speed cameras and the development of Python command line / web applications for a continuous '
                'testing platform for camera hardware developed at the IPE.'
            ),
            'image_url': static_url('images/ipe.jpg'),
            'image_title': 'Institute for data processing and electronics (IPE)',
            'from': 'August 2017',
            'to': 'Ongoing',
            'links': [
                {'title': 'IPE Homepage', 'url': 'https://www.ipe.kit.edu/'}
            ]
        }
    ],
    'abilities': {
        'Programming': [
            [
                {
                    'name': 'Python',
                    'rating': [1, 1, 1, 1, 1],
                    'icon_url': 'https://python.org/static/favicon.ico'
                },
                {
                    'name': 'Click',
                    'rating': [1, 1, 1, 1, 0],
                    'icon_url': static_url('images/favicons/click.ico')
                },
                {
                    'name': 'Django',
                    'rating': [1, 1, 1, 0, 0],
                    'icon_url': static_url('images/favicons/django.ico')
                },
                {
                    'name': 'Flask',
                    'rating': [1, 1, 0, 0, 0],
                    'icon_url': static_url('images/favicons/flask.ico')
                }
            ],
            [
                {
                    'name': 'HTML5',
                    'rating': [1, 1, 1, 1, 0],
                    'icon_url': static_url('images/favicons/html.ico')
                },
                {
                    'name': 'CSS',
                    'rating': [1, 1, 1, 1, 0],
                    'icon_url': static_url('images/favicons/css.ico')
                },
                {
                    'name': 'Javascript',
                    'rating': [1, 1, 1, 0, 0],
                    'icon_url': static_url('images/favicons/js.ico')
                },
                {
                    'name': 'VueJS',
                    'rating': [1, 1, 0, 0, 0],
                    'icon_url': static_url('images/favicons/vue.ico')
                },
                {
                    'name': 'PHP',
                    'rating': [1, 1, 1, 0, 0],
                    'icon_url': static_url('images/favicons/php.ico')
                },
                {
                    'name': 'Wordrpess',
                    'rating': [1, 1, 0, 0, 0],
                    'icon_url': static_url('images/favicons/wordpress.ico')
                }
            ]
        ]
    },
    'projects': [
        {
            'name': 'Schiller in Space',
            'image_url': static_url('images/ipe.jpg')
        },
        {
            'name': 'UcaPhantom',
            'image_url': static_url('images/ipe.jpg')
        },
        {
            'name': 'UfoTest',
            'image_url': static_url('images/ipe.jpg')
        }
    ],
    'contacts': [
        {
            'content': 'jonseb1998@gmail.com',
            'href': '/',
            'image_url': static_url('images/favicons/favicon.ico')
        }
    ]
}
