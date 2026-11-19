"""Writes challenge_mat.pdf: a cover page, then the 24 sheets at their real size.

A tool, run by hand when build/mat.py changes; the PDF is committed, so the page
build does not need a browser.   python3 build/mat_pdf.py
"""
import os

from playwright.sync_api import sync_playwright

import mat

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
         '<div class="two">' + mat.overview_svg("") + '<div><h2>Missions, %d points</h2><table>%s</table></div></div></div>'
         % (mat.TOTAL, rows))
pages = [cover] + ['<div class="page">' + mat.sheet_svg(c, r) + '</div>'
                   for r in range(mat.ROWS) for c in range(mat.COLS)]
doc = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
       '@page{size:21.59cm 27.94cm;margin:0} html,body{margin:0;padding:0}'
       '.page{width:21.59cm;height:27.94cm;overflow:hidden;page-break-after:always;position:relative}'
       '.page svg{display:block}'
       '.cover{box-sizing:border-box;padding:1.5cm 1.6cm;font-family:Arial,Helvetica,sans-serif;font-size:11.5pt;line-height:1.4}'
       '.cover h1{margin:0 0 .3cm;font-size:26pt}.cover p{margin:0 0 .25cm}'
       '.cover h2{font-size:14pt;margin:0 0 .2cm}.two{display:flex;gap:.8cm;margin-top:.4cm}.two .figwrap{flex:none}.cover svg{width:8.6cm;height:auto}.cover table{border-collapse:collapse;font-size:10pt}.cover td{border:1px solid #999;padding:4px 6px;vertical-align:top}.figcap{display:none}'
       '</style></head><body>' + "".join(pages) + '</body></html>')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page()
    pg.set_content(doc)
    pg.pdf(path=OUT, prefer_css_page_size=True, print_background=True)
    b.close()
print("wrote", OUT)
