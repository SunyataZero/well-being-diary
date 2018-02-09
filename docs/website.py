
prefix_str = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/html">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Mindfulness at the Computer</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="shortcut icon" type="image/x-icon" href="favicon.ico">
</head>
<body class="center-div">
<div class="header">
    <a class="title" href=".">Mindfulness at the Computer</a>
    <br>
    <div class="navbar">
        <a href=".">Main</a>
        <a href="screenshots.html">Screenshots</a>
        <a href="downloads.html">Downloads</a>
        <a href="user-guide.html">User Guide</a>
        <a href="participate.html">Participate</a>
    </div>
</div>
"""

suffix_str = """
</body>
</html>"""

home_str = prefix_str + "<h1>Well-being Practice Journal</h1>" + suffix_str
user_guide_str = prefix_str + "<h1>User Guide</h1>" + suffix_str

with open("index.html", "w") as text_file:
    text_file.write(home_str)

with open("user_guide.html", "w") as text_file:
    text_file.write(user_guide_str)
