74c: #!/usr/bin/env python
f6c: import argparse
810: import os
866: import sys
ed6: import urwid
27e: 
f7d: PYTHON2 = sys.version_info[0] == 2
27e: 
27e: 
d31: class WheelableListBox(urwid.ListBox):
bbd:     """ListBox which lets user scroll with mouse wheel."""
f52:     def __init__(self, body):
396:         super(WheelableListBox, self).__init__(body)
6f0:         self.default_keypress = urwid.ListBox.keypress
27e: 
38c:     def mouse_event(self, size, event, button, col, row, focus):
78f:         from urwid.util import is_mouse_press
ef6:         if is_mouse_press(event):
dbe:             if button == 5:
c5f:                 return self.keypress(size, 'down')
538:             elif button == 4:
0c5:                 return self.keypress(size, 'up')
27e: 
e28:         return super(WheelableListBox, self).mouse_event(
260:             size, event, button, col, row, focus)
27e: 
27e: 
1cd: class ActionEditBox(urwid.Edit):
215:     """A box which allows user to hit enter and a function will be called"""
c85:     def __init__(self, callback, caption=''):
11e:         super(ActionEditBox, self).__init__(caption=caption)
cce:         self.callback = callback
27e: 
f89:     def keypress(self, size, key):
7b4:         if key == 'enter':
a05:             self.callback(self._edit_text)
59c:         else:
c55:             super(ActionEditBox, self).keypress(size, key)
27e: 
27e: 
086: def quit():
9e5:     """Terminate program"""
9a8:     raise urwid.ExitMainLoop()
27e: 
27e: 
67a: def intersperse(alist, item):
ef4:     """Insert item between every element of alist"""
da9:     count = len(alist)
2b2:     for index in range(1, count*2-1, 2):
956:         alist.insert(index, item)
6a5:     return alist
27e: 
27e: 
e9d: def search(term=''):
505:     """Highlight matching portions of each line in content"""
eff:     global frame, searchterm
d6f:     searchterm = term
cfb:     if not term:
5e7:         return
7c0:     count = 0
c84:     frame.set_focus('body')
482:     contents = frame.body.contents[1][0].original_widget.original_widget.body
4a9:     for index, text in enumerate(contents):
209:         text, attr = text.get_text()
d11:         if term in text:
ba7:             parts = intersperse(text.split(term), term)
192:             count += len(parts) // 2
a66:             attrs = ('viewer', 'search') * ((len(parts)+1)//2)
fee:             newtext = zip(attrs, parts)
d94:             contents[index] = urwid.Text(newtext)
59c:         else:
951:             contents[index] = urwid.Text([('viewer', text)])
27e: 
e8b:     frame.footer = urwid.Text('{} matches found.'.format(count))
049:     return
27e: 
27e: 
8fd: def handle_key(key):
d7f:     global  frame
ede:     """Handle key presses not handled by any widgets"""
1df:     if key in ('q', 'Q', 'esc'):
aac:         quit()
d3a:     elif key == '/':
77e:         box = ActionEditBox(search, caption='regex: ')
df4:         frame.footer = urwid.AttrWrap(box, 'search')
bd7:         frame.set_focus('footer')
27e: 
27e: 
45b: def file_contents(filepath):
1ad:     """Return the entire contents of a file"""
7b7:     with open(filepath, 'rb') as f:
fe5:         if not PYTHON2:
743:             contents = f.read().decode(encoding='utf-8', errors='ignore')
59c:         else:
25e:             contents = unicode(f.read(), encoding='utf-8', errors='ignore')
27e: 
41f:     return contents
27e: 
27e: 
dbc: def main():
737:     global  header, viewer, panes, footer, frame, searchterm
4f7:     searchterm = ''
f00:     palette = [
529:         (None, 'light gray', 'black'),
ad4:         ('viewer', 'black', 'light gray'),
a41:         ('focus', 'white', 'black', 'standout'),
e30:         ('header', 'yellow', 'black', 'standout'),
ab0:         ('footer', 'light gray', 'black'),
7af:         ('key', 'light cyan', 'black', 'underline'),
2bc:         ('error', 'dark red', 'light gray'),
74f:         ('good', 'dark green', 'black', 'standout'),
59d:         ('search', 'dark red', 'yellow')
af5:     ]
27e: 
d19:     def button_press(button, user_data=None):
634:         """Action when another file is selected, display its content in
151:         viewer"""
30e:         global  viewer, panes, footer, frame, term
195:         index = choice_path.index(user_data)
be5:         thetitle = choice_text[index]
8c6:         frame.footer = urwid.Text('loading {}'.format(thetitle))
81c:         try:
4f4:             lines = file_contents(user_data).replace('\r', '').expandtabs().split('\n')
159:             contents = [urwid.Text(x) for x in lines]
8eb:             viewer = urwid.AttrWrap(WheelableListBox(
bb4:                 urwid.SimpleListWalker(contents)), 'viewer')
8e1:             viewer = urwid.LineBox(viewer, title=thetitle)
332:             frame.body = urwid.Columns([(choice_width, choice_list),
5d4:                                        ('weight', 1, viewer)],
d96:                                        focus_column=1, dividechars=1)
928:             search(searchterm)
b2c:             frame.footer = urwid.AttrWrap(urwid.Text('loaded {}'.format(thetitle)), 'good')
219:         except:
603:             text = 'Could not read {}: {}'
a69:             frame.footer = urwid.AttrWrap(urwid.Text(text.format(thetitle,
39c:                                                    sys.exc_info()[0])), 'error')
27e: 
d6a:     choice_text = []
269:     choice_path = []
ada:     if (args.directory is None and
1c2:         args.files is None and
800:         args.title is None):
061:         # No arguments supplied, use current directory.
5b4:         listing = sorted(os.listdir('.'))
ecd:         choice_text = [x for x in listing if os.path.isfile(x)]
83f:         choice_path = choice_text
ec9:     elif args.directory:
f87:         # User supplid a directory
111:         dir = args.directory
74d:         files = sorted(os.listdir(dir))
d07:         isfile = os.path.isfile
4ce:         choice_text = [x for x in files if isfile(os.path.join(dir, x))]
8d9:         choice_path = [os.path.join(dir, x) for x in
f2f:             files if isfile(os.path.join(dir, x))]
95d:     elif args.files:
08c:         # A list of files
e3e:         files = sorted(args.files)
f12:         choice_text = [os.path.basename(x) for x in
a70:             files if os.path.isfile(x)]
441:         choice_path = [x for x in files if os.path.isfile(x)]
99a:     elif args.title:
fc8:         # Pairs of titles and files
415:         choice_text = [x[0] for x in args.title]
25d:         choice_path = [x[1] for x in args.title]
d07:     else:
aac:         quit()
27e: 
22f:     # Create buttons
413:     choices = []
44d:     for index in range(len(choice_text)):
4ed:         choice = urwid.Button(
bf3:             choice_text[index],
bd0:             on_press=button_press,
55e:             user_data=choice_path[index])
025:         choices.append(choice)
e9c:     header = urwid.AttrWrap(urwid.Text(args.banner), 'header')
61e:     choice_list = WheelableListBox(urwid.SimpleListWalker([header] + choices))
5d6:     choice_width = min(max(len(x) for x in choice_text)+4, 24)
27e: 
d55:     viewer = urwid.AttrWrap(WheelableListBox(urwid.SimpleListWalker([])),
6c0:                             'viewer')
677:     viewerr = urwid.LineBox(viewer, title=choice_text[0])
27e: 
0a2:     panes = urwid.Columns([(choice_width, choice_list), ('weight',1,viewer)],
261:                           focus_column=1,dividechars=1)
c73:     footer = urwid.AttrWrap(urwid.Text(''), 'footer')
ef9:     frame = urwid.Frame(panes, footer=footer)
27e: 
cd3:     button_press(None, choice_path[0])
dfe:     loop = urwid.MainLoop(frame, palette=palette, unhandled_input=handle_key)
7ae:     loop.run()
27e: 
4b0: header, viewer, panes, footer, frame = None, None, None, None, None
27e: 
f5b: if __name__ == '__main__':
74a:     parser = argparse.ArgumentParser()
f14:     parser.add_argument('-b', '--banner', default='File Viewer',
cc1:                         help='Text to display above the file list')
066:     group = parser.add_mutually_exclusive_group()
891:     group.add_argument('-t', '--title', action='append', nargs=2,
36c:                        help='Specify a title and file path. Use multiple times'
a0b:                        ' to include more than one title,file pair')
dc1:     group.add_argument('-d', '--directory',
e4b:                        help='Specify a directory whose files to view')
d6e:     group.add_argument('-f', '--files', nargs='+',
035:                        help='Specify a list of files to view')
c48:     args = parser.parse_args()
cc7:     main()
27e: 

Full md5 hash of: ../easy-viewer/viewer.py - bc7beb3d85815fe43341c112184c7548
