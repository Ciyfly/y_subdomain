html_head = """ <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">"""

html_title ="""<title>{0}&nbsp;子域名扫描结果</title>"""

html_body_head = """<body bgcolor="#272727">"""

html_body_title = """<h1>{0}&nbsp;子域名扫描结果</h1>"""

html_body_a = """<p><a href="http://{0}" target="_blank">{0}</a></p>"""

html_body_end = """</body>"""

html_style = """<style type="text/css">
a:link,a:visited{
text-decoration:none;  /*超链接无下划线*/
}
h1{
    color: white;
        padding-left: 5%;
        }
        a{
            padding-left: 5%;
            }
            a:link {color: white;}
            a:visited {color:red;}
            body {
                margin: 0;
                    padding: 0;
                    }
                    </style>
                    </html>"""

