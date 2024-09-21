#!/usr/bin/env python3

import os
import markdown
import chevron
#import bs4
import blogpostParser
from dataclasses import dataclass
from feedgen.feed import FeedGenerator
from feedgen.entry import FeedEntry
import tomllib
from typing import Dict, List

TIMESTAMP_STRING: str = 'T12:00:00Z'

@dataclass
class Templates:
    post: str
    category: str
    site: str

def getBlogpostsFromDir(dirOfPosts, template_name: str):
    blogParser = blogpostParser.blogpostParser()
    blogpostList = []

    for filename in os.listdir(dirOfPosts):
        if filename[-3:] == ".md":
            blogpostDict = {}
            blogpostDict['template_name'] = template_name
            fileHandler = open(f"{dirOfPosts}/{filename}",'r',encoding='utf-8')
            lineToParse = fileHandler.readline()
            blogpostDict["body"] = markdown.markdown(fileHandler.read())
            fileHandler.close()

            blogpostDict['filename'] = filename.replace(".md",".html")

            blogpostAttributes = blogParser.splitBlogStringToDict(lineToParse)
            blogpostAttributes["title"] = blogpostAttributes["title"].title()
            blogpostDict.update(blogpostAttributes)

            blogpostList.append(blogpostDict)

    blogpostList.sort(key=lambda postInList: postInList['date'],reverse=True)

    return blogpostList

def generateBlogpostObj(blogpostTemplateLocation,blogpost,include_readmore):
    fileHandler = open(blogpostTemplateLocation,"r")
    blogpostTemplate = fileHandler.read()
    fileHandler.close()

    content = blogpost.copy()
    if include_readmore:
        content["readmore_bar"] = f"<a class=\"readmore\" href=\"/pages/{content["filename"]}\">read more</a>"
    else:
        content["readmore_bar"] = ""

    generatedBlogpost = chevron.render(blogpostTemplate,content)
    blogpostObj = {"post":generatedBlogpost}

    return blogpostObj

def generateBlogPages(dirToWriteTo,blogpostList,templates: Templates,rootURL,feedtitle):

    for blogpostObj in blogpostList:
        templateToUse = templates.__getattribute__(blogpostObj["template_name"])
        blogpost = generateBlogpostObj(templateToUse,blogpostObj,include_readmore=False)
        siteContent = {
        "relativelink":"../",
        "rootURL":rootURL,
        "feedtitle":feedtitle,
        "content":[blogpost],
        "readmore_top":"",
        "readmore_bottom":"",
        }
        siteHtml = generateSite(templates.site,siteContent)
#       parsedSiteHtml = bs4.BeautifulSoup(siteHtml, 'html.parser')

        fileHandler = open(f"{dirToWriteTo}/{blogpostObj['filename']}","w")
#       fileHandler.write(parsedSiteHtml.prettify())
        fileHandler.write(siteHtml)
        fileHandler.close()

def generateAtomFeed(blogposts,rootURL,title):
    feedGen  = FeedGenerator()
    feedGen.title(title)
    feedGen.link(href=f"{rootURL}/atom.xml", rel='alternate')
    feedGen.id(rootURL)
    feedGen.updated(f'{blogpostList[0]["date"]}{TIMESTAMP_STRING}')
    for post in blogpostList:
        atomFeedEntry  = feedGen.add_entry()
        atomFeedEntry.title(post['title'])
        atomFeedEntry.link(href=f'{rootURL}/pages/{post["filename"]}', rel='alternate')
        atomFeedEntry.updated(f'{post["date"]}{TIMESTAMP_STRING}')
        atomFeedEntry.id(f'{rootURL}/pages/{post["filename"]}')
        atomFeedEntry.content(post['body'],type="html")

    return feedGen





def generateSite(siteTemplateLocation,content):
    for i in range(0, len(content["content"])):
        content["content"][i]["post"] = chevron.render(content["content"][i]["post"], content)

    fileHandler = open(siteTemplateLocation,"r")
    siteTemplate = fileHandler.read()
    fileHandler.close()

    generatedSite = chevron.render(siteTemplate,content)

    return generatedSite


READMORE_TOP = """
<details class="readmore">
  <summary class="readmore">
    Read more
  </summary>
"""

READMORE_BOTTOM = """
</details>
"""

if __name__ == "__main__":
    postDir = "posts"
    categoriesDir = "posts/categories"
    dirForPages = "../public_html/pages"
    dirForFeed = "../public_html"
    postTemplate = "templates/blogpost.mustache"
    categoryTemplate = "templates/category.mustache"
    siteTemplate = "templates/site.mustache"

    templates = Templates(post=postTemplate, category=categoryTemplate, site=siteTemplate)

    blogpostList = getBlogpostsFromDir(postDir, "post") + getBlogpostsFromDir(categoriesDir, "category")

    with open("config.toml","rb") as file:
        config = tomllib.load(file)

    rootURL = config.get("rootURL","")
    feedtitle = config.get("title","My Cool Blog")
    feedIncluded = False
    if len(rootURL) > 0:
        feed = generateAtomFeed(blogpostList,rootURL,feedtitle)
        feedIncluded = True
        feed.atom_file(f'{dirForFeed}/atom.xml')

    generateBlogPages(dirForPages,blogpostList,templates,rootURL,feedtitle)

    index_content = {
    "relativelink":"",
    "rootURL":rootURL,
    "feedtitle":feedtitle,
    "content":[],
    "readmore_top":READMORE_TOP,
    "readmore_bottom":READMORE_BOTTOM,
    }
    for post in blogpostList:
        index_content["content"].append(generateBlogpostObj(templates.__getattribute__(post["template_name"]),post,include_readmore=True))

    siteHtml = generateSite(siteTemplate,index_content)
#   parsedSiteHtml = bs4.BeautifulSoup(siteHtml, 'html.parser')

    index_html = open('../public_html/index.html',"w")
#   index_html.write(parsedSiteHtml.prettify())
    index_html.write(siteHtml)
    index_html.close()