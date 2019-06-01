# -*- coding: utf-8 -*-
from kibitzr.transformer import transform_factory


HTML = u"""<?xml version="1.0" encoding="utf-8"?>
<html>
    <body>
        <h2 class="header nav">
            <a href="page.html" id="page-link">Page</a>
        </h2>
        <div id="content">
            Привет, Мир!
        </div>
        <div class="footer">
            Footer content
        </div>
    </body>
</html>
"""


def run_transform(key, value, content):
    pipeline = transform_factory({'transform': [{key: value}]})
    return pipeline(True, content)
