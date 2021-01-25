import json, os
from mdutils.mdutils import MdUtils
from mdutils.tools.TextUtils import TextUtils
from mdutils.tools.Header import Header
from natsort import natsorted

character_names = [
    'Etou_Kanami',
    'Juujou_Hiyori',
    'Yanase_Mai',
    'Itomi_Sayaka',
    'Mashiko_Kaoru',
    'Kohagura_Ellen',
    'Asakura_Mihono'
    'Setouchi_Chie',
    'Musumi_Kiyoka',
    'Shichinosato_Kofuki',
    'Kitora_Mirja',
    'Yamashiro_Yui',
    'Origami_Yukari',
    'Shidou_Maki',
    'Konohana_Suzuka',
    'Satsuki_Yomi',
    'Tsubakuro_Yume',
    'Ban_Tsugumi',
    'Fujiwara_Minato',
    'Hiiragi_Kagari',
    'Inago_Akira',
    'Inami_Suu',
    'Iwakura_Sanae',
    'Nitta_Hirona'
]

def part_titles(x):
    return {
        '2': 'Part 2: Complication',
        '3': 'Part 3: Turmoil',
        '4': 'Part 4: Bonds',
        '5': 'Part 5: Fog at First Light'
    }.get(x, 'Part')  

def generate_toc():
    toc = '[Home](/)\n'
    toc += '> :Collapse label=Main Story\n'
    toc += '> \n'
    toc += '> > :Collapse label=Part 1: Formation\n'
    toc += '> > \n'

    part1 = []
    other_parts = []    # part numbers
    chapters = []
    episodes = []
    others = []         # everything else 
    for md in os.listdir('./docs/md/docs'):
        if (md[0].isnumeric() and md[2] == '-') or 'Prologue' in md:
            part1.append(md)
        elif md[0].isnumeric():
            other_parts.append(md[0])
            chapters.append(md)
        elif 'episode' in md or 'misogi' in md or any(name in md for name in character_names):
            episodes.append(md)
        else:
            others.append(md)

    part1.sort()
    part1 = part1[-1:] + part1[:-1]
    for chp in part1:
       fn = chp.replace('.md', '')
       title = fn.replace('_', ' ')
       toc += f'> > [{title}](/docs/{fn})\n'
    
    other_parts = list(set(other_parts))
    other_parts.sort()
    for part in other_parts:
        part_chapters = [x for x in chapters if x[0] == part]
        part_chapters = natsorted(part_chapters)
        if part == '4':
            part_chapters.append('Chain_Story_Archives_Part_2.5.md')
        toc += '>\n'
        toc += f'> > :Collapse label={part_titles(part)}\n'
        toc += '> >\n'
        for chp in part_chapters:
            if (chp[3] != '.' and chp[4] != '.') or ((chp[3] == '.' or chp[4] == '.') and not any(x[2] == chp[2] and x[3] != chp[3] for x in part_chapters)):
                fn = chp.replace('.md', '')
                title = fn.replace('_', ' ')
                toc += f'> > [{title}](/docs/{fn})\n'
    
    toc += '\n> :Collapse label=Episodes\n> \n'
    for ep in episodes:
        fn = ep.replace('.md', '')
        title = fn.replace('_', ' ')
        toc += f'> [{title}](/docs/{fn})\n'

    toc += '\n> :Collapse label=Events/Misc./Unsorted\n> \n'
    for o in others:
        fn = o.replace('.md', '')
        title = fn.replace('_', ' ')
        toc += f'> [{title}](/docs/{fn})\n'

    with open('./docs/md/_toc.md', 'w') as toc_file:
        toc_file.write(toc)


def generate_file(title, data):
    mdFile = MdUtils(file_name='./docs/md/docs/' + title.replace('/', '_').replace(' ', '_') + '.md', title=title)
    for line in data.splitlines():
        line = line.replace('~', '\~')
        line = line.replace('!', '\!')
        line = line.replace('!?', '!\?')
        line = line.replace('!"', '!\\"')
        if line and (('[' == line[0] and ('Q' != line[1] and not line[2].isnumeric())) or '[R]' not in line or line[0].isnumeric()):
            mdFile.write(Header.atx_level_2(line))
        elif ':' in line and 'http' not in line:
            pos = line.find(':')
            bold_name = TextUtils.bold(line[0:pos+1])
            mdFile.write(bold_name + line[pos+1:])
            mdFile.new_line()
        # elif 'https://www.youtube' in line:
        #     id = line.replace('https://www.youtube.com/watch?v=', '')
        #     video = f'''
        #          <iframe width="560" height="315"
        #         src="https://www.youtube.com/embed/{id}" 
        #         frameborder="0" 
        #         allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        #         allowfullscreen></iframe>
        #     '''
        #     mdFile.write(video)
        #     mdFile.new_line()
        elif line:
            mdFile.write(line + "\n\n")
            mdFile.new_line()
        else:
            mdFile.write(line)
    
    mdFile.write('> :ToCPrevNext')
    mdFile.create_md_file()
    

with open('result_1.json', 'r') as res1, open('titles_1.json') as tit1, open('result_2.json') as res2, open('titles_2.json') as tit2:
    results = json.load(res1) + json.load(res2)
    titles = json.load(tit1) + json.load(tit2)

    for r in results:
        for t in titles:
            if r['paste_key'] == t['paste_key']:
                # print(t['title'], r['hits'])
                generate_file(t['title'], r['data'])
        #         break
        # else:
        #     continue
        # break

generate_toc()

