import os

COLORS = {
                    '#color1_bright#'   : '#36a9d3',
                    '#color1#'          : '#2584a7',
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


def main():
    dirname = os.path.dirname(__file__)
    uiFiles = ['Main_Window', 'stacked_recipes']
    color_hex = COLORS
    
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

def update_colors():
    dirname = os.path.dirname(__file__)
    template = dirname + '/UI/stylesheet_template.txt'
    color_hex = COLORS
    files_ss = read_template(template)
    for file, template_str in files_ss.items():
        for color in color_hex:
            template_str = template_str.replace(color, color_hex[color][1:])
        
        filename = dirname + '/UI/%s' % file
        with open(filename, 'r') as fr:
            lines = ''.join(fr.readlines())
        body_up, ss_part, body_bottom = lines.split('/**/')
        
        lines_update = ''.join([body_up, template_str, body_bottom])
        with open(filename, 'w') as fw:
            fw.write(lines_update)
        

def read_template(template_file):
    files_ss = {}
    new_ui_file = None
    template_str = ''
    with open(template_file, 'r') as fr:
        lines = fr.readlines()
        for line in lines:
            if '.ui##' in line:
                if not new_ui_file is None and template_str != '':
                    files_ss[new_ui_file] = template_str
            
                new_ui_file = line.split('##')[1]
                template_str = ''
            else:
                template_str += line
        if not new_ui_file is None and template_str != '':
            files_ss[new_ui_file] = template_str
    return files_ss
                

def debug():
    print('debug')
    dirname = os.path.dirname(__file__)
    template = dirname + '/UI/stylesheet_template.txt'
    files_ss = read_template(template)
    print(files_ss)
    
if __name__ == "__main__":
    update_colors()