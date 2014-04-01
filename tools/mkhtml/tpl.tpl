<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<title>{{ea}}</title>
</head>

<body>

<h2>ii://{{ea}}</h2>

%for m,mo in j:
<hr />
<h3>{{mo.subj}}</h3>
<p>from: {{mo.msgfrom}} ({{mo.addr}}) to: {{mo.msgto}}</p>
<hr />
<p>{{! _escape(mo.msg).replace('\n','<br />')}}</p>
<p align="right">ii://{{m}}</p>
<br /><br /><br />
%end
<hr />


</body></html>
