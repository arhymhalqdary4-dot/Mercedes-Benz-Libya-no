#!/usr/bin/env python3
"""Extract the Decakila catalogue from the supplied price-list PDF.

    pip install pypdf
    python3 tools/extract-catalogue.py <catalogue.pdf> data/products.json

Reads the item/name/description columns, repairs names split across lines by the
PDF's column wrapping, classifies each product into one of seven ranges, and
writes English + Arabic names and specifications. Wholesale and retail price
columns are read but intentionally not emitted.
"""
import json, re, sys
from collections import Counter, OrderedDict
from pypdf import PdfReader

PDF = sys.argv[1] if len(sys.argv) > 1 else "catalogue.pdf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "data/products.json"

def read_products(path):
    """Page text -> [{code, name, spec[]}] using the item-code column as the
    record separator."""
    lines = []
    for page in PdfReader(path).pages:
        lines += (page.extract_text() or "").split("\n")
    code_re = re.compile(r"^([A-Z]{2,4}[A-Z0-9]{3,8})\s+(.*)$")
    out, cur = [], None
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith(("Decakila item", "No. Picture")) or "رقم الصنف" in s:
            continue
        m = code_re.match(s)
        if m and re.match(r"^[A-Z]{2,4}[0-9]{3}", m.group(1)) and m.group(2) and not m.group(2)[0].isdigit():
            cur = {"code": m.group(1), "name": m.group(2).strip(), "spec": []}
            out.append(cur)
        elif cur is not None:
            cur["spec"].append(s)
    return out

prods = read_products(PDF)

num_re = re.compile(r'^[\d.,]+\s+[\d.,]+\s+[\d.,]+$')
drop_re = re.compile(r'^(packed by|packing|packaging|carton|qty|moq|remark)', re.I)

def clean(x):
    n = x['name'].strip()
    sp = list(x['spec'])
    # name wrapped onto next line
    if sp and sp[0].islower() and len(sp[0].split()) <= 2 and ':' not in sp[0] and not any(c.isdigit() for c in sp[0]):
        n = n + ' ' + sp[0]; sp = sp[1:]
    n = re.sub(r'\bsoup po\b', 'soup pot', n)
    n = re.sub(r'\s+', ' ', n).strip()
    n = n[0].upper() + n[1:]
    out = []
    for s in sp:
        if num_re.match(s) or drop_re.match(s): continue
        s = re.sub(r'\s+', ' ', s).strip()
        if len(s) < 3: continue
        out.append(s)
    return n, out

# merge spec continuation lines (a line lacking ':' following one with ':')
def merge_specs(sp):
    res = []
    for s in sp:
        if res and ':' not in s and not re.match(r'^\d', s) and not re.match(r'^(With|Made|Can|Removable|Adjustable|Suitable|Stainless|Plastic|LED|LCD)\b', s) and len(s.split()) <= 3:
            res[-1] += ' ' + s
        else:
            res.append(s)
    return res

KEYS = ['voltage','power','wattage','capacity','vacuum','speed','material','size','dimension','frequency','temperature','pressure','weight','cord','noise','output','input','refrigerant','cooling','tank','diameter','thickness','net','battery','motor','timer','display']
def pick_specs(sp):
    keyed = [s for s in sp if ':' in s and any(s.lower().startswith(k) for k in KEYS)]
    keyed += [s for s in sp if ':' in s and s not in keyed]
    feats = [s for s in sp if ':' not in s]
    return (keyed[:4] or sp[:4]), feats[:5]

CATS = [
 ('spare', [r'\bhousing\b', r'grinding filter', r'heating tube', r'metal body', r'\bleg\b', r'stirring cup', r'replacement brush', r'toothbrush heads', r'battery pack', r'battery charger', r'alkaline battery', r'sealer bags']),
 ('care',  [r'hair', r'shaver', r'trimmer', r'clipper', r'toothbrush', r'oral irrigator', r'massage', r'massager', r'fascia gun', r'body ?scale', r'body fat', r'facial steamer', r'makeup mirror', r'grooming', r'curling', r'styler', r'lady shaver', r'pet dryer', r'pet clipper']),
 ('clean', [r'vacuum cleaner', r'robotic vacuum', r'steam cleaner', r'spot cleaner', r'pressure sprayer', r'sewing machine', r'garment steamer', r'steam brush', r'steam station', r'\biron\b', r'dry iron', r'steam iron', r'hair iron']),
 ('large', [r'refrigerator', r'freezer', r'washing machine', r'water heater', r'water boiler', r'air conditioner', r'gas stove', r'freestanding oven', r'water dispenser', r'gas bbq', r'charcoal', r'thermo pot', r'coffee urn']),
 ('climate',[r'\bfan\b', r'air cooler', r'heater', r'humidifier', r'mosquito', r'pest repeller', r'quartz']),
 ('cookware',[r'\bpan\b', r'\bpot\b', r'casserole', r'\bplate\b', r'mold', r'mould', r'container', r'bottle', r'\bbowl\b', r'\bspoon\b', r'spatula', r'turner', r'\bwhisk\b', r'strainer', r'mitts', r'ladle', r'tumbler', r'\bcup set\b', r'cutting board', r'pizza cutter', r'\bgrater\b', r'slicer', r'squeezer', r'garlic chopper', r'salad spinner', r'ice cube', r'measuring', r'\bkettle\b(?!.*electric)', r'moka', r'thermometer', r'\bcan\b', r'bbq tool', r'pasta server', r'noodle roti', r'\btray\b', r'\bcutter\b', r'sauce bottle', r'\bcasserole\b']),
]
def category(name):
    n = name.lower()
    for cat, pats in CATS:
        for p in pats:
            if re.search(p, n): return cat
    return 'kitchen'

# ---- Arabic ----
BASE = OrderedDict([
 ('stirring cup assembly','طقم كوب الخلط'),('grinding filter','فلتر الطحن'),('heating tube','عنصر تسخين'),
 ('replacement brush heads','رؤوس فرشاة بديلة'),('electric toothbrush heads','رؤوس فرشاة أسنان كهربائية'),
 ('lithium-ion battery pack','بطارية ليثيوم أيون'),('battery charger','شاحن بطارية'),('alkaline battery','بطارية ألكالاين'),
 ('metal body','هيكل معدني'),('housing','هيكل خارجي'),('leg 4pcs','أرجل 4 قطع'),('leg','رجل'),
 ('vacuum sealer bags rolls','أكياس تفريغ الهواء'),('vacuum sealer machine','ماكينة تفريغ الهواء'),
 ('split type air conditioner','مكيف هواء سبليت'),('transparent window air fryer','قلاية هوائية بنافذة شفافة'),
 ('air fryer','قلاية هوائية'),('air oven','فرن هوائي'),('halogen oven','فرن هالوجين'),('toaster oven','فرن كهربائي صغير'),
 ('microwave oven','فرن ميكروويف'),('freestanding oven','فرن مستقل'),('electric pizza pan','صانعة بيتزا كهربائية'),
 ('drip coffee maker with grinder','صانعة قهوة مقطرة بمطحنة'),('drip coffee maker','صانعة قهوة مقطرة'),
 ('single serve drip coffee machine','ماكينة قهوة مقطرة فردية'),('capsule espresso machine','ماكينة إسبريسو بالكبسولات'),
 ('pump espresso coffee machine','ماكينة إسبريسو بمضخة'),('espresso coffee machine with grinder','ماكينة إسبريسو بمطحنة'),
 ('espresso maker','صانعة إسبريسو'),('turkish coffee maker','صانعة قهوة تركية'),('turkish coffee pot','ركوة قهوة تركية'),
 ('drip coffee kettle','إبريق قهوة مقطرة'),('electric coffee urn','ترمس قهوة كهربائي'),
 ('cordless coffee grinder','مطحنة قهوة لاسلكية'),('coffee grinder','مطحنة قهوة'),('moka pot','ركوة موكا'),
 ('electric milk frother','خفاقة حليب كهربائية'),('handheld milk frother','خفاقة حليب يدوية'),
 ('cordless portable blender','خلاط محمول لاسلكي'),('cordless stand blender','خلاط عمودي لاسلكي'),
 ('cordless hand blender','خلاط يدوي لاسلكي'),('stand blender','خلاط عمودي'),('hand blender','خلاط يدوي'),
 ('table blender','خلاط طاولة'),('power blender','خلاط قوي'),('powerful blender','خلاط فائق القوة'),
 ('cordless hand mixer','خفاقة يدوية لاسلكية'),('hand mixer','خفاقة يدوية'),('stand mixer','عجانة كهربائية'),
 ('cordless food processor','محضرة طعام لاسلكية'),('food processor','محضرة طعام'),
 ('cordless baby food maker','محضرة طعام أطفال لاسلكية'),('cordless mini chopper','فرامة صغيرة لاسلكية'),
 ('cordless chopper','فرامة لاسلكية'),('mini chopper','فرامة صغيرة'),('food chopper','فرامة طعام'),('chopper','فرامة'),
 ('manual garlic chopper','فرامة ثوم يدوية'),('electric meat grinder','مفرمة لحم كهربائية'),('meat grinder','مفرمة لحم'),
 ('electric pepper grinder','مطحنة فلفل كهربائية'),('centrifugal juicing machine','عصارة طرد مركزي'),
 ('citrus juicer','عصارة حمضيات'),('lemon squeezer','عصارة ليمون'),('ice crusher','كسارة ثلج'),
 ('electric kettle-stainless steel','غلاية كهربائية ستانلس ستيل'),('electric kettle-glass','غلاية كهربائية زجاجية'),
 ('electric kettle-plastic','غلاية كهربائية بلاستيكية'),('glass kettle','غلاية زجاجية'),('stainless kettle','غلاية ستانلس ستيل'),
 ('plastic kettle','غلاية بلاستيكية'),('kettle popcorn maker','صانعة فشار'),('kettle','غلاية'),
 ('electric water boiler','سخان ماء كهربائي'),('electric thermo pot','ترمس ماء كهربائي'),
 ('storage electric water heater','سخان مياه تخزيني'),('instant electric water heater','سخان مياه فوري'),
 ('water dispenser','برادة مياه'),('water can','خزان مياه'),
 ('electric pressure cooker','قدر ضغط كهربائي'),('stainless steel pressure cooker','قدر ضغط ستانلس ستيل'),
 ('aluminum pressure cooker','قدر ضغط ألمنيوم'),('rice cooker','طباخ أرز'),('slow cooker','طباخ بطيء'),
 ('egg cooker','سلاقة بيض'),('ceramic cooker','سخان سيراميك'),('electric cooker','طباخ كهربائي'),
 ('food steamer','جهاز طهي بالبخار'),('folding steamer tray','صينية طهي بالبخار قابلة للطي'),
 ('double hot plate','سخان كهربائي مزدوج'),('mini electric hot plate','سخان كهربائي صغير'),('hot plate','سخان كهربائي'),
 ('table gas stove','طباخ غاز طاولة'),('gas stove with shelf','طباخ غاز مع رف'),('gas stove','طباخ غاز'),
 ('gas bbq grill','شواية غاز'),('electric barbecue grill','شواية كهربائية'),('portable charcoal grill','شواية فحم محمولة'),
 ('charcoal bbq','شواية فحم'),('contact grill','شواية تلامسية'),('grill plate','صفيحة شواء'),
 ('bbq tool set','طقم أدوات شواء'),('electric griddle','صاج كهربائي'),('griddle','صاج'),('electric skillet','مقلاة كهربائية'),
 ('deep fryer','قلاية عميقة'),('stainless steel fryer pot','قدر قلي ستانلس ستيل'),
 ('sandwich toaster','محمصة ساندويتش'),('sandwich maker','صانعة ساندويتش'),('breakfast station','محطة إفطار'),
 ('toaster','محمصة خبز'),('bread maker','صانعة خبز'),('bun warmer','مسخن خبز'),('pizza maker','صانعة بيتزا'),
 ('round waffle maker','صانعة وافل دائرية'),('round cupcake maker','صانعة كب كيك'),('cotton candy maker','صانعة غزل البنات'),
 ('chocolate fountain','نافورة شوكولاتة'),('ice cream maker','صانعة آيس كريم'),('yogourt maker','صانعة زبادي'),
 ('automatic dumpling maker','صانعة عجينة أوتوماتيكية'),('manual noodle roti making machine','ماكينة عجين ورقائق يدوية'),
 ('hot air popcorn popper','صانعة فشار بالهواء الساخن'),('hot oil popcorn popper','صانعة فشار بالزيت'),
 ('popcorn maker cart','عربة صانعة فشار'),('electric knife sharpener','مسن سكاكين كهربائي'),('electrical knife','سكين كهربائي'),
 ('kitchen scale','ميزان مطبخ'),('smart body fat scale','ميزان ذكي لقياس الدهون'),('body scale','ميزان جسم'),
 ('meat thermometer','ميزان حرارة اللحوم'),('sterilizer cutting board and knife set','طقم تعقيم ألواح وسكاكين'),
 ('vacuum cleaner','مكنسة كهربائية'),('cordless vacuum cleaner','مكنسة كهربائية لاسلكية'),
 ('portable vacuum cleaner','مكنسة محمولة'),('robotic vacuum','مكنسة روبوت'),('portable spot cleaner','منظف بقع محمول'),
 ('steam cleaner','منظف بالبخار'),('pressure sprayer','رشاش ضغط'),('pet dryer and groomer','مجفف وتصفيف الحيوانات الأليفة'),
 ('steam iron','مكواة بخار'),('heavy dry iron','مكواة جافة ثقيلة'),('dry iron','مكواة جافة'),('steam station','محطة كي بالبخار'),
 ('steam brush','فرشاة بخار'),('handle garment steamer','مكواة بخار محمولة'),('garment steamer','مكواة بخار عمودية'),
 ('multifunction sewing machine','ماكينة خياطة متعددة الوظائف'),('handheld sewing machine','ماكينة خياطة يدوية'),
 ('mini sewing machine','ماكينة خياطة صغيرة'),
 ('twin tub washing machine','غسالة حوضين'),('single tub washing machine','غسالة حوض واحد'),
 ('front load washing machine','غسالة أوتوماتيك تحميل أمامي'),('automatic washing machine','غسالة أوتوماتيكية'),
 ('chest freezer','فريزر أفقي'),('upright freezer','فريزر رأسي'),('car refrigerator','ثلاجة سيارة'),
 ('mini refrigerator','ثلاجة صغيرة'),('refrigerator','ثلاجة'),
 ('bladeless air cooler','مبرد هواء بدون مروحة'),('air cooler','مبرد هواء'),('tower fan','مروحة برجية'),
 ('ceiling fan','مروحة سقف'),('circulation fan','مروحة تدوير هواء'),('orbit fan','مروحة دوارة'),
 ('mini telescopic fan','مروحة صغيرة قابلة للتمديد'),('fan heater','دفاية هوائية'),('quartz heater','دفاية كوارتز'),
 ('ultrasonic humidifier','مرطب هواء بالموجات فوق الصوتية'),('mosquito killer lamp','مصباح قاتل الحشرات'),
 ('mosquito killing lamp','مصباح قاتل الحشرات'),('pest repeller','طارد الحشرات'),
 ('super speed hair dryer','مجفف شعر فائق السرعة'),('hair dryer','مجفف شعر'),('hair straightener comb','مشط فرد الشعر'),
 ('hair straightener','مملس شعر'),('hair iron set','طقم مملس شعر'),('hair styler set','طقم تصفيف شعر'),
 ('hot air styler','مصفف شعر بالهواء الساخن'),('curling tong','جهاز تجعيد الشعر'),('baby hair clipper','ماكينة حلاقة للأطفال'),
 ('pet clipper','ماكينة قص شعر الحيوانات'),('hair clipper','ماكينة حلاقة'),('rotary shaver','ماكينة حلاقة دوارة'),
 ('electric foil shaver','ماكينة حلاقة بشفرة رقائقية'),('foil shaver','ماكينة حلاقة بشفرة رقائقية'),
 ('portable trip shaver','ماكينة حلاقة للسفر'),('lady shaver','ماكينة حلاقة نسائية'),('electric shaver','ماكينة حلاقة كهربائية'),
 ('shaver','ماكينة حلاقة'),('one blade trimmer','ماكينة تشذيب بشفرة واحدة'),('nose and eyebrow trimmer','ماكينة تشذيب الأنف والحواجب'),
 ('nose trimmer','ماكينة تشذيب الأنف'),('eyebrow trimmer','ماكينة تشذيب الحواجب'),('trimmer','ماكينة تشذيب'),
 ('grooming kit','طقم العناية الشخصية'),('sonic toothbrush','فرشاة أسنان سونيك'),('oral irrigator','جهاز تنظيف الأسنان بالماء'),
 ('handheld massager','جهاز مساج يدوي'),('massage gun','مسدس مساج'),('fascia gun','مسدس مساج عضلي'),
 ('ionic facial steamer','جهاز بخار للوجه أيوني'),('facial steamer','جهاز بخار للوجه'),('makeup mirror','مرآة مكياج'),
 ('forged frying pan','مقلاة مطروقة'),('forged grill pan','مقلاة شواء مطروقة'),('forged saucepan','قدر مطروق'),
 ('forged casserole','حلة مطروقة'),('double-sided frying pan','مقلاة بوجهين'),('deep frying pan','مقلاة عميقة'),
 ('stainless steel frying pan','مقلاة ستانلس ستيل'),('frying pan','مقلاة'),('crepe pan','مقلاة كريب'),
 ('stainless steel sauce pan','قدر ستانلس ستيل'),('saucepan','قدر'),('stainless steel soup pot','قدر شوربة ستانلس ستيل'),
 ('stainless steel stock pot','قدر كبير ستانلس ستيل'),('casserole','حلة'),('stainless steel bowl','وعاء ستانلس ستيل'),
 ('stainless steel fine mesh strainer','مصفاة ستانلس ستيل'),('bundt pan','قالب كيك دائري'),('loaf pan','قالب كيك مستطيل'),
 ('round cake pan','قالب كيك دائري'),('springform pan','قالب كيك قابل للفك'),('muffin pan','قالب مافن'),
 ('pie pan','قالب فطائر'),('silicone cupcake mold','قالب كب كيك سيليكون'),('popsicles mold','قالب مثلجات'),
 ('cakepops plate','صفيحة كيك بوبس'),('donut plate','صفيحة دونات'),('fish plate','صفيحة سمك'),
 ('rice ball plate','صفيحة كرات الأرز'),('shell plate','صفيحة أصداف'),('triangle plate','صفيحة مثلثات'),
 ('oval plate','صفيحة بيضاوية'),('round plate','صفيحة دائرية'),('waffle plate','صفيحة وافل'),
 ('star plate sharp cookie plate','صفيحة كوكيز نجمية'),('sealed food container set','طقم حافظات طعام محكمة'),
 ('sealed food container','حافظة طعام محكمة'),('food container set','طقم حافظات طعام'),('ice cube trays set','طقم قوالب ثلج'),
 ('plastic cup set','طقم أكواب بلاستيك'),('plastic water bottle','زجاجة ماء بلاستيك'),('drinking bottle','زجاجة شرب'),
 ('sauce bottle','زجاجة صلصة'),('mug tumbler','كوب حراري'),('silicone oven mitts','قفازات فرن سيليكون'),
 ('cotton oven mitts','قفازات فرن قطنية'),('silicone spatula','ملعقة سيليكون'),('slotted turner','مقلبة مثقبة'),
 ('slotted spoon','ملعقة مثقبة'),('solid spoon','ملعقة تقديم'),('pasta server','ملعقة معكرونة'),('ladle','مغرفة'),
 ('measuring spoon-plastic','ملاعق قياس بلاستيك'),('spin whisk','خفاقة دوارة'),('whisk','خفاقة يدوية'),
 ('salad spinner','مجفف سلطة'),('drum grater','مبشرة أسطوانية'),('mandoline slicer','مقطعة شرائح'),
 ('potato cutter','مقطعة بطاطس'),('pizza cutter','قطاعة بيتزا'),('can opener','فتاحة علب'),
])

MOD = [('cordless','لاسلكي'),('portable','محمول'),('mini','صغير'),('electric','كهربائي'),('stainless steel','ستانلس ستيل')]

def arabic(name):
    n = name.lower().strip()
    if n in BASE: return BASE[n]
    for k in sorted(BASE, key=len, reverse=True):
        if k in n: return BASE[k]
    return name

CAT_LABEL = {
 'kitchen':  ('Kitchen Appliances','أجهزة المطبخ'),
 'large':    ('Major Appliances','الأجهزة الكبيرة'),
 'clean':    ('Home Care & Cleaning','العناية بالمنزل'),
 'care':     ('Personal Care','العناية الشخصية'),
 'climate':  ('Cooling & Heating','التبريد والتدفئة'),
 'cookware': ('Cookware & Kitchenware','أدوات وأواني المطبخ'),
 'spare':    ('Spare Parts','قطع الغيار'),
}

SPEC_KEYS = [('voltage','الجهد'),('wattage','القدرة'),('power','القدرة'),('capacity','السعة'),('vacuum','قوة الشفط'),
 ('speed','السرعة'),('material','الخامة'),('size','المقاس'),('product size','المقاس'),('dimension','الأبعاد'),
 ('frequency','التردد'),('temperature','درجة الحرارة'),('pressure','الضغط'),('weight','الوزن'),('net weight','الوزن الصافي'),
 ('power cord','طول السلك'),('noise','مستوى الصوت'),('output','الخرج'),('input','الدخل'),('refrigerant','غاز التبريد'),
 ('cooling capacity','قدرة التبريد'),('tank capacity','سعة الخزان'),('diameter','القطر'),('thickness','السماكة'),
 ('battery','البطارية'),('charging time','مدة الشحن'),('working time','مدة التشغيل'),('timer','المؤقت'),
 ('dust bag capacity','سعة كيس الغبار'),('dust cup capacity','سعة الوعاء'),('rated pressure','ضغط التشغيل')]

def spec_ar(s):
    if ':' not in s: return s
    k, v = s.split(':', 1)
    kl = k.strip().lower()
    for en, ar in sorted(SPEC_KEYS, key=lambda t: -len(t[0])):
        if kl == en or kl.startswith(en): return ar + ': ' + v.strip()
    return k.strip() + ': ' + v.strip()

def tidy(s):
    s = re.sub(r'\s*:\s*', ': ', s, count=1)
    return re.sub(r'\s+', ' ', s).strip()

seen = set(); items = []
for x in prods:
    n, sp = clean(x)
    if not n or n.lower() in ('picture','product name'): continue
    key = x['code']
    if key in seen: continue
    seen.add(key)
    sp = merge_specs(sp)
    specs, feats = pick_specs(sp)
    items.append({
        'c': x['code'], 'n': n, 'na': arabic(n), 'cat': category(n),
        's': [tidy(s)[:70] for s in specs],
        'sa': [tidy(spec_ar(s))[:70] for s in specs],
        'f': [f[:80] for f in feats],
    })

print('total', len(items))
print(Counter(i['cat'] for i in items))
untranslated = [i['n'] for i in items if i['na'] == i['n']]
print('untranslated', len(set(untranslated)), sorted(set(untranslated))[:20])
for i in items:                       # trim to what the cards render
    i['s'] = i['s'][:3]; i['sa'] = i['sa'][:3]
    i['f'] = [f for f in i['f'] if len(f) > 8][:3]

with open(OUT, 'w') as fh:
    json.dump({'cats': CAT_LABEL, 'items': items}, fh, ensure_ascii=False, separators=(',', ':'))
print('wrote', OUT)
