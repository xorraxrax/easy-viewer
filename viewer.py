#!/usr/bin/env python
#
# Viewer code
#    Copyright (C) 2016 James Johnson
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Viewer website: https://github.com/xorraxrax/easy-viewer

import argparse
import os
import sys
import urwid

PYTHON2 = sys.version_info[0] == 2


class WheelableListBox(urwid.ListBox):
    """ListBox which lets user scroll with mouse wheel."""
    def __init__(self, body):
        super(WheelableListBox, self).__init__(body)
        self.default_keypress = urwid.ListBox.keypress

    def mouse_event(self, size, event, button, col, row, focus):
        from urwid.util import is_mouse_press
        if is_mouse_press(event):
            if button == 5:
                return super(WheelableListBox, self).keypress(size, 'down')
            elif button == 4:
                return super(WheelableListBox, self).keypress(size, 'up')

        return super(WheelableListBox, self).mouse_event(
            size, event, button, col, row, focus)

class SearchBox(urwid.Edit):
    """A box which allows user to hit enter and a function will be called"""
    def __init__(self, callback, caption='search: '):
        super(SearchBox, self).__init__(caption=caption)
        self.callback = callback

    def keypress(self, size, key):
        if key == 'enter':
            self.callback(self._edit_text)
        else:
            super(SearchBox, self).keypress(size, key) 


def quit():
    """Terminate program"""
    raise urwid.ExitMainLoop()


def search(one):
    global frame
    frame.set_focus('body')
    frame.footer = urwid.Text('hello world: {}'.format(one))


def handle_key(key):
    global  frame
    """Handle key presses not handled by any widgets"""
    if key in ('q', 'Q', 'esc'):
        quit()
    elif key == '/':
        box = SearchBox(search, caption='regex: ')
        frame.footer = urwid.AttrWrap(box, 'search')
        frame.set_focus('footer')


def file_contents(filepath):
    """Return the entire contents of a file"""
    with open(filepath, 'rb') as f:
        if not PYTHON2:
            contents = f.read().decode(encoding='utf-8', errors='ignore')
        else:
            contents = unicode(f.read(), encoding='utf-8', errors='ignore')

    return contents


def main():
    global  header, viewer, panes, footer, frame
    palette = [
        (None, 'light gray', 'black'),
        ('viwer', 'black', 'light gray'),
        ('focus', 'white', 'black', 'standout'),
        ('header', 'yellow', 'black', 'standout'),
        ('footer', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('error', 'dark red', 'light gray'),
        ('good', 'dark green', 'black', 'standout'),
        ('search', 'dark red', 'yellow')
    ]

    def button_press(button, user_data=None):
        """Action when another file is selected, display its content in
        viewer"""
        global  viewer, panes, footer, frame
        index = choice_path.index(user_data)
        thetitle = choice_text[index]
        frame.footer = urwid.Text('loading {}'.format(thetitle))
        try:
            lines = file_contents(user_data).split('\n')
            contents = [urwid.Text(x) for x in lines]
            viewer = urwid.AttrWrap(WheelableListBox(
                urwid.SimpleListWalker(contents)), 'viwer')
            viewer = urwid.LineBox(viewer, title=thetitle)
            frame.body = urwid.Columns([(choice_width, choice_list),
                                       ('weight', 1, viewer)],
                                       focus_column=1, dividechars=1)
            frame.footer = urwid.AttrWrap(urwid.Text('loaded {}'.format(thetitle)), 'good')
        except:
            text = 'Could not read {}: {}'
            frame.footer = urwid.AttrWrap(urwid.Text(text).format(thetitle,
                                                   sys.exc_info()[0]), 'error')

    choice_text = []
    choice_path = []
    if (args.directory is None and
        args.files is None and
        args.title is None):
        # No arguments supplied, use current directory.
        choice_text=[x for x in os.listdir('.') if os.path.isfile(x)]
        choice_path=[x for x in os.listdir('.') if os.path.isfile(x)]
    elif args.directory:
        # User supplid a directory
        dir = args.directory
        files = os.listdir(dir)
        choice_text = [x for x in
            files if os.path.isfile(os.path.join(dir, x))]
        choice_path = [os.path.join(dir, x) for x in 
            files if os.path.isfile(os.path.join(dir, x))]
    elif args.files:
        # A list of files
        choice_text = [os.path.basename(x) for x in
            args.files if os.path.isfile(x)]
        choice_path = [x for x in args.files if os.path.isfile(x)]
    elif args.title:
        # Pairs of titles and files
        choice_text = [x[0] for x in args.title]
        choice_path = [x[1] for x in args.title]
    else:
        quit()

    choices = []
    for index in range(len(choice_text)):
        choice = urwid.Button(
            choice_text[index],
            on_press=button_press,
            user_data=choice_path[index])
        choices.append(choice)
    header = urwid.AttrWrap(urwid.Text(args.banner), 'header')
    choice_list = WheelableListBox(urwid.SimpleListWalker([header] + choices))
    choice_width = min(max(len(x) for x in choice_text)+4, 24)

    lines = file_contents(choice_path[0]).split('\n')
    contents = [urwid.Text(x) for x in lines]
    viewer = urwid.AttrWrap(WheelableListBox(urwid.SimpleListWalker(contents)),
                            'viwer')
    viewer = urwid.LineBox(viewer, title=choice_text[0])

    panes = urwid.Columns([(choice_width, choice_list), ('weight',1,viewer)],
                          focus_column=1,dividechars=1)
    footer = urwid.AttrWrap(urwid.Text(''), 'footer')
    frame = urwid.Frame(panes, footer=footer)
    
    
    loop = urwid.MainLoop(frame, palette=palette, unhandled_input=handle_key)
    loop.run()

header, viewer, panes, footer, frame = None, None, None, None, None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--banner', default='File Viewer',
                        help='Text to display above the file list')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--title', action='append', nargs=2, 
                       help='Specify a title and file path. Use multiple times'
                       ' to include more than one title,file pair')
    group.add_argument('-d', '--directory',
                       help='Specify a directory whose files to view')
    group.add_argument('-f', '--files', nargs='+',
                       help='Specify a list of files to view')
    args = parser.parse_args()
    main()

