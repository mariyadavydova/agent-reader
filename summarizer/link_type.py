from enum import Enum

class LinkType(Enum):
  PROJECT = "project"
  PAPER = "paper"
  TWEET = "tweet"
  REDDIT = "reddit"
  YOUTUBE = "youtube"
  POST = "post"

  @staticmethod
  def get_type_from_link(link):
    if "github.com" in link:
      return LinkType.PROJECT
    elif "arxiv.org" in link:
      return LinkType.PAPER
    elif "twitter.com" in link:
      return LinkType.TWEET
    elif "reddit.com" in link:
      return LinkType.REDDIT
    elif "youtube.com" in link:
      return LinkType.YOUTUBE
    else:
      return LinkType.POST