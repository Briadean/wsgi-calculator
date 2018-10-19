"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
default = "No Value Set"


def page():
    return"""
        <html>
        <head>
        <title>WSGI Calculator</title>
        </head>
        <body>
        <p>Modify the URL to invoke the add, subtract, multiply and divide functions</p>
        <p>Example: http://localhost8080/divide/12/3</p>
        </body>
        </html>"""


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum = 0
    for arg in args:
        try:
            sum += int(arg)
        except (ValueError, TypeError):
            pass

    return "{}".format(sum)


def subtract(*args):
    """ Returns a string with the difference of the arguments """
    minuend, subtrahend = args

    for arg in args:
        try:
            diff = int(minuend) - int(subtrahend)
        except (ValueError, TypeError):
            pass

    return "{}".format(diff)


def multiply(*args):
    """ Returns a string with the product of the arguments """
    product = 1
    for arg in args:
        try:
            product *= int(arg)
        except (ValueError, TypeError):
            pass

    return "{}".format(product)


def division(*args):
    """ Returns a string with the quotient of the arguments """
    dividend, divisor = args
    for arg in args:
        try:
            quotient = int(dividend) / int(divisor)
        except (ValueError, TypeError):
            pass

    return "{}".format(quotient)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {"add": add,
             "subtract": subtract,
             "multiply": multiply,
             "divide": division}

    path = path.strip("/").split("/")
    req_func = path[0]
    args = path[1:]

    try:
        func = funcs[req_func]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):

    path = environ.get('PATH_INFO', None)

    if path == "/":
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        return [page().encode('utf8')]

    func, args = resolve_path(path)
    body = func(*args)

    response_body = ['<h1>Result: {}</h1>'.format(str(func))]
    response_body.extend(['<p>', str(body), '</p>'])
    response_body = '\n'.join(response_body)
    status = '200 OK'

    headers = [('Content-Type', 'text/html'),
               ('Content-Length', str(len(response_body)))]
    start_response(status, headers)

    return [response_body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
