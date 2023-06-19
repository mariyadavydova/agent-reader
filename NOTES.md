The goal of this project is two-fold:

* Support summarization of a large number of various media sources, including web pages, Twitter threads, etc.
* Give a try to various LLMs, available via API (i.e. affordable for hobbyists like me).

## Media sources

* [x] Web pages
* [ ] GitHub projects
* [ ] Arxiv papers annotations
* [ ] Twitter threads
* [ ] Reddit threads
* [ ] YouTube videos (aspirational; it's beyond text summarization)

## LLMs

* [x] GPT-3 from OpenAI
  * Default choice, obviously. Pricing is based on tokens and is very low.
  * The quality of summarization is pretty good. 
  * The only downside is that this API is quite slow. Azure hosting is said to be much faster, 
  but it's out of reach for me ATM.
* [x] Cohere (with LangChain)
  * There is a free tier, which is great. The limit is 5 requests per minute.
  * It looks like it's easy to get a paid tier. The pricing is based on the number of tokens.
  * The quality of summarization in the playground is pretty decent. However, an attempt to use
  their API with LangChain resulted in a very poor quality of summarization.
  * Probably, it's worth trying to use Cohere for summarization directly, without LangChain.
* [ ] Cohere summarization API (without LangChain)
* [ ] Anthropic Claude -- in a waitlist
* [ ] Google PALM 2.0 -- in a waitlist
* [ ] Models from MosaicML -- in a waitlist
  * The promise is that they charge per tokens
* [ ] GPT-3 from Azure -- out of reach now, they only serve enterprise customers
