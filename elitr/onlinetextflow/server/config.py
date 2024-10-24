path = 'textflow'

port = 5000

host = '127.0.0.1'

auth = {'user': 'elitr', 'pass': 'elitr'}

#menu = ['en', 'asr', 'cs', 'ar', 'az', 'be', 'bg',
#        'bs', 'da', 'de', 'el', 'es', 'et',
#        'fi', 'fr', 'ga', 'he', 'hr', 'hu',
#        'hy', 'is', 'it', 'ka', 'kk', 'lb',
#        'lt', 'lv', 'me', 'mk', 'mt', 'nl',
#        'no', 'pl', 'pt', 'ro', 'ru', 'sk',
#        'sl', 'sq', 'sr', 'sv', 'tr', 'uk',
#        'cs']

#show = "en cs".split()
show = "en cs".split()


all_menu = "ar az be bg bs cs ca da de el es et fi fr ga he hr hu hy is it ka kk lb lt lv me mk mt nb nl nn pl pt ro ru sk sl sq sr_cyrillic sr_latin sv tr uk".split()

menu = show + [a for a in all_menu if a not in show] + ["asr", "zh"]

hide = []

view = ''
