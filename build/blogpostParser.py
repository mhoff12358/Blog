#!/usr/bin/env python3

class blogpostParser:
	def splitBlogStringToDict(self,stringToSplit):
		stringToSplit = stringToSplit.replace(" @","@")
		splitStringList = stringToSplit.split("@")[1:]	#Split by @ and disregard first element (empty string)
		
		blogAttributes = {}
		
		for element in splitStringList:
			key,val = element.partition(" ")[0::2] #Split by first ' ' and disregard separator tuple element
			blogAttributes[key] = val
		return blogAttributes

if __name__ == "__main__":
	exampleString = "@title Example Title @author slimelia @date Today"
	parser = blogpostParser()
	exampleDict = parser.splitBlogStringToDict(exampleString)
	print(exampleDict)
