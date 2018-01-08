import os
import re
from pdfrw import PdfReader
import datetime

path = 'C:/Codes/PycharmProjects/Scraps/PDF_Titles/IEEE'
NoneType = type(None)


def renameFileToPDFTitle(path, fileName):

    fullName = os.path.join(path, fileName)
    # Extract pdf title from pdf file
    print(PdfReader(fullName).Info)
    newName = PdfReader(fullName).Info.Title
    print(newName)
    print(type(newName))
    if type(newName) == NoneType:
        timestamp = datetime.datetime.utcnow().strftime("%H-%M-%S-%f")
        newName = 'Untitled' + timestamp
    # Remove surrounding brackets that some pdf titles have
    newName = re.sub('[!@#$/]', '', newName)
    newName = re.sub('[&]', ' and ', newName)
    newName = newName.strip('()') + '.pdf'
    print(newName)
    print(type(newName))
    newFullName = os.path.join(path, newName)
    os.rename(fullName, newFullName)


for fileName in os.listdir(path):
    # Rename only pdf files
    fullName = os.path.join(path, fileName)
    if not os.path.isfile(fullName) or fileName[-4:] != '.pdf':
        continue
    renameFileToPDFTitle(path, fileName)


