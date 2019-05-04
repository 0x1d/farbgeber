from time import gmtime, strftime

def terminal(p):
    print("base_color ", p['b'])
    print("baseColorVariant1 ", p['v1'])
    print("baseColorVariant2 ", p['v2'])
    print("baseColorVariant3 ", p['v3'])
    print("baseColorVariant4 ", p['v4'])
    print("contrast_color ", p['c'])
    print("###################################")

def html(palette, outPath):
    base_hue = palette['base_hue']
    base_color = palette['base_color']
    base_color_variant_1 = palette['base_color_variant_1']
    base_color_variant_2 = palette['base_color_variant_2']
    base_color_variant_3 = palette['base_color_variant_3']
    base_color_variant_4 = palette['base_color_variant_4']
    contrast_color = palette['contrast_color']

    htmlpreface = """<html><head><title>visuelle Ausgabeeinheit des zentralen Farbgebers</title><meta http-equiv="refresh" content="1" />
    <style type="text/css">
    """
    htmlcontent = """</style></head><body><h1>visuelle Ausgabeeinheit des zentralen Farbgebers</h1>
    <div>BaseColor """ + base_color.hex + """</div></ br>
    <div class="base_color_variant_1">baseColorVariant1 """ + base_color_variant_1.hex + """</div>
    <div class="base_color_variant_2">baseColorVariant2 """ + base_color_variant_2.hex + """</div>
    <div class="base_color_variant_3">baseColorVariant3 """ + base_color_variant_3.hex + """</div>
    <div class="base_color_variant_4">baseColorVariant4 """ + base_color_variant_4.hex + """</div>
    <div class="Contrastcolor">Contrastcolor """ + contrast_color.hex + """</div>"""
    zeitzeile = "<h3>Color-Seed " + str(base_hue) + " " + strftime("%H:%M:%S", gmtime()) + "Uhr</h3>"
    htmlclosing = """</body></html>"""
    css1 = "body { font-size:20px; background-color:" + base_color.hex + "; color:" + contrast_color.hex + "; }"
    css2 = ".base_color_variant_1 { background-color:" + base_color_variant_1.hex + "; width:100%; height:40px; padding: 40px; font-size:20px; } \n\r"
    css3 = ".base_color_variant_2 { background-color:" + base_color_variant_2.hex + "; width:50%; height:40px; padding: 40px; font-size:20px; } \n\r"
    css4 = ".base_color_variant_3 { background-color:" + base_color_variant_3.hex + "; width:100%; height:40px; padding: 40px; font-size:20px; } \n\r"
    css5 = ".base_color_variant_4 { background-color:" + base_color_variant_4.hex + "; width:50%; height:40px; padding: 40px; font-size:20px; } \n\r"
    css6 = ".Contrastcolor { background-color:" + contrast_color.hex + "; width:10%; height:900px; position:absolute; right:300px; top:0px; color:" + base_color.hex + "; padding: 40px; font-size:20px; } \n"
    f = open(outPath, 'w')
    outputtxt = str(htmlpreface) + str(css1) + str(css2) + str(css3) + str(css4) + str(css5) + str(css6) + str(
        htmlcontent) + str(zeitzeile) + str(htmlclosing)
    f.write(outputtxt)
    f.close()
