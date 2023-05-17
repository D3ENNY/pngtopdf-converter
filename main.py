#!/bin/python

from glob import glob
from sys import exit, argv, stderr
from os import system, getcwd, chdir
from subprocess import check_output, CalledProcessError
    
def dependencies():
    if not checkLibrary():
        choise = input("\033[0;31mATTENZIONE! \033[0m \n vuoi installare le dipendenze necessarie per l'esecuzione del programma?[y/n]").lower()
        try:
            if choise in ['y', 'yes','s','si']:
                system(f'pip install --user -r dependencies/requirements.txt')
                    
            elif choise in ['n','no']:
                print('\033[0;35m operazione annullata\033[0m\n')
                if not checkLibrary(): 
                    print("\033[0;31mnon tutte le dipendenze sono installate\nchiusura del programma in corso \033[0m")
            else:
                print('\033[0;35minput non gestito\nchiusura del programma in corso \033[0m\n')
                exit(1)
        except Exception() as e:
            stderr.write(f"\033[0;31m {str(e)} \033[0m")
            exit(1)

def checkLibrary():
    with open('dependencies/requirements.txt') as file:
        package = file.read().splitlines()
    try:
        for i in package:
            i = i.split('==')
            check_output(['pip', 'show', i[0]])
        return True
    except CalledProcessError:  
        return False  
  
def getFile(path):
    pwd = getcwd()
    chdir(path)
    file = glob('*.png')
    if not file:
        file = glob('*.jpg')
    chdir(pwd)
    return file
        
        
def createPDF(img, dir):
    from img2pdf import convert
    if img:
        outputDir = "output/"
        name = input("\033[0;33minserire il nome del pdf che vuoi creare \033[0m")
        with open(f"{outputDir}{name}.pdf", 'wb') as pdf:
            pdf.write(convert([open(f"{dir}/{f}", "rb") for f in img]))
        print('\033[92mPDF creato con successo!\033[0m')
    else:
        stderr.write("non sono state trovate delle foto")
        
    
        
def main():
    if len(argv) > 1:
        dependencies()
        img = getFile(argv[1]);
        createPDF(img, argv[1])
    else:
        print('\033[0;35mpassare in input la directory con le immagini da convertire! \033[0m')
        exit(1)

    
if __name__ == '__main__':
    main()
    