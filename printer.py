from recipe import Recipe
from reportlab.lib import pagesizes
# from xhtml2pdf import pisa             # import python module
# import fitz

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, ListFlowable, ListItem, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import custom_widgets as cw
import os
import menu
import math


class Printer:
    def __init__(self, output_pdf):
        pdfmetrics.registerFont(TTFont('Poiret One', '/home/jv/.local/share/fonts/PoiretOne-Regular.ttf'))
        # self.canvas = Canvas(output_pdf, pagesize = A4)
        
        self.dirname = cw.dirname()
        self.doc = SimpleDocTemplate(output_pdf,pagesize=A4,
                        rightMargin=24,leftMargin=24,
                        topMargin=70,bottomMargin=70)
        self.define_styles()
        self.Story = []

    def sample(self):
        Story = []
        
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='myTitle', alignment=TA_CENTER, 
                                    fontName='Poiret One', fontSize=18, textColor='#36a9d3', 
                                    leading=16, spaceBefore=6, spaceAfter=6))
        ptext = '<font color="#1a5d75">Menus</font>'
        Story.append(Paragraph(ptext, styles['myTitle']))
        ptext = 'du %s au %s' % ('lundi', 'dimanche')
        Story.append(Paragraph(ptext, styles['myTitle']))
        image = self.dirname + '/UI/images/icon_menu_3colors_LD.png'
        im = Image(image, 1*cm, 1*cm)
        Story.append(im)
        Story.append(Spacer(1, 12))

        data = [['','Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
                ['Midi', '', '', '', '', '', '', ''],
                ['Soir', '', '', '', '', '', '', '']]
        t = Table(data, style =[('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                ('BACKGROUND', (1,0), (-1,0), '#ffcb77'),
                                ('BACKGROUND', (0,1), (0,-1), '#ffcb77'),
                                ('BOX', (1,0), (-1,0), 1, '#1a5d75'),
                                ('BOX', (0,1), (0,-1), 1, '#1a5d75'),
                                ('BOX', (1,1), (-1,-1), 1, '#36a9d3')])
        Story.append(t)

        self.doc.build(Story, onFirstPage=self.AllPageSetup, onLaterPages=self.AllPageSetup)
    
    def print_shopping_list(self, my_menu, icons, images = []):
        icon_menu, icon_shopping, icon_table = icons

        #Title
        from_day_str = menu.full_date_to_french(my_menu.start_day)
        to_day = my_menu.to_day()
        to_day_str = menu.full_date_to_french(to_day)
        self.add_icon(icon_menu)
        self.write('Menus', 'Title_Center') 
        self.write('du %s au %s' % (from_day_str, to_day_str), 'Subtitle_Center')

        self.Story.append(Spacer(1, 12))
        self.write_tags(images)
        self.Story.append(Spacer(1, 12))
        
        # self.Story.append(Spacer(1, 12))

        #Table
        # if recipe_object.image != '':
        #     image_path = dirname + recipe_object.image + '_icon.jpg'

        length = len(my_menu.full_menu())

        for i in range(math.ceil(length/7)):
            full_menu = my_menu.full_menu()[i*7:(i+1)*7]
            # desserts = my_menu.desserts[i*7:(i+1)*7]
            # data = [[''],['Midi'],['Soir'],['Desserts']]
            data = [[''],['Midi'],['Soir']]

            data[0] += [col[0] for col in full_menu]
            
            menuLunch_list = []
            menuDinner_list = []
            for col in full_menu:
                if type(col[1]) == Recipe:
                    menuLunch_list.append(col[1].name)
                elif type(col[1]) == list:
                    menuLunch_list.append(' | '.join([c.name for c in col[1]]))
                if type(col[2]) == Recipe:
                    menuDinner_list.append(col[2].name)
                elif type(col[2]) == list:
                    menuDinner_list.append(' | '.join([c.name for c in col[2]]))
            data[1] += menuLunch_list
            data[2] += menuDinner_list
            
            # try:
            #     data[1] += [col[1].name for col in full_menu]
            # except:
            #     data[1] += [' | '.join([c.name for c in col[1]]) for col in full_menu]
            # try:
            #     data[2] += [col[2].name for col in full_menu]
            # except:
            #     data[2] += [' | '.join([c.name for c in col[2]]) for col in full_menu]
            # data[3] += [dessert.name for dessert in desserts]

            if math.ceil(length/7) - 1 > 0 and i == math.ceil(length/7) - 1 and length%7 != 0:#last iteration
                data[0] += [''] * (7 - length%7)
                data[1] += [''] * (7 - length%7)
                data[2] += [''] * (7 - length%7)

            self.write_table(data)
            self.Story.append(Spacer(1, 12))

        #List
        self.Story.append(PageBreak())
        self.add_icon(icon_shopping)
        self.write('Liste de courses', 'Title_Center')

        INGREDIENTS = []

        options = []
        missing = []
        for ingredient, qty_unit in my_menu.get_shopping_list().items():
            if ingredient != 'missing information':
                string = ''
                string_option = ''
                qty, unit = qty_unit
                if ingredient[0] == '[' and ingredient[-1] == ']':
                    string_option += '%s : %s' % (ingredient, qty)
                    if unit != '()':
                        string_option += unit

                    options.append(string_option)
                else:
                    string += '%s : %s' % (ingredient, qty)
                    if unit != '()':
                        string += unit

                    INGREDIENTS.append(string)
            else:
                missing.append(qty_unit) #in that case qty_unit is recipe name
        
        self.write_list(INGREDIENTS)
        
        if len(options) > 0:
            self.Story.append(Spacer(1, 12))
            self.write('Optionnel :', 'Subtitle_Left')
            self.write_list(options)
        
        if len(missing) > 0:
            self.Story.append(Spacer(1, 12))
            self.write('Ingrédients manquants pour :', 'Subtitle_Left')
            self.write_list(missing[0])

            
        #Footer
        self.add_icon(icon_table)
        self.write('<font color="#1a5d75">Bon Appétit !</font>', 'Normal_Center')
        self.doc.build(self.Story, onFirstPage=self.AllPageSetup, onLaterPages=self.AllPageSetup)
        
    def print_recipe(self, recipe, images =[]):
        self.add_icon(self.dirname + '/UI/images/icon_recipe_3colors_LD_t.png')
        self.write('Recette', 'Title_Center') 
        self.write(recipe.name, 'Subtitle_Center')
        
        image_path = self.dirname + recipe.image + '.jpg'
        if os.path.isfile(image_path):
            self.Story.append(Spacer(1, 12))
            I = Image(self.dirname + recipe.image + '.jpg')
            I.drawHeight = 5*cm*I.drawHeight / I.drawWidth
            I.drawWidth = 5*cm
            self.Story.append(I)

        self.Story.append(Spacer(1, 12))
        self.write_tags(images, size = 1)

        string_list = recipe.ingredients_string_list()
        # print(len(recipe.preparation))
        if recipe.preparation is not None:
            if len(recipe.preparation) < 900: 
                self.write_in_grid([['Ingrédients :', '', 'Préparation :'],['<br/>'.join(string_list), '', recipe.preparation.replace('\n','<br/>')]])
            else:#more than 900 characters->split into 2 tables
                first_part = recipe.preparation[:900].replace('\n','<br/>') + '...'
                last_part = '...' + recipe.preparation[900:].replace('\n','<br/>')
                self.write_in_grid([['Ingrédients :', '', 'Préparation :'],['<br/>'.join(string_list), '', first_part]])
                self.Story.append(PageBreak())
                self.write_in_case([['Préparation (suite) :'],[last_part]])
            

        if recipe.time is not None:
            self.Story.append(Spacer(1, 12))
            self.write('Temps de préparation : %s minutes' % recipe.time, 'Normal_Center')

        self.doc.build(self.Story, onFirstPage=self.AllPageSetup, onLaterPages=self.AllPageSetup)

    def define_styles(self):
        self.styles=getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Title_Center', alignment=TA_CENTER, 
                                    fontName='Poiret One', fontSize=18, textColor='#1a5d75', 
                                    leading=16, spaceBefore=6, spaceAfter=6))
        self.styles.add(ParagraphStyle(name='Subtitle_Center', alignment=TA_CENTER, 
                                    fontName='Poiret One', fontSize=18, textColor='#36a9d3', 
                                    leading=16, spaceBefore=6, spaceAfter=6))
        self.styles.add(ParagraphStyle(name='Title_Left', alignment=TA_LEFT, 
                                    fontName='Poiret One', fontSize=18, textColor='#1a5d75', 
                                    leading=16, spaceBefore=6, spaceAfter=6))
                                    # backColor='#ffcb77', borderWidth=1, borderRadius=3, borderColor='#36a9d3'))
        self.styles.add(ParagraphStyle(name='Subtitle_Left', alignment=TA_LEFT, 
                                    fontName='Poiret One', fontSize=16, textColor='#1a5d75', 
                                    leading=16, spaceBefore=6, spaceAfter=6))
        self.styles.add(ParagraphStyle(name='Normal_Center', alignment=TA_CENTER, 
                                    fontName='Poiret One', fontSize=13, textColor='#36a9d3', 
                                    leading=16, spaceBefore=6, spaceAfter=6))
        self.styles.add(ParagraphStyle(name='Normal_Left', alignment=TA_LEFT, 
                                    fontName='Poiret One', fontSize=13, textColor='#36a9d3', 
                                    leading=16, spaceBefore=6, spaceAfter=6))
        self.styles.add(ParagraphStyle(name='Boxed_Left', alignment=TA_LEFT, 
                                    fontName='Poiret One', fontSize=13, textColor='#36a9d3', 
                                    leading=16, spaceBefore=6, spaceAfter=6,
                                    backColor='#ffcb77', borderWidth=1, borderRadius=3, borderColor='#36a9d3', borderPadding=4))
        
    def write(self, text, style = 'Normal_Left'):
        self.Story.append(Paragraph(text, self.styles[style]))
    
    def write_table(self, data):
        styled_data = []
        for i, row in enumerate(data):
            styled_data.append([])
            if i == 0: #Horizontal Header
                styled_data[i] = [Paragraph('<font color="#1a5d75">%s</font>' % text, self.styles['Normal_Center']) for text in row]
            else:
                for j, text in enumerate(row):
                    if j == 0: #Vertical Header
                        styled_data[i] = [Paragraph('<font color="#1a5d75">%s</font>' % text, self.styles['Normal_Center'])]
                    else:
                        styled_data[i].append(Paragraph(text, self.styles['Normal_Center']))
        
        #TODO append every 7 days a new table

        t = Table(styled_data, style =[('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                ('BACKGROUND', (1,0), (-1,0), '#ffcb77'),
                                ('BACKGROUND', (0,1), (0,-1), '#ffcb77'),
                                ('GRID', (1,1), (-1,-1), 0.5, '#ffcb77'),
                                ('BOX', (1,0), (-1,0), 1, '#1a5d75'),
                                ('BOX', (0,1), (0,-1), 1, '#1a5d75'),
                                ('BOX', (1,1), (-1,-1), 1, '#36a9d3')])
        self.Story.append(t)
    
    def write_in_grid(self, data):
        styled_data = []
        for i, row in enumerate(data):
            
            styled_data.append([])
            if i == 0: #Horizontal Header
                styled_data[i] = [Paragraph('<font color="#1a5d75">%s</font>' % text, self.styles['Title_Left']) for text in row]
            else:
                for text in row:
                    
                    if type(text) is str:
                        styled_data[i].append(Paragraph(text, self.styles['Normal_Left']))
                    elif type(text) is list:
                        styled_data[i].append([Paragraph(sub_text, self.styles['Normal_Left']) for sub_text in text])
        
        rowH = len(styled_data) * [None]
        rowH[0] = 1*cm
        colW = [7*cm, 1*cm, 11*cm]

        t = Table(styled_data, style =[('BACKGROUND', (0,1), (0,1), '#ffcb77'),
                                        ('BACKGROUND', (2,1), (2,-1), '#ffcb77'),
                                        # ('BACKGROUND', (1,0), (-1,-1), '#ffcb77'),
                                        ('VALIGN',(0,0),(-1,0),'BOTTOM'),
                                        ('VALIGN',(0,1),(-1, -1),'TOP'),
                                        ('LEFTPADDING', (0,0), (-1,-1), 10),
                                        ('TOPPADDING', (0,1), (-1,1), 12)],
                                colWidths=colW,
                                rowHeights=rowH
                    )
        self.Story.append(t)
    

    def write_in_case(self, data):
        styled_data = []
        for i, row in enumerate(data):
            
            styled_data.append([])
            if i == 0: #Horizontal Header
                styled_data[i] = [Paragraph('<font color="#1a5d75">%s</font>' % text, self.styles['Title_Left']) for text in row]
            else:
                for text in row:
                    
                    if type(text) is str:
                        styled_data[i].append(Paragraph(text, self.styles['Normal_Left']))
                    elif type(text) is list:
                        styled_data[i].append([Paragraph(sub_text, self.styles['Normal_Left']) for sub_text in text])
        
        rowH = len(styled_data) * [None]
        rowH[0] = 1*cm
        colW = [None]

        t = Table(styled_data, style =[('BACKGROUND', (0,1), (0,1), '#ffcb77'),
                                        # ('BACKGROUND', (2,1), (2,-1), '#ffcb77'),
                                        # ('BACKGROUND', (1,0), (-1,-1), '#ffcb77'),
                                        ('VALIGN',(0,0),(-1,0),'BOTTOM'),
                                        ('VALIGN',(0,1),(-1, -1),'TOP'),
                                        ('LEFTPADDING', (0,0), (-1,-1), 10),
                                        ('TOPPADDING', (0,1), (-1,1), 12)],
                                colWidths=colW,
                                rowHeights=rowH
                    )
        self.Story.append(t)
    
    def write_tags(self, images, size = 1.6):
        data=[Image(image) for image in images]
        for I in data:
            I.drawHeight = size*cm*I.drawHeight / I.drawWidth
            I.drawWidth = size*cm
        t = Table([data], style =[
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOX', (0,0), (-1,-1), 2, '#fdf1d9'),
        ])
        self.Story.append(t)

    def write_list(self, list):
        t = ListFlowable(
            [ListItem(Paragraph(item, self.styles['Normal_Left']), value='rarrowhead') for item in list],
            bulletType='bullet',
            bulletColor='#1a5d75',
            start='rarrowhead'
        )

        self.Story.append(t)
    
    def add_icon(self, image):
        im = Image(image, 1.2*cm, 1.2*cm)
        self.Story.append(im)
    
    def AllPageSetup(self, canvas, doc):

        canvas.saveState()
        
        #background
        canvas.drawImage(self.dirname + '/UI/images/clement_chef_bg2.jpg', x=0.5*cm, y=0.5*cm, width=20*cm, height=28.7*cm)

        #header
        canvas.setFont("Poiret One", 12)
        canvas.setStrokeColor('#fdf1d9')
        canvas.setFillColor('#1a5d75')
        canvas.drawImage(self.dirname + '/UI/images/donut.png', x=1*cm, y=27.7*cm, width=1*cm, height=1*cm, mask = [0,0,0,0,0,0])
        canvas.drawString(2.2*cm, 28*cm, 'À table')
        canvas.line(1.5*cm, 27.5*cm, 19.5*cm, 27.5*cm)
        canvas.drawImage(self.dirname + '/UI/images/icon_chef_3colors.png', x=19*cm, y=27.7*cm, width=1*cm, height=1*cm, mask = [0,0,0,0,0,0])
        canvas.drawImage(self.dirname + '/UI/images/icon_recipe_3colors.png', x=17*cm, y=27.7*cm, width=1*cm, height=1*cm, mask = [0,0,0,0,0,0])
        canvas.drawImage(self.dirname + '/UI/images/icon_plate_3colors.png', x=15*cm, y=27.7*cm, width=1*cm, height=1*cm, mask = [0,0,0,0,0,0])

        #footers
        canvas.drawImage(self.dirname + '/UI/images/icon_cocktail_3colors.png', x=19*cm, y=0.9*cm, width=1*cm, height=1*cm, mask = [0,0,0,0,0,0])
        canvas.drawRightString(18.5*cm, 1.3*cm, 'Contact : notification.a.table@gmail.com')
        canvas.line(1.5*cm, 2.1*cm, 19.5*cm, 2.1*cm)
        canvas.drawImage(self.dirname + '/UI/images/score_ete_8.png', x=2*cm, y=0.9*cm, width=1*cm, height=1*cm, mask = [0,0,0,0,0,0])
        canvas.drawImage(self.dirname + '/UI/images/icon_cover_3colors_new.png', x=4*cm, y=0.9*cm, width=1*cm, height=1*cm, mask = [0,0,0,0,0,0])
        canvas.drawImage(self.dirname + '/UI/images/score_vegan_8.png', x=6*cm, y=0.9*cm, width=1*cm, height=1*cm, mask = [0,0,0,0,0,0])
        

        
        # canvas.setStrokeGray(0.90)
        # canvas.setFillGray(0.90)
        # canvas.drawCentredString(5.5 * 2.54*cm, 3.25 * 2.54*cm, 'DRAFT')

        canvas.restoreState()
    


def main():
    # pdfmetrics.registerFont(TTFont('Poiret One', '/home/jv/.local/share/fonts/PoiretOne-Regular.ttf'))
    # canvas = Canvas('test.pdf', pagesize = A4)
    # canvas.setFont('Poiret One', 18)
    # canvas.drawString(2.5 * cm, 27.2 * cm, 'Menus')
    # canvas.save()

    myPrinter = Printer('test.pdf')
    # myPrinter.sample()
    myPrinter.print_recipe(None)



# Utility function
'''
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

def find_icon_locations(input_pdf):
    image_rects = []
    doc = fitz.open(input_pdf)
    page = doc[0]
    for word in page.getText('blocks'):
        if '[ICON' in word[4]:
            x0, y0, x1, y1 = word[:4]
            image_rects.append(fitz.Rect(int(x0), int(y0), int(x0)+40, int(y0)+40))
    doc.close()
    return image_rects

def draw_icon(input_pdf, output_pdf, image_rects, icon_list):
    doc = fitz.open(input_pdf)
    page = doc[0]
    for image_rect, icon_image in zip(image_rects, icon_list):
        # print(image_rect, icon_image)
        page.insertImage(image_rect, filename = icon_image)
    doc.save(output_pdf)
    doc.close()
'''
def debug():
# Define your data
    source_html = "<html><body><p>To PDF or not to PDF</p><p>[ICON_MENU_PATH]</p></body></html>"
    with open('shopping_core.html', 'r') as html:
        data = html.readlines()
    source_html = ''.join(data)
    output_filename = "test.pdf"
    # pisa.showLogging()
    # convert_html_to_pdf(source_html, output_filename)
    # image_rects = find_icon_locations(output_filename)
    # # print(image_rects)
    # draw_icon(output_filename, "test_.pdf", image_rects, ['/home/jv/Documents/MyScripts/VSCODE/PY/Recipe/UI/images/icon_menu_3colors_LD_t.png'])


if __name__ == "__main__":
    main()
    