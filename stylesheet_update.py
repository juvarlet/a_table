import os

def main():
    dirname = os.path.dirname(__file__)
    uiFiles = ['Main_Window', 'stacked_recipes']
    color_hex = {
                    '#color1_bright#'   : '#36a9d3',
                    '#color1#'          : '#227c9d',
                    '#color1_dark#'     : '#1a5d75',
                    '#color2_bright#'   : '#fe9a9d',
                    '#color2#'          : '#fe6d73',
                    '#color2_dark#'     : '#fe484e',
                    '#color3_bright#'   : '#ffe0ad',
                    '#color3#'          : '#ffcb77',
                    '#color3_dark#'     : '#ffc05c',
                    '#color4_bright#'   : '#24e5d2',
                    '#color4#'          : '#17c3b2',
                    '#color4_dark#'     : '#13a496',
                    '#color5_bright#'   : '#fef9ef',
                    '#color5#'          : '#fdf1d9',
                    '#color5_dark#'     : '#fae2b2'
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