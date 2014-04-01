<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
%if get('rss'):
    <link rel="alternate" type="application/rss+xml" title="{{r.ea}}" href="/rss/{{r.ea}}">
%end
    <title>{{r.page_title}}</title>
    <link rel="stylesheet" href="/s/css/foundation.min.css" />
    <link rel="stylesheet" href="/s/css/font-awesome.min.css" />
    <link rel="icon" type="image/png" href="/s/favicon.png" />
    <script src="/s/js/vendor/modernizr.js"></script>
    <script src="/s/pretty/run_prettify.js"></script>
  </head>

