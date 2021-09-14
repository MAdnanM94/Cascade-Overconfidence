from os import environ

SESSION_CONFIGS = [
    dict(
        name='cascade_A1',
        display_name='Cascade Test - Quiz Bank A - 1',
        num_demo_participants=6,
        q_sequence=1,
        app_sequence=['instructions',
                      'control_block',
                      'quiz_block_A1',
                      'quiz_block_A2',
                      'quiz_block_A3',
                      'quiz_block_A4',
                      'final_payment',
                      'payment_info'],
        use_browser_bots=False
    ),
    dict(
        name='cascade_A2',
        display_name='Cascade Test - Quiz Bank A - 2',
        num_demo_participants=6,
        q_sequence=2,
        app_sequence=['instructions',
                      'control_block',
                      'quiz_block_A1',
                      'quiz_block_A2',
                      'quiz_block_A3',
                      'quiz_block_A4',
                      'final_payment',
                      'payment_info'],
        use_browser_bots=False
    ),
    dict(
        name='cascade_B1',
        display_name='Cascade Test - Quiz Bank B - 1',
        num_demo_participants=6,
        q_sequence=1,
        app_sequence=['instructions',
                      'control_block',
                      'quiz_block_B1',
                      'quiz_block_B2',
                      'quiz_block_B3',
                      'quiz_block_B4',
                      'final_payment',
                      'payment_info'],
        use_browser_bots=False
    ),
    dict(
        name='cascade_B2',
        display_name='Cascade Test - Quiz Bank B - 2',
        num_demo_participants=6,
        q_sequence=2,
        app_sequence=['instructions',
                      'control_block',
                      'quiz_block_B1',
                      'quiz_block_B2',
                      'quiz_block_B3',
                      'quiz_block_B4',
                      'final_payment',
                      'payment_info'],
        use_browser_bots=False
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=2.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'c$rnq%mha-d_a_h&crf#qfsmwu5bh#krrcci7m(sjmu!*p5^!9'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# Rooms
ROOMS = [
    dict(
        name='online_lab',
        display_name='OSU Online Experimental Economics Lab',
        #participant_label_file='_rooms/cascade_lab.txt',
        #use_secure_urls=True
    ),
    dict(
        name='econ_lab',
        display_name='OSU Experimental Economics Lab',
        participant_label_file='_rooms/econ_lab.txt',
        use_secure_urls=True
    ),
]
