from parrot import Parrot
"""py -m pip install git+https://github.com/PrithivirajDamodaran/Parrot_Paraphraser.git"""
parrot = Parrot()
phrases = [
   ('Many of you may be familiar with Python as a programming language,'
    ' but don\'t know much about it')
]

for phrase in phrases:
   print('-'*110)
   print('Input Phrase:', phrase)
   print('-'*110)
   paraphrases = parrot.augment(input_phrase=phrase)
   if paraphrases:
       for paraphrase in paraphrases:
           print(paraphrase)