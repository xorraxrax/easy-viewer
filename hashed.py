74c: #!/usr/bin/env python
f6c: import argparse
810: import os
866: import sys
ed6: import urwid
27e: 
57a: PYTHON2=sys.version_info[0] == 2
27e: 
d31: class WheelableListBox(urwid.ListBox):
f52:     def __init__(self, body):
396:         super(WheelableListBox, self).__init__(body)
6f0:         self.default_keypress = urwid.ListBox.keypress
27e: 
38c:     def mouse_event(self, size, event, button, col, row, focus):
78f:         from urwid.util import is_mouse_press
ef6:         if is_mouse_press(event):
dbe:             if button == 5:
95b:                 return super(WheelableListBox, self).keypress(size, 'down')
538:             elif button == 4:
f09:                 return super(WheelableListBox, self).keypress(size, 'up')
27e: 
e6e:         return super(WheelableListBox, self).mouse_event(size, event, button, col, row, focus)
27e: 
27e: 
086: def quit():
9a8:     raise urwid.ExitMainLoop()
27e: 
8fd: def handle_key(key):
1df:     if key in ('q', 'Q', 'esc'):
aac:         quit()
27e: 
45b: def file_contents(filepath):
7b7:     with open(filepath, 'rb') as f:
fe5:         if not PYTHON2:
743:             contents = f.read().decode(encoding='utf-8', errors='ignore')
59c:         else:
25e:             contents = unicode(f.read(), encoding='utf-8', errors='ignore')
27e: 
41f:     return contents
27e: 
dbc: def main():
f00:     palette = [
529:         (None, 'light gray', 'black'),
084:         ('viwer', 'black', 'light gray'),
a41:         ('focus', 'white', 'black', 'standout'),
e30:         ('header', 'yellow', 'black', 'standout'),
ab0:         ('footer', 'light gray', 'black'),
7af:         ('key', 'light cyan', 'black', 'underline'),
ff7:         ('error', 'dark red', 'light gray')
af5:     ]
27e: 
d19:     def button_press(button, user_data=None):
195:         index = choice_path.index(user_data)
be5:         thetitle = choice_text[index]
8c6:         frame.footer = urwid.Text('loading {}'.format(thetitle))
81c:         try:
f8e:             contents = [urwid.Text(x) for x in file_contents(user_data).split('\n')]
39b:             viewer = urwid.AttrWrap(WheelableListBox(urwid.SimpleListWalker(contents)), 'viwer')
8e1:             viewer = urwid.LineBox(viewer, title=thetitle)
b0d:             frame.body = urwid.Columns([ (choice_width,choice_list), ('weight',1,viewer) ], focus_column=1,dividechars=1)
95d:             frame.footer = urwid.Text('loaded {}'.format(thetitle))
219:         except:
7ce:             frame.footer = urwid.Text('Could not read {}: {}'.format(thetitle, sys.exc_info()[0]))
27e: 
27e: 
d6a:     choice_text = []
269:     choice_path = []
6a6:     if args.directory == None and args.files == None and args.title == None:
061:         # No arguments supplied, use current directory.
5b1:         choice_text = [x for x in os.listdir('.') if os.path.isfile(x)]
83b:         choice_path = [x for x in os.listdir('.') if os.path.isfile(x)]
ec9:     elif args.directory:
f87:         # User supplid a directory
111:         dir = args.directory
961:         files = os.listdir(dir)
380:         choice_text = [x for x in files if os.path.isfile(os.path.join(dir, x))]
d8f:         choice_path = [os.path.join(dir, x) for x in files if os.path.isfile(os.path.join(dir, x))]
95d:     elif args.files:
08c:         # A list of files
ae5:         choice_text = [os.path.basename(x) for x in args.files if os.path.isfile(x)]
1c3:         choice_path = [x for x in args.files if os.path.isfile(x)]
99a:     elif args.title:
fc8:         # Pairs of titles and files
415:         choice_text = [x[0] for x in args.title]
25d:         choice_path = [x[1] for x in args.title]
d07:     else:
aac:         quit()
27e: 
413:     choices = []
44d:     for index in range(len(choice_text)):
edd:         choice = urwid.Button(choice_text[index], on_press=button_press, user_data=choice_path[index])
025:         choices.append(choice)
e9c:     header = urwid.AttrWrap(urwid.Text(args.banner), 'header')
61e:     choice_list = WheelableListBox(urwid.SimpleListWalker([header] + choices))
5d6:     choice_width = min(max(len(x) for x in choice_text)+4, 24)
27e: 
a90:     contents = [urwid.Text(x) for x in file_contents(choice_path[0]).split('\n')]
0e7:     viewer = urwid.AttrWrap(WheelableListBox(urwid.SimpleListWalker(contents)), 'viwer')
7d5:     viewer = urwid.LineBox(viewer, title=choice_text[0])
27e: 
555:     panes = urwid.Columns([ (choice_width, choice_list), ('weight',1,viewer) ], focus_column=1,dividechars=1)
c73:     footer = urwid.AttrWrap(urwid.Text(''), 'footer')
ef9:     frame = urwid.Frame(panes, footer=footer)
27e: 
27e: 
dfe:     loop = urwid.MainLoop(frame, palette=palette, unhandled_input=handle_key)
7ae:     loop.run()
27e: 
27e: 
27e: 
f5b: if __name__ == '__main__':
74a:     parser = argparse.ArgumentParser()
9b6:     parser.add_argument('-b', '--banner', default='File Viewer', help='Text to display above the file list')
066:     group = parser.add_mutually_exclusive_group()
e98:     group.add_argument('-t', '--title', action='append', nargs=2, help='Specify a title and file path. Use multiple times to include more than one title,file pair')
978:     group.add_argument('-d', '--directory', help='Specify a directory whose files to view')
6cc:     group.add_argument('-f', '--files', nargs='+', help='Specify a list of files to view')
c48:     args = parser.parse_args()
cc7:     main()

Full md5 hash of: /home/enigma/easy-viewer/viewer.py - 3fb44795f3f984022b4a8b6e03a1e580