def write_pages(articls):
    with open('pages.html', 'w') as output:
        html_begin = '''
        <!doctype html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
                <title>Visited pages</title>
            </head>
            <body>
            <table class="table">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">Page</th>
                </tr>
            </thead>
            <tbody>'''
        html_end = '''</tbody></table></body></html>'''
        tb_contet = fill_table(articls)
        print(html_begin + tb_contet + html_end, file=output, end='')
        

def fill_table(articls):
    print('fill_table')
    content = ''
    for counter, articl in enumerate(articls):
        content += '<tr><th scope="row">{0}</th><td><a href="{2}">{1}</a></td></tr>'.format(
            counter, articl[0], articl[1])
    return content
