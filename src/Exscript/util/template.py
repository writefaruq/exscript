# Copyright (C) 2007 Samuel Abels, http://debain.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from Exscript             import stdlib
from Exscript.Interpreter import Parser

def _builtin_vars(conn = None, filename = 'undefined'):
    hostname = conn and conn.get_host().get_address() or 'undefined'
    builtin  = dict(__filename__   = [filename],
                    __hostname__   = [hostname],
                    __connection__ = conn)
    return builtin

def _compile(template, parser_kwargs, **kwargs):
    # Init the parser and compile the template.
    parser = Parser(**parser_kwargs)
    parser.define_object(**kwargs)
    parser.define_object(**stdlib.functions)
    return parser.parse(template)

def _run(conn, template, parser_kwargs, **kwargs):
    compiled = _compile(template, parser_kwargs, **kwargs)
    return compiled.execute()

def test(string, **kwargs):
    """
    Compiles the given template, and raises an exception if that
    failed. Does nothing otherwise.

    @type  string: string
    @param string: The template to compile.
    @type  kwargs: dict
    @param kwargs: Variables to define in the template.
    """
    kwargs.update(_builtin_vars())
    _compile(string, {}, **kwargs)

def test_file(filename, **kwargs):
    """
    Convenience wrapper around test() that reads the template from a file
    instead.

    @type  filename: string
    @param filename: The name of the template file.
    @type  kwargs: dict
    @param kwargs: Variables to define in the template.
    """
    kwargs.update(_builtin_vars())
    _compile(string, {}, **kwargs)

def eval(conn, string, strip_command = True, **kwargs):
    """
    Compiles the given template and executes it on the given
    connection.
    Raises an exception if the compilation fails.

    if strip_command is True, the first line of each response that is
    received after any command sent by the template is stripped. For
    example, consider the following template::

        ls -1{extract /(\S+)/ as filenames}
        {loop filenames as filename}
            touch $filename
        {end}

    If strip_command is False, the response, (and hence, the `filenames'
    variable) contains the following::

        ls -1
        myfile
        myfile2
        [...]

    By setting strip_command to True, the first line is ommitted.

    @type  conn: Connection
    @param conn: The connection on which to run the template.
    @type  string: string
    @param string: The template to compile.
    @type  strip_command: bool
    @param strip_command: Whether to strip the command echo from the response.
    @type  kwargs: dict
    @param kwargs: Variables to define in the template.
    @rtype:  dict
    @return: The variables that are defined after execution of the script.
    """
    kwargs.update(_builtin_vars(conn))
    return _run(conn, string, {'strip_command': strip_command}, **kwargs)

def eval_file(conn, filename, strip_command = True, **kwargs):
    """
    Convenience wrapper around eval() that reads the template from a file
    instead.

    @type  conn: Connection
    @param conn: The connection on which to run the template.
    @type  filename: string
    @param filename: The name of the template file.
    @type  strip_command: bool
    @param strip_command: Whether to strip the command echo from the response.
    @type  kwargs: dict
    @param kwargs: Variables to define in the template.
    """
    kwargs.update(_builtin_vars(conn, filename))
    template = open(filename, 'r').read()
    return _run(conn, template, {'strip_command': strip_command}, **kwargs)

def paste(conn, string, **kwargs):
    """
    Compiles the given template and executes it on the given
    connection. This function differs from eval() such that it does not
    wait for a prompt after sending each command to the connected host.
    That means that the script can no longer read the response of the
    host, making commands such as `extract' or `set_prompt' useless.

    The function raises an exception if the compilation fails, or if
    the template contains a command that requires a response from the
    host.

    @type  conn: Connection
    @param conn: The connection on which to run the template.
    @type  string: string
    @param string: The template to compile.
    @type  kwargs: dict
    @param kwargs: Variables to define in the template.
    @rtype:  dict
    @return: The variables that are defined after execution of the script.
    """
    kwargs.update(_builtin_vars(conn))
    return _run(conn, string, {'no_prompt': True}, **kwargs)

def paste_file(conn, filename, **kwargs):
    """
    Convenience wrapper around paste() that reads the template from a file
    instead.

    @type  conn: Connection
    @param conn: The connection on which to run the template.
    @type  filename: string
    @param filename: The name of the template file.
    @type  kwargs: dict
    @param kwargs: Variables to define in the template.
    """
    kwargs.update(_builtin_vars(conn, filename))
    template = open(filename, 'r').read()
    return _run(conn, template, {'no_prompt': True}, **kwargs)
