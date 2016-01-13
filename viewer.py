#!/usr/bin/env python
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
        ('focus', 'dark red', 'dark blue', 'standout'),
        ('header', 'yellow', 'black', 'standout'),
        ('footer', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('error', 'dark red', 'light gray')
    ]

    def button_press(button, user_data=None):
        frame.footer = urwid.Text('loading {}'.format(user_data))
        try:
            contents = [urwid.Text(x) for x in file_contents(user_data).split('\n')]
            viewer = urwid.AttrWrap(urwid.ListBox(urwid.SimpleListWalker(contents)), 'viwer')
            frame.body = urwid.Columns([ (choice_width,choice_list), ('weight',1,viewer) ], focus_column=1,dividechars=1)
            frame.footer = urwid.Text('loaded {}'.format(user_data))
        except:
            frame.footer = urwid.Text('Could not read {}'.format(user_data))
    
    choice_text = os.listdir('.')
    choices = [urwid.AttrWrap(urwid.Button(x, on_press=button_press, user_data=x), 'focus') for x in choice_text]
    choice_list = urwid.ListBox(urwid.SimpleListWalker(choices))
    choice_width = min(max(len(x) for x in choice_text)+4, 24)

    contents = [urwid.Text(x) for x in file_contents(choices[3].label).split('\n')]
    viewer = urwid.AttrWrap(urwid.ListBox(urwid.SimpleListWalker(contents)), 'viwer')

    header = urwid.AttrWrap(urwid.Text('File Viewer'), 'header')
    panes = urwid.Columns([ (choice_width,choice_list), ('weight',1,viewer) ], focus_column=1,dividechars=1)
    footer = urwid.AttrWrap(urwid.Text(''), 'footer')
    frame = urwid.Frame(panes, header=header, footer=footer)
    
    
    loop = urwid.MainLoop(frame, palette=palette, unhandled_input=handle_key)
    loop.run()

if __name__ == '__main__':
    main()
