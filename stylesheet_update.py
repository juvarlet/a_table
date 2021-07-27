import os

def main():
    dirname = os.path.dirname(__file__)
    uiFiles = ['Main_Window', 'stacked_recipes']
    color_hex = {
            '#color1#'          : '#005d8f',
            '#color1_bright#'   : '#0085cc',
            '#color1_dark#'     : '#003049',
            '#color2#'          : '#d62828',
            '#color2_bright#'   : '#e36464',
            '#color2_dark#'     : '#ac2020',
            '#color3#'          : '#f77f00',
            '#color3_bright#'   : '#ff9c33',
            '#color3_dark#'     : '#b85f00',
            '#color4#'          : '#fcbf49',
            '#color4_bright#'   : '#fdd686',
            '#color4_dark#'     : '#fbac0e',
            '#color5#'          : '#eae2b7',
            '#color5_bright#'   : '#faf9ef',
            '#color5_dark#'     : '#dfd390'
            }
    
    for uiFile in uiFiles:
        filename_read = dirname + '/UI/%s_template.ui' % uiFile
        filename = dirname + '/UI/%s.ui' % uiFile
        newcontent = ''
        with open(filename_read, 'r') as fr:
            lines = fr.readlines()
            for line in lines:
                l = line
                for color in color_hex:
                    l = l.replace(color, color_hex[color][1:])
                newcontent += l
        with open(filename, 'w') as fw:
            fw.write(newcontent)



def debug():
    print('debug')
    
    
if __name__ == "__main__":
    main()