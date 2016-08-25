#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi

html_opener = """
<!DOCTYPE html>
<html>
    <head>
        <title>Caesar</title>
        <style type="text/css">
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
        <div>
"""

html_closer = """        </div>
    </body>
<html>
"""

ALPHABET_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def alphabet_position(letter):
    alphabet = ALPHABET_LOWERCASE if letter.islower() else ALPHABET_UPPERCASE
    return alphabet.index(letter)

def rotate_char(char, rotation):
    if not char.isalpha():
        return char

    alphabet = ALPHABET_LOWERCASE if char.islower() else ALPHABET_UPPERCASE
    new_pos = (alphabet_position(char) + rotation) % 26
    return alphabet[new_pos]

def encrypt(text, rotation):
    answer = ""
    for char in text:
        answer += rotate_char(char, rotation)
    return answer


class MainHandler(webapp2.RequestHandler):
    def get(self):

        cypher_value = 0
        output = ""

        rotation_html = """
            <p>
                Rotate by:
                <input type="text" name="cypher-value" value="{0}"></input>
            </p>
        """.format(cypher_value)

        textarea_html = """
            <p>
                <textarea name="text">{0}</textarea>
            </p>
        """.format(output)

        submit_html = """
            <p>
                <input type="submit" value="Cypher That Stuff!"></input>
            </p>
        """
        form_html ="""
            <form action="/" method="post">{0}{1}{2}</form>
        """.format(rotation_html, textarea_html, submit_html)

        html = output + html_opener + form_html + html_closer

        self.response.write(html)

    def post(self):

        user_input = self.request.get("text")
        cypher_value = self.request.get("cypher-value")
        cypher_value = int(cypher_value)
        user_input = cgi.escape(user_input, quote=True)

        output = user_input

        rotation_html = """
            <p>
                Rotate by:
                <input type="text" name="cypher-value" value="0"></input>
            </p>
        """

        textarea_html = """
            <p>
                <textarea name="text">{0}</textarea>
            </p>
        """.format(encrypt(output, cypher_value))

        submit_html = """
            <p>
                <input type="submit" value="Cypher That Stuff!"></input>
            </p>
        """
        form_html ="""
            <form action="/" method="post">{0}{1}{2}</form>
        """.format(rotation_html, textarea_html, submit_html)

        html = html_opener + form_html + html_closer

        self.response.write(html)



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
