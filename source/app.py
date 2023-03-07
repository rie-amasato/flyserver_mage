import os
from flask import Flask, make_response
from mkMage import mkMage

app=Flask(__name__)

@app.route('/')
def index():
    return('<html><body><h1>index</h1></body></html>')

@app.route('/showmage/<sidelength>')
def returnMagePage(sidelength):
    return '<html><body><img src="/imgapi-mage/'+str(sidelength)+'.png"><br><img src="/imgapi-mage/'+str(sidelength)+'.svg"></body></html>'

@app.route('/imgapi-mage/<sidelength>.png')
def returnMageImg(sidelength):
    img_mage_b=mkMage.mkImg(sidelength)
    response = make_response(img_mage_b)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Cache-Control', 'no-cache')
    response.headers.set('Cache-Control', 'no-store')
    response.headers.set('Cache-Control', 'must-revalidate')
    response.headers.set('Cache-Control', 'max-age=0')
    response.headers.set('Pragma', 'no-cache')
    return response

@app.route('/imgapi-mage/<sidelength>.svg')
def returnMageSvg(sidelength):
    svg_mage_str=mkMage.mkSvg(sidelength)
    response=make_response(svg_mage_str)
    response.headers.set('Content-Type', 'image/svg+xml')
    response.headers.set('Cache-Control', 'no-cache')
    response.headers.set('Cache-Control', 'no-store')
    response.headers.set('Cache-Control', 'must_revalidate')
    response.headers.set('Cache-Control', 'max-age=0')
    response.headers.set('Pragma', 'no-cache')
    return response


if __name__=='__main__':
    print(app.url_value_preprocessor)
    app.run()
