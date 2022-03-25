import config
import pygame
import os


dir = "Assets/Images"

def LoadAssetNames(direct):
	files = []

	for fileName in os.listdir(direct):
		if "." in fileName:
			if (".png" in fileName or ".jpg" in fileName) and not ".meta" in fileName:
				files.append(fileName)

		else:
			for subFile in LoadAssetNames(direct + "/" + fileName):
				files.append(subFile)

	return files


allFiles = LoadAssetNames(dir)


def LoadAssetImages(direct):
	files = []

	for fileName in os.listdir(direct):
		if "." in fileName:
			if (".png" in fileName or ".jpg" in fileName) and not ".meta" in fileName:
				image = pygame.image.load(os.path.join(direct + "/" + fileName))
				files.append(image)

		else:
			for subFile in LoadAssetImages(direct + "/" + fileName):
				files.append(subFile)

	return files


allFileImages = LoadAssetImages(dir)


def ValidateFileNames(invalidFiles):
	validFiles = []

	for fileIndex in range(0, len(invalidFiles)):
		fileName = invalidFiles[fileIndex].lower()

		letterIndex = 0
		for letter in fileName:
			if letter == ".":
				fileName = fileName[:letterIndex]
			
			letterIndex += 1


		newFileName = ""
		for letter in fileName:
			if letter.isalnum():
				newFileName += letter

		validFiles.append(newFileName)
		
	return validFiles


allNames = ValidateFileNames(allFiles)

SPRITES = {}

for i in range(0, len(allNames)):
	SPRITES[allNames[i]] = allFileImages[i]