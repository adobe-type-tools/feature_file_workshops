/* Copyright 2025 Adobe Systems Incorporated (http://www.adobe.com/). All Rights Reserved.
 * This software is licensed as OpenSource, under the Apache License, Version 2.0.
 * This license is available at: http://opensource.org/licenses/Apache-2.0.
 */

// Python-compatible lexer for feature file validation
// Derived from FeatLexer.g4 with C++ code replaced by Python

lexer grammar FeatLexerPython;
import FeatLexer;

@members {
anon_tag = ""

def verify_anon(self, line):
    """
    Verify anonymous block closing tag matches opening tag.

    All the TSTART/TCHR characters are grouped together, so just
    look for the string and if its there verify that the characters
    on either side are from the appropriate set (in case there are
    "extra" characters).
    """
    try:
        p = line.find(self.anon_tag)
        if p == -1:
            return False
        p -= 1
        if line[p] not in ' \t}':
            return False
        p += len(self.anon_tag) + 1
        if line[p] not in ' \t;':
            return False
        return True
    except (IndexError, AttributeError):
        return False
}

ANON                        : 'anon' -> pushMode(Anon) ;
ANON_v                      : 'anonymous' -> pushMode(Anon) ;

mode Anon;

A_WHITESPACE                : [ \t\r\n]+ -> skip ;
A_LABEL                     : (NAMELABEL | EXTNAME | STRVAL | MARK) { self.anon_tag = self.text } ;
A_LBRACE                    : '{' -> mode(AnonContent) ;

mode AnonContent;

A_CLOSE                     : '\r'? '\n}' [ \t]* (NAMELABEL | EXTNAME | STRVAL | MARK) [ \t]* ';' { self.verify_anon(self.text) }? -> popMode ;
A_LINE                      : '\r'? '\n' ~[\r\n]* ;
