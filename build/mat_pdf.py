"""Writes challenge_mat.pdf: a cover page, the 24 sheets at their real size, then the
programs for every mission in Python and Word Blocks.

A tool, run by hand when build/mat.py changes; the PDF is committed, so the page
build does not need a browser.   python3 build/mat_pdf.py
"""
import os

from playwright.sync_api import sync_playwright

import mat
import render

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "challenge_mat.pdf")

rows = "".join('<tr><td>%d. %s</td><td>%d for each robot that %s</td><td>%d more if all three do it on the same run</td></tr>'
               % (m["n"], m["name"], m["each"], m["does"], m["bonus"]) for m in mat.MISSIONS)
cover = ('<div class="page cover"><h1>Space challenge mat for three robots</h1>'
         '<p><b>Print this file at 100 % size, on letter paper, upright.</b> In the print '
         'window choose Actual size. Do not choose Fit to page. Check one sheet before you '
         'print the rest: the bar in its bottom left corner must be 5 cm long.</p>'
         '<p>There are 24 sheets after this page. Each has its name in the bottom right '
         'corner: a letter for its column and a number for its row. Lay them out like the '
         'picture, edge to edge, with no gaps and no overlaps. Do not cut anything off. Tape '
         'every seam on the back, then turn the mat over. The mat is about 86 cm wide and '
         '168 cm tall.</p>'
         '<p><b>For every robot the class builds.</b> A robot with a colour sensor stops at '
         'the black dock. A robot with a distance sensor or a force sensor stops at a wall, a '
         'box that stands past the dock. A robot with no sensor stops by a number that its '
         'crew reads from the lane\'s ruler. The last 10 pages of this file are the programs for every '
         'mission, in Python and in Word Blocks. Print those on plain paper for each crew.</p>'
         '<div class="two">' + mat.overview_svg("") + '<div><h2>Missions, %d points</h2><table>%s</table></div></div></div>'
         % (mat.TOTAL, rows))
# the programs, after the sheets: Python, then the same program as blocks, in the open
prog = ['<div class="progs"><h1>Programs for every mission</h1><p>' + render.MAT_PROGRAM_INTRO
        + '</p><p>Small wheels need bigger numbers than big wheels. One full turn of a big '
        'wheel moves the robot about %d cm, and one full turn of a small wheel about %g cm. '
        'The mat\'s page has a table of first tries.</p>' % (mat.SQUARE_CM, mat.SMALL_WHEEL_CM)]
for n, name, items in render.mat_program_groups():
    title = ("Bonus mission" if n == 5 else "Mission %d" % n) + ": " + name
    if n == 3:
        prog.append('<h2>' + title + '</h2><p>Every team moves one lane down. A robot with a '
                    'sensor changes nothing after the swap. A robot with no sensor uses the '
                    'mission 1 program and changes TO_DOCK to the number for its new lane. A '
                    'wall moves with its robot: for a distance sensor its face is %d cm past '
                    'the dashed red line, and for a force sensor its face is on the dashed red '
                    'line.</p>' % mat.WALL_PAST)
    for i, (kind, lead, key) in enumerate(items):
        head = '<h2>' + title + '</h2>' if (i == 0 and n != 3) else ''
        prog.append('<div class="prog%s">' % (" first" if key == "m1" else " tall" if key == "m5" else "") + head + '<p><b>' + kind + '.</b> ' + lead + '</p>'
                    + render.mat_program_html(key, panel=False) + '</div>')
prog.append('</div>')
pages = [cover] + ['<div class="page">' + mat.sheet_svg(c, r) + '</div>'
                   for r in range(mat.ROWS) for c in range(mat.COLS)]
doc = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>' + render.CSS + '</style><style>'
       '@page{size:21.59cm 27.94cm;margin:0} html,body{margin:0;padding:0;background:#fff;max-width:none}'
       '.page{width:21.59cm;height:27.94cm;overflow:hidden;page-break-after:always;position:relative}'
       '.page svg{display:block;width:21.59cm;height:27.94cm;max-width:none}'
       '.cover{box-sizing:border-box;padding:1.5cm 1.6cm;font-family:Arial,Helvetica,sans-serif;font-size:11.5pt;line-height:1.4}'
       '.cover h1{margin:0 0 .3cm;font-size:26pt}.cover p{margin:0 0 .25cm;max-width:none}'
       '.cover h2{font-size:14pt;margin:0 0 .2cm}.two{display:flex;gap:.8cm;margin-top:.4cm}'
       '.two .figwrap{flex:none;margin:0;padding:0;border:0;overflow:visible}'
       '.cover svg.fig{width:8.6cm;min-width:0;height:auto}'
       '.two>div:last-child{flex:1}'
       '.cover table{border-collapse:collapse;font-size:10pt;width:auto;margin:0}'
       '.cover td{border:1px solid #999;padding:4px 6px;vertical-align:top}.figcap{display:none}'
       '@page code{size:21.59cm 27.94cm;margin:1.1cm 1.5cm}'
       '.progs{page:code;font-family:Arial,Helvetica,sans-serif;font-size:11pt;line-height:1.4;color:#17181B}'
       '.progs h1{font-size:22pt;margin:0 0 .3cm}.progs h2{font-size:15pt;margin:0 0 .25cm}'
       '.progs p{margin:0 0 .25cm;max-width:none}'
       '.prog{break-before:page;page-break-before:always}'
       '.progs pre.py{font-size:8.4pt;line-height:1.34;white-space:pre-wrap;margin:.15cm 0 .3cm;padding:.3cm .4cm}'
       '.prog.first{break-before:auto;page-break-before:auto}.prog.tall .wbbody{zoom:.58}.progs .prog.tall pre.py{font-size:7.8pt;line-height:1.28}'
       '.progs .wbbody{padding:0;zoom:.7}.progs figure.blocks{margin:0}'
       '</style></head><body>' + "".join(pages) + "".join(prog) + '</body></html>')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page()
    pg.set_content(doc)
    pg.pdf(path=OUT, prefer_css_page_size=True, print_background=True)
    b.close()
print("wrote", OUT)
