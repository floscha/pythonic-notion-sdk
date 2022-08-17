# Usage

## Client

### Load the Notion Client

```python
from notion import NotionClient

notion = NotionClient("secret_token")
```

## Pages

### Load a Page

```python
page = client.get_page("some-page-id")
print(page.title)
```

### Edit some property of a Page

```python
page.title = "pythonic-notion-playground-test"
print(page.title)
```
