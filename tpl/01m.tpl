%from api.sx import g_opts, hsh

<nav class="top-bar" data-topbar> 
    <ul class="title-area"> 

        <li class="name"> <h1><a href="/">{{r.ea}}</a></h1> </li> 
        <li class="toggle-topbar menu-icon"><a href="#">Menu</a></li>
    </ul> 
    <section class="top-bar-section"> 
        <!-- Right Nav Section --> 
        <ul class="right"> 
            <li class="divider"></li>

%if r.getl.rev:
<li class="has-form"><a href="/{{r.ea}}{{! g_opts(('lim',r.getl.lim))}}" class="alert button" title="Показать сообщения в обычном стиле"><i class="fa fa-fw fa-sort-numeric-asc"></i></a></li>
%else:
<li><a href="/{{r.ea}}{{! g_opts(('rev','1'),('lim',r.getl.lim))}}" title="Показать сообщения в обратном порядке"><i class="fa fa-fw fa-sort-numeric-desc"></i></a></li>
%end

            <li class="divider"></li>

        <li><a href="/{{r.ea}}{{! g_opts(('rev',r.getl.rev),('lim',r.getl.lim))}}" title="Обновить список сообщений"><i class="fa fa-fw fa-refresh"></i></a>

            <li class="divider"></li>

            <li class="has-dropdown"> <a href="#">
              {{r.ea}}  {{! '<i class="fa fa-fw fa-envelope"></i> %s' % len(j)}}
            </a> 
                <ul class="dropdown"> 
                    <li class="divider"></li>
%for name,cnt in r.echolist:
    <li {{!'class="active"' if r.ea == name else ''}}><a href="/{{name}}">{{name}} <i class="fa fa-fw fa-envelope"></i> {{cnt}}</a></li>
%end
                </ul> 
            </li>
         </ul> 


            <!-- Left Nav Section --> 
        <ul class="left"> 
            <li class="divider"></li>
            <li><a href="/rss/{{r.ea}}" title="RSS-лента"><i class="fa fa-fw fa-rss"></i></a></li>
            <li class="divider"></li>
            <li class="has-form"><a class="button radius" href="/reply/{{r.ea}}/-" title="Написать новое сообщение в эту эху">
                <i class="fa fa-plus-circle"></i> NEW</a>
            </li>
            <li class="divider"></li>
        </ul> 
    </section> 
</nav>
