import random, math

class Poison:
    def __init__(self, level, start, damage, duration, symptoms):
        self.level = level
        self.start = start
        self.damage = damage
        self.duration = duration
        self.symptoms = symptoms
    
    def __str__(self):
        rtn = f'Stufe {self.level}\nBeginn nach {self.start}\n{self.damage} für {self.duration}'
        if len(self.symptoms) > 0:
            rtn += '\nSymptome:'
        for s in self.symptoms:
            rtn += f'\n-{s}'
        return rtn

class Symptom:
    @staticmethod
    def roll_symptom():
        roll = random.randint(1,20)
        log('Gewürfelt: {}'.format(roll))
        if roll <= 4:
            return Symptom('Erbrechen', 'CH')
        if roll <= 6:
            return Symptom('Durchfall / Koliken', 'MU')
        if roll <= 8:
            return Symptom('Schweißausbrüche / Atemnot', 'KO')
        if roll <= 10:
            return Symptom('Schwäche', 'KK')
        if roll <= 12:
            return Symptom('Kopfschmerz / Schwindel', 'KL')
        if roll <= 14:
            return Symptom('Lähmungen', 'GE')
        if roll <= 16:
            return Symptom('Taubheiten', 'FF')
        if roll <= 17:
            return Symptom('Schwellungen', 'GE')
        if roll <= 18:
            return Symptom('Erregung', 'Jähzorn', 1)
        if roll <= 19:
            return Symptom('Blutungen', 'Aberglaube', 1)
        return Symptom('Bewusstlosigkeit', '')
        
    def __init__(self, name, effect, strength_dice=-1):
        self.name = name
        self.effect = effect
        self.strength_dice = strength_dice
    
    def __str__(self):
        return f'{self.name}' \
            + ('' if self.name=='Bewusstlosigkeit' \
            else f': {self.effect} {self.strength_dice}W6')

def log(*args):
    if options.verbose: print(*args)

def parse_arguments():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Spuck enorm viel Holz aus.")
    parser.add_option("-o", "--output", dest="filename", default=None, help="Der Speicherort für die Ausgabe. Standard ist stdout.")
    parser.add_option("-x", "--seed", dest="seed", default=None, help="Setze den Seed manuell.")
    parser.add_option("-l", "--level", dest="level", default=1, help="Die Giftstufe.")
    global options, args
    options, args = parser.parse_args()
    options.level = int(options.level)

def output(arg):
    if options.filename is None:
        print(arg)
        return
    
    log("Opening file:",options.filename)
    with open(options.filename, "w", encoding="utf-8") as outfile:
        outfile.write(str(arg))

if __name__ == '__main__':
    parse_arguments()
    log("Options: ", options)
    if options.level < 1 or options.level > 20:
        raise ValueError('Stufe war: {}\nMuss zwischen 1 und 20 liegen'.format(options.level))
    
    random.seed(options.seed)
    
    dice = math.ceil(options.level / 4.0)
    if 1 <= options.level <= 5:
        start = '1W SR'
        damage = '1W6 pro Stunde'
        duration = '{} Stunden'.format(dice)
    if 6 <= options.level <= 9:
        start = '1 SR'
        damage = '1W6 pro SR'
        duration = '{} SR'.format(dice)
    if 10 <= options.level <= 15:
        start = '1W+4 KR'
        damage = '2W6 pro SR'
        duration = '{} SR'.format(int(dice/2))
    if 16 <= options.level <= 20:
        start = '1W KR'
        damage = '1W6 pro KR'
        duration = '{} KR'.format(dice)
    log(f'Beginn: {start}\nSchaden: {damage}\nDauer: {duration}')
    
    symptoms = []
    log('{} Symptom(e)'.format(math.ceil(options.level/2.0)))
    for i in range(math.ceil(options.level/2.0)):
        symptoms.append(Symptom.roll_symptom())
    log([str(x) for x in symptoms])
    
    p = Poison(options.level, start, damage, duration, symptoms)
    output(p)