#!/usr/bin/env python
import argparse
import os
import urwid

def quit():
    raise urwid.ExitMainLoop()

def handle_key(key):
    if key in ('q', 'Q', 'esc'):
        quit()

def file_contents(filepath):
    f = open(filepath)
    contents = f.read()
    f.close()
    return contents

def main():
    palette = [
        (None, 'light gray', 'black'),
        ('viwer', 'black', 'light gray'),
        ('focus', 'white', 'black', 'standout'),
        ('header', 'yellow', 'black', 'standout'),
        ('footer', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('error', 'dark red', 'light gray')
    ]

    def button_press(button, user_data=None):
        index = choice_path.index(user_data)
        thetitle = choice_text[index]
        frame.footer = urwid.Text('loading {}'.format(thetitle))
        try:
            contents = [urwid.Text(x) for x in file_contents(user_data).split('\n')]
            viewer = urwid.AttrWrap(urwid.ListBox(urwid.SimpleListWalker(contents)), 'viwer')
            viewer = urwid.LineBox(viewer, title=thetitle)
            frame.body = urwid.Columns([ (choice_width,choice_list), ('weight',1,viewer) ], focus_column=1,dividechars=1)
            frame.footer = urwid.Text('loaded {}'.format(thetitle))
        except:
            frame.footer = urwid.Text('Could not read {}'.format(thetitle))
   
    choice_text = []
    choice_path = [] 
    if args.directory == None and args.files == None and args.title == None:
        # No arguments supplied, use current directory.
        choice_text = [x for x in os.listdir('.') if os.path.isfile(x)]
        choice_path = [x for x in os.listdir('.') if os.path.isfile(x)]
    elif args.directory:
        # User supplid a directory
        dir = args.directory
        files = os.listdir(dir)
        choice_text = [x for x in files if os.path.isfile(os.path.join(dir, x))]
        choice_path = [os.path.join(dir, x) for x in files if os.path.isfile(os.path.join(dir, x))]
    elif args.files:
        # A list of files
        choice_text = [os.path.basename(x) for x in args.files if os.path.isfile(x)]
        choice_path = [x for x in args.files if os.path.isfile(x)]
    elif args.title:
        # Pairs of titles and files
        choice_text = [x[0] for x in args.title]
        choice_path = [x[1] for x in args.title]
    else:
        quit()
    
    choices = []
    for index in range(len(choice_text)):
        choice = urwid.Button(choice_text[index], on_press=button_press, user_data=choice_path[index])
        choices.append(choice)
    header = urwid.AttrWrap(urwid.Text(args.banner), 'header')
    choice_list = urwid.ListBox(urwid.SimpleListWalker([header] + choices))
    choice_width = min(max(len(x) for x in choice_text)+4, 24)

    contents = [urwid.Text(x) for x in file_contents(choice_path[0]).split('\n')]
    viewer = urwid.AttrWrap(urwid.ListBox(urwid.SimpleListWalker(contents)), 'viwer')
    viewer = urwid.LineBox(viewer, title=choice_text[0])

    panes = urwid.Columns([ (choice_width, choice_list), ('weight',1,viewer) ], focus_column=1,dividechars=1)
    footer = urwid.AttrWrap(urwid.Text(''), 'footer')
    frame = urwid.Frame(panes, footer=footer)
    
    
    loop = urwid.MainLoop(frame, palette=palette, unhandled_input=handle_key)
    loop.run()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--banner', default='File Viewer', help='Text to display above the file list')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--title', action='append', nargs=2, help='Specify a title and file path. Use multiple times to include more than one title,file pair')
    group.add_argument('-d', '--directory', help='Specify a directory whose files to view')
    group.add_argument('-f', '--files', nargs='+', help='Specify a list of files to view')
    args = parser.parse_args()
    print args
    main()
